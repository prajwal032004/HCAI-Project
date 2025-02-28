
# HCAI-Based E-Commerce Website

This project is an **AI-powered e-commerce automation system** that helps users add items to their shopping carts on **Amazon, Flipkart, and Meesho** using **Human-Centered AI (HCAI)**.

## 🚀 Features
- **AI-Powered Request Parsing**: Uses OpenAI's GPT to process user shopping requests.
- **Automated Shopping**: Searches for products and adds them to carts using Selenium.
- **Multi-Platform Support**: Works with Amazon, Flipkart, and Meesho.
- **Screenshot Verification**: Captures screenshots of cart addition for confirmation.
- **Flask Web Interface**: User-friendly input form.

---

## 🛠 Installation

### **Prerequisites**
- Python 3.x
- Google Chrome & ChromeDriver
- Virtual environment (recommended)

### **Setup Instructions**
\`\`\`bash
# Clone the Repository
git clone <repository-url>
cd hcai_ecommerce

# Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows

# Install Dependencies
pip install -r requirements.txt

# Set Up Environment Variables
echo "OPENAI_API_KEY='your-api-key'" > .env

# Run the Application
python app.py
\`\`\`

---

## 🌐 API Endpoints

### **Home Page**
\`\`\`http
GET /
\`\`\`
Loads the main web interface.

### **Process Shopping Request**
\`\`\`http
POST /process_request
\`\`\`
**Request Example:**
\`\`\`json
{
  "user_request": "Buy a black t-shirt size M from Amazon"
}
\`\`\`

**Response Example:**
\`\`\`json
{
  "success": true,
  "message": "Item successfully added to Amazon cart!",
  "parsed_request": {
    "website": "amazon",
    "item_name": "black t-shirt",
    "quantity": 1,
    "specific_requirements": "size M"
  },
  "screenshots": [
    "/static/screenshots/cart.png"
  ]
}
\`\`\`

---

## 🏗️ Project Structure
\`\`\`bash
.
├── app.py                # Flask backend
├── templates/
│   ├── index.html        # Web UI
├── static/
│   ├── screenshots/      # Captured screenshots
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── README.md             # Documentation
├── setup_project.sh      # Bash setup script
\`\`\`

---

## 📜 License
MIT License - Use freely with proper attribution.

EOL

echo "✅ README.md generated successfully!"

# Step 3: Create a basic Flask app file
echo "🐍 Setting up Flask app..."
cat <<EOL > $PROJECT_FOLDER/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the HCAI-Based E-Commerce Bot!"

@app.route("/process_request", methods=["POST"])
def process_request():
    data = request.json
    return jsonify({
        "success": True,
        "message": f"Processing request for: {data.get('user_request')}"
    })

if __name__ == "__main__":
    app.run(debug=True)
EOL

echo "✅ Flask app created!"

# Step 4: Create requirements.txt
echo "📜 Installing dependencies..."
cat <<EOL > $PROJECT_FOLDER/requirements.txt
Flask
requests
selenium
python-dotenv
openai
EOL

# Step 5: Install dependencies in a virtual environment
cd $PROJECT_FOLDER
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

echo "✅ Dependencies installed!"

# Step 6: Create a .env file
echo "🔑 Setting up environment variables..."
cat <<EOL > $PROJECT_FOLDER/.env
OPENAI_API_KEY="your-api-key"
EOL

echo "✅ Environment setup complete!"

# Step 7: Display success message
echo "🎉 Project setup complete! Navigate to '$PROJECT_FOLDER' and run 'python app.py' to start."
