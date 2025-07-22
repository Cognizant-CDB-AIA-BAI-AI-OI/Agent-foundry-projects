from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from pathlib import Path
import os
import vertexai
from typing import Optional
from langchain.prompts import PromptTemplate
import json
import requests

class PropertyInfo(BaseModel):
    """Individual property information"""
    summary: Optional[str] = Field(None, description="Comprehensive summary of property, transaction, and taxation information with important details quoted using backticks")
    account_number: Optional[str] = Field(None, description="The account number of the property")
    address: Optional[str] = Field(None, description="Full mailing address of the property owner")
    property_site_address: Optional[str] = Field(None, description="Physical address of the property")
    legal_description: Optional[str] = Field(None, description="Legal description of the property")
    current_tax_levy: Optional[str] = Field(None, description="Current tax levy amount")
    current_amount_due: Optional[str] = Field(None, description="Current amount due for taxes")
    prior_year_amount_due: Optional[str] = Field(None, description="Amount due from prior years")
    total_amount_due: Optional[str] = Field(None, description="Total amount due")
    market_value: Optional[str] = Field(None, description="Market value of the property")
    land_value: Optional[str] = Field(None, description="Value of the land")
    improvement_value: Optional[str] = Field(None, description="Value of improvements on the property")
    capped_value: Optional[str] = Field(None, description="Capped value of the property")
    agricultural_value: Optional[str] = Field(None, description="Agricultural value of the property")
    exemptions: Optional[str] = Field(None, description="Property tax exemptions")

class PropertyWebScraper:
    """Class to scrape property information from a designated web page"""

    def __init__(self, credentials_path='cred/cdb-aia-ops-Palm 4.json', project_id="cdb-aia-ops-000305776", region="us-central1", model_id='gemini-2.5-pro'):
        self.project_id = project_id
        self.region = region
        self.credentials_path = credentials_path
        self.model_id = model_id

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
        vertexai.init(project=self.project_id, location=self.region)

        self.client = genai.Client(vertexai=True, project=self.project_id, location=self.region)

        self.__prompt_template = """Please analyze the following HTML content from a property information webpage and:

{url_html}

Extract property data and format it as JSON with the following structure:

```json
{{
    "Summary": "",
    "Account Number": "",
    "Address": "",
    "Property Site Address": "",
    "Legal Description": "",
    "Current Tax Levy": "",
    "Current Amount Due": "",
    "Prior Year Amount Due": "",
    "Total Amount Due": "",
    "Market Value": "",
    "Land Value": "",
    "Improvement Value": "",
    "Capped Value": "",
    "Agricultural Value": "",
    "Exemptions": ""
}}

For all monetary values, extract only the numeric amount without dollar signs ($) or other currency symbols. For example, if the HTML shows "$1,234.56", just include "1234.56" in the JSON.

In the 'Summary' field, provide a comprehensive overview that includes ALL relevant information found in the HTML content, not just the data that maps to the specified JSON keys. The summary should include:

1. All property details (owner information, location, size, type, etc.)
2. Complete financial and valuation information (all assessments, values, and appraisals)
3. Full taxation details (current and past taxes, payment status, due dates, etc.)
4. Any transaction history or ownership changes
5. All exemptions, special classifications, or tax benefits
6. Any additional information present in the HTML that might be relevant to understand the property

Highlight important information by enclosing it in backticks (`). Important information includes specific values, dates, statuses, property characteristics, tax amounts, deadlines, or any other key details that would be most relevant to understanding the property's complete profile."""

    def set_url_to_scrape(self, url):
        html_response = requests.get(url).text
        if html_response:
            prompt_template = PromptTemplate.from_template(self.__prompt_template)
            self.__prompt = prompt_template.invoke({'url_html': html_response})
        else:
            raise Exception(f"Unable to fetch HTML details from URL: [{url}]")

    def scrape_property_info(self):
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=self.__prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": list[PropertyInfo],
            },
        )
        return json.loads(response.text)


if __name__ == "__main__":
    url = "https://www.dallasact.com/act_webdev/dallas/showdetail2.jsp?can=325510000003R0000&ownerno=0"
    scraper = PropertyWebScraper()
    scraper.set_url_to_scrape(url)
    #scraper.load_url(url)
 
    property_data = scraper.scrape_property_info()
    print(json.dumps(property_data, indent=2))
