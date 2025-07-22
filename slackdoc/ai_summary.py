from google import genai
from .gdocs_utils import get_doc_content
from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()

def generate_summary(doc_url):
    """
    Fetches the content of a Google Doc and generates a project-focused summary using Gemini.
    """
    print('got into generate_summary')
    doc_content = get_doc_content(doc_url)
    print(doc_content)
    if not doc_content:
        return "❌ Could not retrieve the document content. Please check the link and permissions."

    prompt = (
        "You are an expert project manager. Given the following Google Docs content, extract and summarize all important information, "
        "including deadlines, key points, action items, decisions, and anything that should be remembered or followed up. "
        "If the document contains project milestones, deliverables, or important dates, highlight them clearly. "
        "If there are any instructions, warnings, or special notes, include them in the summary. Be concise but thorough.\n\n"
        "Document content:\n"
        f'"""\n{doc_content}\n"""'
    )
    print('got doc content')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    print("got gemini api key")
    genai.configure(api_key=GEMINI_API_KEY)
    print('Configured Gemini API with provided key.')
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    response = model.generate_content(prompt)
    print('Generated response from Gemini model.')
    return response.text