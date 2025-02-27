# app.py
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import re

app = Flask(__name__)

# Simple parser function to replace LangChain and OpenAI
def parse_shopping_request(user_request):
    # Convert to lowercase for easier pattern matching
    request_lower = user_request.lower()
    
    # Default values
    website = "amazon"  # Default to Amazon
    item_name = ""
    quantity = 1
    specific_requirements = ""
    
    # Determine website
    if "amazon" in request_lower:
        website = "amazon"
    elif "flipkart" in request_lower:
        website = "flipkart"
    elif "meesho" in request_lower:
        website = "meesho"
    
    # Extract quantity using regex
    quantity_pattern = r'(\d+)\s+(pieces|pcs|items?|units?)'
    quantity_match = re.search(quantity_pattern, request_lower)
    if quantity_match:
        try:
            quantity = int(quantity_match.group(1))
        except ValueError:
            quantity = 1
    
    # Look for common descriptive words indicating requirements
    color_pattern = r'(red|blue|green|yellow|black|white|pink|purple|orange|gray|grey|brown)\s+'
    color_match = re.search(color_pattern, request_lower)
    
    size_pattern = r'(size\s+)(xs|s|m|l|xl|xxl|\d+)'
    size_match = re.search(size_pattern, request_lower)
    
    brand_pattern = r'(by|from|brand)\s+([a-z0-9]+)'
    brand_match = re.search(brand_pattern, request_lower)
    
    # Collect specific requirements
    requirements = []
    if color_match:
        requirements.append(color_match.group(1))
    if size_match:
        requirements.append(f"size {size_match.group(2)}")
    if brand_match:
        requirements.append(f"brand {brand_match.group(2)}")
    
    specific_requirements = " ".join(requirements)
    
    # Extract item name - everything that's not website, quantity, or specific requirements
    # This is a simplified approach that should work for basic requests
    words = request_lower.split()
    skip_words = ["add", "buy", "purchase", "get", "to", "my", "cart", "from", "on", "in", 
                 "amazon", "flipkart", "meesho", "pieces", "pcs", "items", "item", "units", "unit"]
    skip_words.extend(requirements)
    
    item_words = []
    for word in words:
        if word not in skip_words and not re.match(r'^\d+$', word):
            item_words.append(word)
    
    item_name = " ".join(item_words).strip()
    
    return {
        "website": website,
        "item_name": item_name,
        "quantity": quantity,
        "specific_requirements": specific_requirements
    }

