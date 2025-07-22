import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SERVICE_ACCOUNT_FILE = r'/Users/happyfox/Documents/HappyFox/Google-doc-summ/Google-docs-summary/slackdoc/credentials.json'  # Place your downloaded JSON in the project root or update the path

def extract_doc_id(doc_url):
    """
    Extracts the document ID from a Google Docs URL.
    """
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', doc_url)
    return match.group(1) if match else None

def get_docs_service():
    """
    Authenticates and returns a Google Docs API service instance.
    """
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('docs', 'v1', credentials=creds)

def get_doc_content(doc_url):
    """
    Given a Google Docs URL, returns the full text content of the document.
    """
    doc_id = extract_doc_id(doc_url)
    print(f"Extracted Document ID: {doc_id}")
    if not doc_id:
        return None
    service = get_docs_service()
    print(f"Service created: {service}")
    doc = service.documents().get(documentId=doc_id).execute()
    content = []
    for element in doc.get('body', {}).get('content', []):
        if 'paragraph' in element:
            for elem in element['paragraph'].get('elements', []):
                text_run = elem.get('textRun')
                if text_run:
                    content.append(text_run.get('content', ''))
    return ''.join(content)