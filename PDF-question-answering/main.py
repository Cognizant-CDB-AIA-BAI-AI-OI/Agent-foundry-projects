# 📦 Import necessary functions
from utils import setup_env_and_llm                         # Initializes environment and language model
from pdf_qa import pdf_text_extraction, pdf_query          # Functions for extracting text and querying PDFs


# ✍️ Inputs: model choice, PDF file path, and user query
model="gemini-2.5-flash"
pdf_path = "sample_pdfs\2072068.pdf" # Replace with your PDF file path
user_input = "Give me 5 bullet points about this document."


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