# Function to initialize the WebDriver
def get_driver():
    chrome_options = Options()
    # Comment the next line for development to see the browser in action
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to add item to Amazon cart
def add_to_amazon_cart(item_name, specific_requirements="", quantity=1):
    driver = get_driver()
    process_log = []
    
    try:
        # Log the start of the process
        process_log.append("Starting Amazon shopping process...")
        
        # Navigate to Amazon
        driver.get("https://www.amazon.com")
        process_log.append("Navigated to Amazon website")
        
        # Wait for search box to be available and search for the item
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        
        # Create search query incorporating specific requirements
        search_query = f"{item_name} {specific_requirements}".strip()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        process_log.append(f"Searched for: {search_query}")
        
        # Wait for search results to load and click on the first item
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.s-result-item h2 a"))
        )
        first_result.click()
        process_log.append("Clicked on the first search result")
        
        # Wait for the add to cart button to appear and click it
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        )
        
        # If quantity is more than 1, try to set the quantity first
        if quantity > 1:
            try:
                # Try to find quantity dropdown
                quantity_dropdown = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "quantity"))
                )
                quantity_dropdown.click()
                # Select the quantity option
                quantity_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"#quantity option[value='{quantity}']"))
                )
                quantity_option.click()
                process_log.append(f"Set quantity to {quantity}")
            except:
                process_log.append(f"Could not set quantity to {quantity}, using default")
        
        # Click add to cart
        add_to_cart_button.click()
        process_log.append("Added item to cart")
        
        # Take a screenshot of the confirmation page
        screenshot_path = os.path.join("static", "screenshots", "confirmation.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        process_log.append("Saved confirmation screenshot")
        
        # Wait to make sure the item is added to cart
        time.sleep(2)
        
        # Navigate to cart to verify
        driver.get("https://www.amazon.com/gp/cart/view.html")
        process_log.append("Navigated to cart to verify item was added")
        
        # Take a screenshot of the cart
        cart_screenshot_path = os.path.join("static", "screenshots", "cart.png")
        driver.save_screenshot(cart_screenshot_path)
        process_log.append("Saved cart screenshot")
        
        success = True
        message = "Item successfully added to Amazon cart!"
        
    except Exception as e:
        success = False
        message = f"Error: {str(e)}"
        process_log.append(f"Error occurred: {str(e)}")
    
    finally:
        driver.quit()
        process_log.append("Closed browser session")
    
    return {
        "success": success,
        "message": message,
        "process_log": process_log,
        "screenshots": [
            "/static/screenshots/confirmation.png",
            "/static/screenshots/cart.png"
        ] if success else []
    }

# Function to add item to Flipkart cart
def add_to_flipkart_cart(item_name, specific_requirements="", quantity=1):
    driver = get_driver()
    process_log = []
    
    try:
        # Log the start of the process
        process_log.append("Starting Flipkart shopping process...")
        
        # Navigate to Flipkart
        driver.get("https://www.flipkart.com")
        process_log.append("Navigated to Flipkart website")
        
        # Close login popup if it appears
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button._2KpZ6l._2doB4z"))
            )
            close_button.click()
            process_log.append("Closed login popup")
        except:
            process_log.append("No login popup appeared or couldn't close it")
        
        # Wait for search box to be available and search for the item
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Create search query incorporating specific requirements
        search_query = f"{item_name} {specific_requirements}".strip()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        process_log.append(f"Searched for: {search_query}")
        
        # Wait for search results to load and click on the first item
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div._1AtVbE div._13oc-S div._4ddWXP a"))
        )
        first_result.click()
        process_log.append("Clicked on the first search result")
        
        # Switch to the new tab that opens
        driver.switch_to.window(driver.window_handles[1])
        process_log.append("Switched to product detail page")
        
        # If quantity is more than 1, try to increase quantity
        if quantity > 1:
            try:
                for _ in range(quantity - 1):
                    increase_qty_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._23FHuj:last-child"))
                    )
                    increase_qty_button.click()
                    time.sleep(0.5)
                process_log.append(f"Set quantity to {quantity}")
            except:
                process_log.append(f"Could not set quantity to {quantity}, using default")
        
        # Wait for the add to cart button to appear and click it
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._2KpZ6l._2U9uOA._3v1-ww"))
        )
        add_to_cart_button.click()
        process_log.append("Added item to cart")
        
        # Take a screenshot of the cart page
        screenshot_path = os.path.join("static", "screenshots", "flipkart_cart.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        process_log.append("Saved cart screenshot")
        
        success = True
        message = "Item successfully added to Flipkart cart!"
        
    except Exception as e:
        success = False
        message = f"Error: {str(e)}"
        process_log.append(f"Error occurred: {str(e)}")
    
    finally:
        driver.quit()
        process_log.append("Closed browser session")
    
    return {
        "success": success,
        "message": message,
        "process_log": process_log,
        "screenshots": ["/static/screenshots/flipkart_cart.png"] if success else []
    }

# Function to add item to Meesho cart
def add_to_meesho_cart(item_name, specific_requirements="", quantity=1):
    driver = get_driver()
    process_log = []
    
    try:
        # Log the start of the process
        process_log.append("Starting Meesho shopping process...")
        
        # Navigate to Meesho
        driver.get("https://www.meesho.com")
        process_log.append("Navigated to Meesho website")
        
        # Wait for search box to be available and search for the item
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        
        # Create search query incorporating specific requirements
        search_query = f"{item_name} {specific_requirements}".strip()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        process_log.append(f"Searched for: {search_query}")
        
        # Wait for search results to load and click on the first item
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.NewProductCard__Wrapper-sc-j0e7tu-0 a"))
        )
        first_result.click()
        process_log.append("Clicked on the first search result")
        
        # If quantity is more than 1, try to increase quantity
        if quantity > 1:
            try:
                # Click on plus button multiple times
                for _ in range(quantity - 1):
                    qty_plus_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='plus_btn']"))
                    )
                    qty_plus_button.click()
                    time.sleep(0.5)
                process_log.append(f"Set quantity to {quantity}")
            except:
                process_log.append(f"Could not set quantity to {quantity}, using default")
        
        # Wait for the add to cart button to appear and click it
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='add_to_cart']"))
        )
        add_to_cart_button.click()
        process_log.append("Added item to cart")
        
        # Take a screenshot of the confirmation
        screenshot_path = os.path.join("static", "screenshots", "meesho_confirmation.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        process_log.append("Saved confirmation screenshot")
        
        # Navigate to cart to verify
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']"))
        )
        cart_button.click()
        process_log.append("Navigated to cart to verify item was added")
        
        # Take a screenshot of the cart
        cart_screenshot_path = os.path.join("static", "screenshots", "meesho_cart.png")
        driver.save_screenshot(cart_screenshot_path)
        process_log.append("Saved cart screenshot")
        
        success = True
        message = "Item successfully added to Meesho cart!"
        
    except Exception as e:
        success = False
        message = f"Error: {str(e)}"
        process_log.append(f"Error occurred: {str(e)}")
    
    finally:
        driver.quit()
        process_log.append("Closed browser session")
    
    return {
        "success": success,
        "message": message,
        "process_log": process_log,
        "screenshots": [
            "/static/screenshots/meesho_confirmation.png",
            "/static/screenshots/meesho_cart.png"
        ] if success else []
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_request', methods=['POST'])
def process_request():
    user_request = request.form.get('user_request')
    
    # Use simple parser instead of LangChain
    try:
        parsed_json = parse_shopping_request(user_request)
        
        # Extract necessary information
        website = parsed_json.get("website", "amazon").lower()
        item_name = parsed_json.get("item_name", "")
        quantity = int(parsed_json.get("quantity", 1))
        specific_requirements = parsed_json.get("specific_requirements", "")
        
        # Process based on website
        if website == "amazon":
            result = add_to_amazon_cart(item_name, specific_requirements, quantity)
        elif website == "flipkart":
            result = add_to_flipkart_cart(item_name, specific_requirements, quantity)
        elif website == "meesho":
            result = add_to_meesho_cart(item_name, specific_requirements, quantity)
        else:
            return jsonify({
                "success": False,
                "message": f"Unsupported website: {website}. Currently supported: amazon, flipkart, meesho",
                "process_log": [f"Received request for unsupported website: {website}"]
            })
        
        # Return the result
        return jsonify({
            "parsed_request": parsed_json,
            **result
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}",
            "process_log": [f"Error: {str(e)}"]
        })

if __name__ == '__main__':
    # Create screenshots directory if it doesn't exist
    os.makedirs(os.path.join("static", "screenshots"), exist_ok=True)
    app.run(debug=True)