from utils import (
    get_llm_response,
    extract_text_from_scanned_pdf,
    extract_text_and_check_strict_natural
)

def pdf_text_extraction(pdf_path):
    context, all_pages_have_text = extract_text_and_check_strict_natural(pdf_path=pdf_path)

    if all_pages_have_text == False:
        print("📸 This appears to be a scanned PDF with image-based content.")
        context = extract_text_from_scanned_pdf(document_path=pdf_path)
    elif all_pages_have_text == True:
        print("📸 This appears to be a natural PDF.")

    return context


def pdf_query(
        context, prompt, 
        client, generate_content_config, model
    ):
    prompt = f"""PDF Context:\n{context}\n\n{prompt}"""
    
    try:
        response, _ = get_llm_response(
            client=client,
            generate_content_config=generate_content_config,
            usr_prompt=prompt,
            contents=[],
            model=model
        )
    except Exception as err:
        print(f"Error in generating response: {err}")
    return response
