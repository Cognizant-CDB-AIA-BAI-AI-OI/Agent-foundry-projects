# 📦 Import necessary functions and inputs
from utils import setup_env_and_llm                         # Initializes environment and language model
from pdf_qa import pdf_text_extraction, pdf_query          # Functions for extracting text and querying PDFs
from inputs import model, pdf_path, user_input             # Inputs: model choice, PDF file path, and user query

# ⚙️ Set up the client and generation config
client, generate_content_config = setup_env_and_llm()

# 📄 Extract text content from the specified PDF
context = pdf_text_extraction(pdf_path)

# 🤖 Query the language model with extracted content and user's question
response = pdf_query(
    context,
    user_input,
    client,
    generate_content_config,
    model
)

# 🖨️ Display the generated response
print(f"\nResponse:\n{response}")
