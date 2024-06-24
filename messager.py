import os
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from bs4 import BeautifulSoup
import requests
class messageManager():
    def __init__(self):
        self.messages = []
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        genai.configure(api_key=API_KEY)

        try:
            vertexai.init(project="6689802496", location="europe-west4")
            model = GenerativeModel(
                "projects/6689802496/locations/europe-west4/endpoints/9007388370740969472",
            )
            self.chat = model.start_chat()
        except Exception as e:
            print(e)
            print("Model not found, using default")
        #self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt):
        prompt = self.replace_urls(prompt)
        print('**************')
        print(prompt)
        print('**************')
        try:
            result = self.chat.send_message(prompt)
            return result.text
        except Exception as e:
            print(e)
        
    
    def replace_urls(self, text):
        #check if text is url
        print(text)
        expression = r"(?:https?):\/\/(?:www\.)?(?:[^\/?]+)(?:[a-zA-Z0-9\/\?=\-_\.]*)"
        url = re.findall(expression, text, re.MULTILINE)
        
        if(len(url)>0):
            try: 
                r = requests.get(url[0]) 
                r.raise_for_status() 
            except requests.exceptions.HTTPError as errh: 
                print("HTTP Error") 
                print(errh.args[0])
                return text
            except requests.exceptions.ReadTimeout as errrt: 
                print("Time out") 
                return text
            except requests.exceptions.ConnectionError as conerr: 
                print("Connection error") 
                return text

            soup = BeautifulSoup(r.content, 'html.parser')
            returntext = soup.get_text()
            while(returntext.find('\n') != -1):
                returntext = returntext.replace('\n', '\t')
            while(returntext.find('\t\t') != -1):
                returntext = returntext.replace('\t\t', '\t')
            returntext = "<website>"+returntext+"</website>"
            res = text.replace(url[0],returntext)
            return res
        else:
            return text
        
if __name__ == "__main__":
    #testing
    m = messageManager()
    text = "https://streetkitchen.hu/pekseg/hazi-sajtos-ropi/"
    print(m.generate_response(text))