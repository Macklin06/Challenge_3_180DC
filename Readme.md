# Courtroom Clash ⚖️
A Streamlit application that simulates a legal debate between two AI lawyers: a fact-based lawyer using Retrieval-Augmented Generation (RAG) and a creative, "chaos" lawyer. This project is a fun way to demonstrate the power of prompt engineering and RAG.

## Features ✨
- **RAG Lawyer:** Uses a small, internal legal database to find and cite precedents for its arguments, demonstrating fact-grounded AI.
- **Chaos Lawyer:** Generates absurd and nonsensical arguments, ignoring all facts for creative effect.
- **Interactive UI:** Simple Streamlit interface to start a new trial, introduce evidence, and declare a verdict.
- **API Integration:** Powered by the Gemini API for AI-generated arguments.

## Prerequisites 🛠️
- Python installed
- VS Code installed
- Google API key for Gemini model

## Setup Instructions 🚀
1. **Clone the Repository (or create the files):**
	- If you have a Git repository, clone it.
	- Otherwise, create the following three Python files in a single folder:
	  - `app.py`
	  - `backend.py`
	  - `frontend.py`

2. **Install Dependencies:**
	- Open your terminal and run:
	  ```bash
	  pip install streamlit requests
	  ```

3. **Add Your API Key:**
	- Open `app.py` in VS Code. When you run the app, use the sidebar to paste your Google API key. The app will not work without it.

4. **Run the Application:**
	- In your terminal, navigate to the project directory and run:
	  ```bash
	  streamlit run app.py
	  ```
	- Your browser should open with the "Courtroom Clash" app running.

## How It Works 🧠
The application is split into three main files:
- **app.py:** Main entry point, manages app memory and button clicks.
- **backend.py:** Contains the legal database, Gemini API functions, and logic for finding legal cases.
- **frontend.py:** Designs the user interface.

This modular design makes it easy to understand and modify each part of the application.
