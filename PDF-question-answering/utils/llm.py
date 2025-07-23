from typing import Optional, List
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv


def set_env():
    # 🌱 Load environment variables
    load_dotenv()
    google_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")

    # Setting default credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_creds

    return project, location


def llm_setup(project: str, location: str) -> genai.Client:
    """Initializes and returns the GenAI client with Vertex AI."""
    try:
        return genai.Client(vertexai=True, project=project, location=location)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize GenAI client: {e}") from e


def llm_config_setup(
    sys_prompt: Optional[str] = None,
    temperature: float = 0.7,
    seed: int = 0,
    max_output_tokens: int = 65535
) -> types.GenerateContentConfig:
    """Creates and returns a GenerateContentConfig object with safety and system settings."""
    config_dict = {
        "temperature": temperature,
        "seed": seed,
        "max_output_tokens": max_output_tokens,
        "safety_settings": [
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        "thinking_config": types.ThinkingConfig(thinking_budget=-1),
    }

    if sys_prompt:
        config_dict["system_instruction"] = [types.Part.from_text(text=sys_prompt)]

    return types.GenerateContentConfig(**config_dict)


def setup_env_and_llm():
    project, location = set_env()
    client = llm_setup(project, location)
    generate_content_config = llm_config_setup()
    return client, generate_content_config


def get_llm_response(
    client: genai.Client,
    generate_content_config: types.GenerateContentConfig,
    usr_prompt: str,
    contents: List,
    model: str = "gemini-2.5-flash"
) -> tuple[str, List[types.Content]]:
    """
    Generates a response from the LLM using the given context and prompt.

    Returns:
        response_text (str): The model's response.
        updated_contents (List[types.Content]): Updated conversation history.
    """
    if not usr_prompt.strip():
        raise ValueError("User prompt must not be empty.")

    # Append new user message to conversation history
    contents.append(types.Content(role="user", parts=[types.Part.from_text(text=usr_prompt)]))

    try:
        raw_response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config
        )
        response_text = raw_response.candidates[0].content.parts[0].text

        contents.append(types.Content(role="model", parts=[types.Part.from_text(text=response_text)]))
        
        return response_text, contents
    except Exception as e:
        raise RuntimeError(f"Failed to generate LLM response: {e}") from e
