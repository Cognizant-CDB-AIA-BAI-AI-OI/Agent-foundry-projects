from google import genai

from pydantic import BaseModel, Field
from pathlib import Path
import os
from langchain_google_vertexai import VertexAI
import vertexai
from google.cloud import vision
from google.cloud import storage
from typing import List, Optional
import json
import time

import PyPDF2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/home/ubuntu/sush/cotality/agent_demo/gbg-project-gravity-939f963ab952.json'
vertexai.init(
        project="gbg-project-gravity",
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com"
    )


storage_client=storage.Client()
bucket_name = 'cotality_poc'
bucket = storage_client.bucket("cotality_poc")


vision_client=vision.ImageAnnotatorClient()
llm = VertexAI(model_name="gemini-2.5-flash-preview-04-17")

# project_id = "cdb-aia-ops-000305776"
# region = "us-central1"
# credentials_path = os.path.join(BASE_DIR, 'cred/cdb-aia-ops-Palm 4.json')
# model_id = 'gemini-2.5-pro'
    
# client = genai.Client(
#         vertexai=True,
#         project=project_id,
#         location=region,
#     )

class Document_Input(BaseModel):
    document_name: Optional[str] = Field("2072068.pdf" , description="The name of the input PDF document")

def read_pdf_doc(document_name : Document_Input) -> str:
    
    # Build the file path
    file_path = '/home/ubuntu/sush/cotality/agent_demo/documents/2072068.pdf'

    if not file_path.exists():
        raise FileNotFoundError(f"Document not found at {file_path}")
    
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            print(text)

    # Generate content with Gemini model
    # response = client.models.generate_content(
    #     model=model_id,
    #     contents=[
    #         types.Part.from_bytes(
    #             data=file_path.read_bytes(),
    #             mime_type='application/pdf',
    #         ),
    #         self.__prompt
    #     ],
    #     config={
    #         "response_mime_type": "application/json",
    #         "response_schema": PropertyInfo,
    #     },
    # )

def read_pdf_doc2(document_name : Document_Input) -> str:
    try:
        # Build the file path
        file_path = f'/home/ubuntu/sush/cotality/agent_demo/documents/{document_name}'
        # if not file_path.exists():
        #     raise FileNotFoundError(f"Document not found at {file_path}")
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("cotality_poc")
        blob = bucket.blob(document_name)
        blob.upload_from_filename(file_path)
        print(f"File {file_path} uploaded to {document_name}.")
        
        try:
            client = vision.ImageAnnotatorClient()
            gcp_file_path=f"gs://{bucket.name}/{document_name}"
            feature = vision.Feature(
                        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION
                    )
            input_config = vision.InputConfig(
                    gcs_source=vision.GcsSource(uri=gcp_file_path),
                    mime_type='application/pdf'
                )
            output_uri = f"gs://{bucket.name}/extracted_data_from_pdf/{document_name.strip('.pdf')}/"
            output_config = vision.OutputConfig(
                    gcs_destination=vision.GcsDestination(uri=output_uri),
                    batch_size=1
                )
            async_request = vision.AsyncAnnotateFileRequest(
                    features=[feature],
                    input_config=input_config,
                    output_config=output_config
                )
            operation = client.async_batch_annotate_files(
                    requests=[async_request]
                )
            print("Processing PDF Text Extraction")
            operation.result(timeout=420)
            time.sleep(5)
            print("Operation Completed")

            blob_list = list(bucket.list_blobs(prefix=f"extracted_data_from_pdf/{document_name.strip('.pdf')}"))
            text_data = ""
            for blob in blob_list:
                if not blob.name.endswith(".json"):
                    continue
                print(f"Processing output file: {blob.name}")
                json_string = blob.download_as_string()
                response = vision.AnnotateFileResponse.from_json(json_string)
                for page_response in response.responses:
                    if page_response.full_text_annotation:
                        text_data += page_response.full_text_annotation.text + "\n"
                # Clean up the output file
                blob.delete()
            with open(f"document_text/{document_name.rstrip('.pdf')}.txt", 'w', encoding='utf-8') as file:
                file.write(text_data)

            return text_data
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

