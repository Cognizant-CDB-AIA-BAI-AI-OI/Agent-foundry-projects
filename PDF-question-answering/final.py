import os
import fitz  # PyMuPDF
import base64
from dotenv import load_dotenv
import streamlit as st
from llm import llm_setup, llm_config_setup, get_llm_response, pdf_to_text_using_vision_llm
from read_pdf_agent import read_pdf_doc2
import tempfile
from pathlib import Path

BASE_DIR = r"/home/ubuntu/sush/cotality/agent_demo"


# 🌱 Load environment variables
load_dotenv()
google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project = os.getenv("PROJECT_ID")
location = os.getenv("LOCATION")

if not all([google_creds, project, location]):
    st.error("❌ Missing environment variables. Check your .env file.")
    st.stop()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds

# 🧠 Setup LLM client and config once
if "client" not in st.session_state:
    st.session_state.client = llm_setup(project, location)

if "generate_content_config" not in st.session_state:
    st.session_state.generate_content_config = llm_config_setup()


# def extract_text_and_check_strict_natural(pdf_stream) -> tuple[str, bool]:
#     """
#     Extracts text and checks whether every page contains selectable text.

#     Returns:
#         - Full extracted text (str)
#         - Boolean: True if all pages have text, False otherwise
#     """
#     try:
#         doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")
#         full_text = ""
#         all_pages_have_text = True

#         for page in doc:
#             text = page.get_text().strip()
#             full_text += text

#             if not text:
#                 all_pages_have_text = False  # Found a empty page

#         return full_text, all_pages_have_text
#     except Exception as e:
#         return f"Error reading PDF: {e}", False

import fitz  # PyMuPDF

def extract_text_and_check_strict_natural(pdf_path: str) -> tuple[str, bool]:
    """
    Extracts text from a PDF file and checks whether every page contains selectable text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        tuple:
            - Full extracted text (str)
            - Boolean: True if all pages have text, False otherwise
    """
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        all_pages_have_text = True

        for page in doc:
            text = page.get_text().strip()
            full_text += text

            if not text:
                all_pages_have_text = False  # Found an empty page

        return full_text, all_pages_have_text
    except Exception as e:
        return f"Error reading PDF: {e}", False




# --- Interface ---
st.title("📚 PDF Chatbot")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])


if uploaded_file:
    
    save_path = Path(os.path.join(BASE_DIR,f'documents/{uploaded_file.name}'))
    # Save the uploaded file to the specified path
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    #read_pdf_doc2(uploaded_file.name)

    print("Uploaded the file")



# if uploaded_file:
    print("Inside uploaded file")
    # context, all_pages_have_text = extract_text_and_check_strict_natural(uploaded_file)
    context, all_pages_have_text = extract_text_and_check_strict_natural(save_path)
    print(context)
    # all_pages_have_text = False
    if all_pages_have_text == False:
        st.warning("📸 This appears to be a scanned PDF with image-based content.")

        context = read_pdf_doc2(uploaded_file.name)
        st.text_area("Context", context, height=300)

    elif all_pages_have_text == True:
        st.text_area("Context", context, height=300)
        st.success("✅ PDF content loaded!")

    st.text_input("Ask a question about the PDF:", key="user_input")

    if st.session_state.user_input:
        prompt = f"""PDF Context:\n{context}\n\nUser Question:\n{st.session_state.user_input}"""
        
        try:
            print("Backend 2")
            response, _ = get_llm_response(
                client=st.session_state.client,
                generate_content_config=st.session_state.generate_content_config,
                usr_prompt=prompt,
                contents=[],
                model="gemini-2.5-flash"
            )
            st.markdown("### 💬 Chatbot Response")
            st.write(response)

        except Exception as err:
            st.error(f"Error generating response: {err}")

    # else: # all_pages_have_text == False:
    #     st.warning("📸 This appears to be a scanned PDF with image-based content.")

    #     text_data = read_pdf_doc2(uploaded_file.name)
    #     st.text_area("Context", text_data, height=300)
        
        