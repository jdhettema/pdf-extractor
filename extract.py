import json
from PyPDF2 import PdfReader
import requests

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_purchase_order_data(file_path):
    text = extract_text_from_pdf(file_path)

    prompt = f"""
    
    You are tasked with extracting information from a provided purchase order PDF and converting it into a structured JSON format. The JSON should match the column headings of a Google Sheet. Some columns may not be filled out using the PDF and should be left blank. If the purchase order contains multiple items, each item should be represented as a separate object in the JSON array.

    Instructions:

    Extract Information:

    Extract the following details from the PDF:
    PO #
    Job #
    Description
    Qty
    Shipped to
    Date Online
    Common Name
    Qty Rec Warehouse
    Date Rec Warehouse
    Qty Rec Job Site
    Date Rec Job Site
    Format the JSON:

    Create a JSON object for each item listed in the purchase order.
    Ensure each object follows the structure below:
    Copy
    [
        {
            "PO #": "",
            "Job #": "",
            "Description": "",
            "Qty": "",
            "Shipped to": "",
            "Date Online": "",
            "Common Name": "",
            "Qty Rec Warehouse": "",
            "Date Rec Warehouse": "",
            "Qty Rec Job Site": "",
            "Date Rec Job Site": ""
        }
    ]
    Handle Missing Information:

    If any of the fields cannot be filled out using the PDF, leave them as empty strings.
    Example Output:

    For a purchase order with multiple items, the output should look like this:
    Copy
    [
        {
            "PO #": 1686,
            "Job #": 1311,
            "Description": "1\" PVC",
            "Qty": 100,
            "Shipped to": "WILL CALL",
            "Date Online": "",
            "Common Name": "",
            "Qty Rec Warehouse": "",
            "Date Rec Warehouse": "",
            "Qty Rec Job Site": "",
            "Date Rec Job Site": ""
        },
        {
            "PO #": 1686,
            "Job #": 1311,
            "Description": "4\" PVC 90 W/36\" RADIUS SWEEP",
            "Qty": 2,
            "Shipped to": "WILL CALL",
            "Date Online": "",
            "Common Name": "",
            "Qty Rec Warehouse": "",
            "Date Rec Warehouse": "",
            "Qty Rec Job Site": "",
            "Date Rec Job Site": ""
        }
    ]
    Note: Ensure that each item in the purchase order is represented as a separate object in the JSON array.

    PDF TEXT:
    {text}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    content = response.json()['response']

    json_text = content.split('```json')[-1].split('```')[0].strip() if '```json' in content else content
    return json.loads(json_text)