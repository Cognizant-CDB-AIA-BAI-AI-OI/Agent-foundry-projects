# 📄 PDF Question Answering

This project enables intelligent querying of PDF documents—both **natural text** and **scanned PDFs**—using a language model and vision model support when needed.

---

* ## 🛠️ Prerequisites

    Ensure the following setup steps are completed before running the script:

    - Place your **Google Cloud Application Credentials** (`.json` file) into the project directory.
    
    - Create a `.env` file with the following keys:
        ```env
        GOOGLE_APPLICATION_CREDENTIALS=your_credentials.json
        PROJECT_ID=your_project_id
        LOCATION=your_location
        ```
    
    - Install required packages using:
        ```bash
        pip install -r requirements.txt
        ```

* ## 🚀 Run the script

    - Before running, ensure the following in `main.py`:
        ```python
        pdf_path = "path/to/document.pdf"
        ```
    
    - Run the main script with:
        ```bash
        python main.py
        ```

* ## 🌐 FastAPI Endpoint

    You can also use this project via an HTTP API powered by FastAPI.
    
    - ▶️ Start the server
        ```bash
        python fast_api_app.py
        ```

    - 📮 Testing
        - Once the server is running, visit: `http://localhost:8000/docs`
        - Upload your PDF file via the POST /query-pdf endpoint, then click "Execute" to view the response.
      
