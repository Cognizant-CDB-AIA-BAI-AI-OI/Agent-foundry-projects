# 📄 PDF Question Answering

This project enables intelligent querying of PDF documents—both **natural text** and **scanned PDFs**—using a language model and vision model support when needed.

---

* ## 🛠️ Prerequisites

Ensure the following setup steps are completed before running the script:

### ✅ STEP 1: Place Credentials file
Place your **Google Cloud Application Credentials** (`.json` file) into the project directory.

### ✅ STEP 2: Environment Variables
Create a `.env` file with the following keys:
```env
GOOGLE_APPLICATION_CREDENTIALS=your_credentials.json
PROJECT_ID=your_project_id
LOCATION=your_location
```

### ✅ STEP 3: Install Dependencies
Install required packages using:
```bash
pip install -r requirements.txt
```

* ## 🚀 How to Run

    - Before running, ensure the following in `inputs\input_variables.py`:
        ```python
        model = "gemini-2.5-flash"  # or your preferred model from Vertex AI
        pdf_path = "path/to/document.pdf"
        user_input = "Your question here"
        ```
    
    - Run the main script with:
        ```bash
        python main.py
        ```
