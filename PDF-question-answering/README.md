# 📄 PDF Question Answering

This project enables intelligent querying of PDF documents—both **natural text** and **scanned PDFs**—using a language model and vision model support when needed.

---

* ## 🛠️ Prerequisites

    Ensure the following setup steps are completed before running the script:
    
    1. Place your **Google Cloud Application Credentials** (`.json` file) into the project directory.
    
    3. Create a `.env` file with the following keys:
        ```env
        GOOGLE_APPLICATION_CREDENTIALS=your_credentials.json
        PROJECT_ID=your_project_id
        LOCATION=your_location
        ```
    
    5. Install required packages using:
        ```bash
        pip install -r requirements.txt
        ```

* ## 🚀 Run the script

    - Before running, ensure the following in `main.py`:
        ```python
        model = "gemini-2.5-flash"  # or your preferred model from Vertex AI
        pdf_path = "path/to/document.pdf"
        user_input = "Your question here"
        ```
    
    - Run the main script with:
        ```bash
        python main.py
        ```
