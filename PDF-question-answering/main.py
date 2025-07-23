# 📦 Import necessary functions
from utils import setup_env_and_llm                        # Initializes environment and language model
from pdf_qa import pdf_text_extraction, pdf_query          # Functions for extracting text and querying PDFs
from inputs import model, user_input                       # Inputs: model choice, and user query


# ✍️ Input: PDF file path
pdf_path = r"sample_pdfs\test.pdf" # Replace with your PDF file path


# ⚙️ STEP 1: Set up the env & llm
client, generate_content_config = setup_env_and_llm()

# 📄 STEP 2: Extract text content from the specified PDF
context = pdf_text_extraction(pdf_path)

# 🤖 STEP 3: Ask the AI to answer the question using the PDF content
response = pdf_query(
    context,
    user_input,
    client,
    generate_content_config,
    model
)

# 🖨️ Display the generated response
print(f"\nResponse:\n{response}")
