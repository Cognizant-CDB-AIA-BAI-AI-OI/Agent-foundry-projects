from google.cloud import vision_v1 as vision
import fitz  # PyMuPDF

def extract_text_from_scanned_pdf(document_path: str) -> str:
    try:
        vision_client = vision.ImageAnnotatorClient()
        doc = fitz.open(document_path)
        full_text = ""

        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            pix = page.get_pixmap()
            image_bytes = pix.tobytes("png")

            image = vision.Image(content=image_bytes)
            response = vision_client.document_text_detection(image=image)

            if response.error.message:
                print(f"Error on page {page_index}: {response.error.message}")
                continue

            if response.full_text_annotation:
                full_text += response.full_text_annotation.text + "\n"

        return full_text

    except Exception as e:
        print(f"Exception occurred: {e}")
        return ""
