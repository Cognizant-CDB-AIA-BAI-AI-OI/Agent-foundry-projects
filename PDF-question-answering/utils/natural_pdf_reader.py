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