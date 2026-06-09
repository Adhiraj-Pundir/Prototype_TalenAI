# TalentAI Prototype

TalentAI is a code evaluation prototype that uses the Gemini AI model to evaluate candidate code submissions and provide HR-friendly recommendations (Pass/No-Pass) along with detailed feedback.

## Project Structure

This repository is split into two parts:
- **`backend/`**: A FastAPI application that handles code execution and AI evaluation.
- **`frontend/`**: A React-based UI that includes a code editor and displays the problem description and evaluation results.

## Prerequisites

- Python 3.10+
- Node.js 18+
- A valid [Google Gemini API Key](https://aistudio.google.com/api-keys)

## Running Locally

### 1. Start the Backend

Navigate to the `backend` directory, set up your Python environment, and start the server:

```bash
cd backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key in the .env file
echo "GEMINI_API_KEY=your_actual_key_here" > .env

# Run the backend
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```
*Note: The backend runs on port `8001`.*

### 2. Start the Frontend

In a new terminal window, navigate to the `frontend` directory and start the Vite dev server:

```bash
cd frontend

# Install dependencies
npm install

# Start the frontend
npm run dev
```
*Note: The frontend will be available at `http://localhost:5173/`.*

## Features

- **Problem Selection**: Choose from multiple pre-defined coding challenges (e.g., Two Sum, Palindrome Number, Valid Anagram).
- **Code Execution Engine**: Safely executes Python code against pre-defined test cases using `eval()` and `exec()` locally.
- **AI Evaluation**: The Gemini AI evaluates the executed code and its test results to provide a structured, confident recommendation for hiring managers.

## Deployment

This prototype is configured to be deployed on platforms like **Render**. 
- The backend URL is automatically detected in the frontend (`import.meta.env.DEV`), ensuring seamless transitions between local development and production.
