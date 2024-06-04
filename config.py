import os
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions

load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Gemini API Configuration
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta2/"
client_options = ClientOptions(api_endpoint=GEMINI_API_ENDPOINT) 

# Available Gemini Models (using only Gemini-1.5-Flash)
GEMINI_MODELS = {
    "gemini-1.5-flash": "models/gemini-1.5-flash",  
}

# Available Analysis Features
ANALYSIS_FEATURES = ["sentiment", "entities", "intents", "topics", "summary", "translation"]
