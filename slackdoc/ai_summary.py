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
    "You are an expert information architect. Your job is to read this document and create a summary that captures its complete essence "
    "while being genuinely easy and quick to understand.\n\n"
    
    "THINK FIRST:\n"
    "1. What type of document is this? (meeting notes, project spec, process guide, etc.)\n"
    "2. What are the 2-3 most important things someone needs to know from this document?\n"
    "3. What's the best way to organize this specific content for maximum clarity?\n"
    "4. What details can I skip without losing the core message?\n\n"
    
    "GUIDELINES FOR YOUR SUMMARY:\n"
    "• Write in a natural, conversational tone - like explaining to a colleague over coffee\n"
    "• Lead with what matters most to the reader\n"
    "• Use the document's own language and terminology (don't over-simplify technical terms)\n"
    "• Include specific details that affect people's work or decisions\n"
    "• Group related information together logically\n"
    "• Keep it under 250 words total\n"
    "• Make it feel complete - someone should understand the full picture without reading the original\n\n"
    
    "STRUCTURE FLEXIBLY:\n"
    "Choose the organization that makes most sense for THIS specific document. You might use:\n"
    "• A brief overview paragraph + key highlights\n"
    "• Timeline format for process or project docs\n"
    "• Problem → Solution → Next Steps for decision docs\n"
    "• Main topic + supporting details for informational docs\n"
    "• Or any other logical flow that serves the content\n\n"
    
    "WHAT TO EMPHASIZE:\n"
    "- Decisions that were made\n"
    "- Actions people need to take\n"
    "- Deadlines and important dates\n"
    "- Changes from previous plans or decisions\n"
    "- Key insights or conclusions\n"
    "- Dependencies or blockers\n\n"
    
    "Remember: Your goal is to save people time while ensuring they're fully informed. "
    "Make it so clear and complete that they won't need to open the original document unless they want deeper details.\n\n"
    
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