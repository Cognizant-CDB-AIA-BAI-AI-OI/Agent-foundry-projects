# app.py

import streamlit as st
from utils import setup_env_and_llm
from pdf_qa import pdf_text_extraction, pdf_query

# 🖼️ App title
st.title("📄 PDF Question Answering with AI")

# 🔽 Model selection dropdown
model = st.selectbox(
    "Select Model",
    options=[
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-lite-001"
    ],
    index=0
)

# 📎 Upload PDF file
pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])

if pdf_file:
    with st.spinner("Processing your document..."):
        # Save uploaded PDF temporarily
        temp_path = f"temp_{pdf_file.name}"
        with open(temp_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        # STEP 1: Setup client and config
        client, generate_content_config = setup_env_and_llm()

        # STEP 2: Extract text from PDF
        context = pdf_text_extraction(temp_path)

        # 📝 Display extracted context
        st.subheader("📃 Extracted PDF Content:")
        st.text_area("Context", context, height=300)


# 💬 Enter user question
question = st.text_area("Enter your question:", value="Give me 5 bullet points about this document.")


# 🚀 Run logic when PDF and question are provided
if st.button("Get Answer") and pdf_file and question:
        # STEP 3: Ask the AI to answer the question
        response = pdf_query(
            context,
            question,
            client,
            generate_content_config,
            model
        )

        # 🖨️ Show result
        st.subheader("🔍 AI Answer:")
        st.write(response)
else:
    st.info("📎 Upload a PDF and enter your question to begin.")
