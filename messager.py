import os
from dotenv import load_dotenv
import os
import google.generativeai as genai
class messageManager():
    def __init__(self):
        self.messages = []
        load_dotenv()
        API_KEY = os.getenv("API_KEY")

        genai.configure(api_key=API_KEY)

        # The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.chat = self.model.start_chat(history=[])

    def generate_response(self, prompt):
        result = self.chat.send_message(prompt)
        return result.text