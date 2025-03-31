# Dropoff Detection System Documentation

## Table of Contents
1. [Overview](#overview)
2. [Installation and Setup](#installation-and-setup)
   - [Backend Instructions](#backend-setup)
   - [Frontend Instructions](#frontend-setup)
3. [API Documentation](#api-documentation)
4. [User Guide](#user-guide)
5. [Folder Structure](#folder-structure)
6. [System Architecture](#system-architecture)
7. [Best Practices](#best-practices)
8. [Conclusion](#conclusion)

---

## Overview
The **Dropoff Detection System** is a web application designed to validate if a package has been delivered at the correct location. Users input a description of where the package was left and upload an image of that location. The system uses OpenAI’s GPT-4o model to determine the validity of the delivery and returns a message indicating whether it is "Valid" or "Invalid".

---

## Installation and Setup

### Backend Setup
1. Ensure that Python (3.7 or higher) and pip are installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn openai python-dotenv
   ```
4. Create a `.env` file in the `backend` directory containing your OpenAI API key:
   ```
   OPENAI_KEY=your_openai_api_key_here
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Ensure Node.js (version 14 or higher) and npm are installed.
2. Navigate to the `frontend` directory and install dependencies:
   ```bash
   npm install
   ```
3. Start the React application:
   ```bash
   npm start
   ```

---

## API Documentation

### POST `/validate/`
- **Description**: Validates the package drop-off by comparing the user-provided description with the uploaded image.
- **Request Body**: Form data containing:
  - `description`: (string) Text description of the delivery location.
  - `file`: (image) Image of the delivery location.
  
- **Response**:
  ```json
  {
    "answer": "Valid" or "Invalid",
    "reasoning": "Explanation of why the answer is Valid or Invalid"
  }
  ```

### Example Request in Python
```python
import requests

url = 'http://localhost:8000/validate/'
files = {'file': open('path_to_image.jpg', 'rb')}
data = {'description': 'Front porch of the house'}

response = requests.post(url, files=files, data=data)
print(response.json())
```

---

## User Guide

### Using the Dropoff Detection System
1. Launch the web application in your browser at `http://localhost:3000`.
2. Fill in the text box with a description of where the package was delivered.
3. Upload an image of the delivery location using the provided file input.
4. Click the "Validate Dropoff" button to initiate the validation process.
5. A response of "Valid" or "Invalid" will be displayed based on the analysis.
6. If available, you can toggle to view the reasoning for the validation decision.

---

## Folder Structure
```
DropoffDetectionSystem/
├── backend/
│   ├── main.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   ├── public/
│   └── package.json
└── README.md
```

---

## System Architecture

The Dropoff Detection System architecture consists of two main components: **Frontend** and **Backend**.

### Frontend
- Technology: React.js
- Functionality: Collects user inputs and interacts with the backend API.
  
### Backend
- Technology: FastAPI (Python)
- Components:
  - Receives image and description.
  - Encodes images to base64 and processes requests to OpenAI API.
  
```plaintext
+-------------------+                   +----------------------+                   +----------------+
|                   |                   |                      |                   |                |
|  Frontend (UI)    | <---------------- |    FastAPI API      | <---------------- |  OpenAI API    |
|                   |    HTTP Requests   |                      |   API Calls       |                |
+-------------------+                   +----------------------+                   +----------------+
```

---

## Best Practices
- **Security**: Use HTTPS to secure API calls.
- **Modular Code**: Structure the backend code into modules for better maintainability.
- **Environment Variables**: Store sensitive keys and configurations in environment variables.
- **Comments and Documentation**: Ensure that code is well-commented and includes adequate documentation.

---

## Conclusion
The Dropoff Detection System provides an intuitive way for users to verify package deliveries based on location descriptions and images. With remote validation powered by OpenAI’s technology, the application's structure and comprehensive documentation facilitate easy setup and user experience. This system is poised to offer effective and accurate delivery validations.

--- 

This documentation serves as a complete guide for developers and users to effectively set up and use the Dropoff Detection System.