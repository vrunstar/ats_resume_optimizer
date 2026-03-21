import google.generativeai as genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL
    
def config_gemini():
    genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    config_gemini()
    return genai.GenerativeModel(GEMINI_MODEL)