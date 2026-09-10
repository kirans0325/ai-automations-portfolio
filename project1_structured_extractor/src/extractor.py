import os
from typing import Optional
from dotenv import load_dotenv
from src.models import SupportTicketAnalysis
from src.mock_llm import mock_extract_ticket_data

# Load .env file if available
load_dotenv()


def extract_structured_ticket(raw_text: str, force_mock: bool = False) -> SupportTicketAnalysis:
    """Core extraction function that converts unstructured customer text into a validated Pydantic model.

    Args:
        raw_text: Unstructured ticket text.
        force_mock: If True, bypasses API calls and uses local offline mock parser.

    Returns:
        SupportTicketAnalysis: Validated Pydantic object.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if force_mock or not api_key:
        # Run local offline mode
        return mock_extract_ticket_data(raw_text)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert AI support triage assistant. 
Extract structured information from the following customer ticket text according to the requested JSON schema.

TICKET TEXT:
{raw_text}
"""

        # Pass Pydantic class directly to response_schema for guaranteed structured output!
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SupportTicketAnalysis,
                temperature=0.1
            ),
        )

        # Parse JSON output into Pydantic model
        result = SupportTicketAnalysis.model_validate_json(response.text)
        return result

    except Exception as e:
        print(f"[Warning] Live API call failed ({e}). Falling back to Offline Mock Engine.")
        return mock_extract_ticket_data(raw_text)
