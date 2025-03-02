
# HCAI-Based E-Commerce Website 🛒

This project is an **AI-powered e-commerce automation system** that helps users add items to their shopping carts on **Amazon, Flipkart, and Meesho** using **Human-Centered AI (HCAI)**.

## 🚀 Features
- **AI-Powered Request Parsing**: Uses a regex-based parser to process user shopping requests.
- **Automated Shopping**: Searches for products and adds them to carts using Selenium.
- **Multi-Platform Support**: Works with Amazon, Flipkart, and Meesho.
- **Screenshot Verification**: Captures screenshots at key stages (confirmation and cart) for verification.
- **Flask Web Interface**: Provides a user-friendly input form.

## 🛠 Installation

### **Prerequisites**
- Python 3.x
- Google Chrome & ChromeDriver (managed automatically using `webdriver_manager`)
- Virtual environment (recommended)

### **Setup Instructions**
Clone the repository, create a virtual environment, install dependencies, and set up environment variables:

```bash
# Clone the Repository
git clone https://github.com/prajwal032004/HCAI-Project.git
cd hcai_ecommerce

# Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate   # For Linux/macOS
# For Windows use: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Set Up Environment Variables
echo "OPENAI_API_KEY='your-api-key'" > .env

# Run the Application
python app.py
```
## 🌐 API Endpoints
```bash
Home Page

GET /

Returns the main web interface.

Process Shopping Request

POST /process_request

Request Example:

{
  "user_request": "Buy 2 black t-shirts size M from Amazon"
}

Response Example:

{
  "parsed_request": {
    "website": "amazon",
    "item_name": "black t-shirts",
    "quantity": 2,
    "specific_requirements": "black size m"
  },
  "success": true,
  "message": "Item successfully added to Amazon cart!",
  "process_log": [
    "Starting Amazon shopping process...",
    "Navigated to Amazon website",
    "... (additional process steps)"
  ],
  "screenshots": [
    "/static/screenshots/confirmation.png",
    "/static/screenshots/cart.png"
  ]
}
```
🏗️ Project Structure
```bash
.
├── app.py                # Flask backend with Selenium automation
├── templates/
│   └── index.html        # Web UI
├── static/
│   └── screenshots/      # Captured screenshots
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md             # Project documentation
```
📜 License

MIT License - Free to use with proper attribution.

Simply copy and paste this into your README.md file in your repository. This documentation covers all aspects of the project—from features and installation to API endpoints and project structure.

