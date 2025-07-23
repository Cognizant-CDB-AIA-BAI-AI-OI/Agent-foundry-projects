model="gemini-2.5-flash"

# pdf_path = r"C:\Users\2403778\OneDrive - Cognizant\Desktop\CTS Usecases\PDF-QA\sample_pdfs\2072068.pdf"
# pdf_path = r"C:\Users\2403778\OneDrive - Cognizant\Desktop\CTS Usecases\PDF-QA\sample_pdfs\9871234.pdf"

# user_input = "Give me 5 bullet points about this document."
user_input = """You are an expert data-extraction assistant for real-estate documents.  
Always respond with only valid JSON—no markdown, no commentary.
 
TASK
 
Extract the following information *STRICTLY* from the provided document:
 
1. Every property's
   • "address_number" - extract only the numeric house or building number
   • "address_unit" - extract only the unit identifier (like Unit A, Apt B) if present
   • "direction" - extract only the cardinal direction (N, S, E, W, NE, NW, SE, SW) if present
   • "street_name" - extract only the street name (exclude house number, directional prefixes, city, state)
   • "city" - extract only the city name without any additional words like "City of" or "County"
   • "county" - extract only the county name without the word "County" or other qualifiers
   • "building" - extract only the building name if present
   • "suite" - extract only the suite number/letter if present
   • "zip_code" - extract only the 5-digit or 9-digit ZIP code if present
   • "account_type" - extract the type of account (e.g., "Residential", "Commercial") if present
   • "owner" - extract the property owner's name if present
 
2. Tax identifiers (tax ID / parcel ID) that:
   • Are EXPLICITLY labeled with terms such as "Tax ID", "Tax #", "Tax No.", "Parcel ID", "Parcel #", "Parcel No." (case-insensitive)
   • Have the format typical of tax/parcel identifiers (alphanumeric with possible dashes or periods)
   • Appear in the context of property information, not in other contexts
   • Do not extract random numbers or figures that aren't clearly identified as tax/parcel IDs
 
OUTPUT
 
Return one JSON object with these keys:
  • "properties" - array of objects containing "address_unit", "address_number", "direction", "street_name", "city", "county", "building", "suite", "zip_code", "account_type", "account_number", "owner"
  • "tax_ids" - array of all tax-ID strings, in order of first appearance. If no valid tax IDs are found, return an empty array.
 
RULES
• Clean all extracted fields to contain only the relevant information:
  - For "county": remove the word "County" and any trailing spaces/punctuation (e.g., "Dallas County" → "Dallas")
  - For "city": remove phrases like "City of" and ensure only the name is returned
  - For "street_name": remove any directional prefixes and house numbers
• Detect U.S. addresses; accept variations like "St." vs "Street", line breaks, missing ZIP
• For tax IDs: Only extract numbers that are EXPLICITLY labeled as tax or parcel identifiers
• When in doubt about whether something is a tax ID, do NOT include it
• Deduplicate identical property entries
• Include each tax ID once; preserve order of appearance
• Output strict, well-formed JSON—no extra keys, no markdown, no comments
• Use null for any fields that cannot be extracted
• Do not include the document text in your response
• Avoid false positives: do not extract information that is not clearly present in the document"""


response_type = "application/json"

response_schema = {
    "type": "OBJECT",
    "properties": {
        "properties": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "account_type": {"type": "STRING"},
                    "address_number": {"type": "STRING"},
                    "address_unit": {"type": "STRING"},
                    "building": {"type": "STRING"},
                    "city": {"type": "STRING"},
                    "county": {"type": "STRING"},
                    "direction": {"type": "STRING"},
                    "owner": {"type": "STRING"},
                    "street_name": {"type": "STRING"},
                    "suite": {"type": "STRING"},
                    "zip_code": {"type": "STRING"}
                },
                "required": [
                    "account_type",
                    "address_number",
                    "address_unit",
                    "building",
                    "city",
                    "county",
                    "direction",
                    "owner",
                    "street_name",
                    "suite",
                    "zip_code"
                ]
            }
        },
        "tax_ids": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        }
    },
    "required": ["properties", "tax_ids"]
}
