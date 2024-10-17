import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() # load all environment variables from .env
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def get_gemini_reponse(input, file, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(file)
    # response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
    response = model.generate_content([input, sample_pdf, prompt])
    print(response.text)
    

input_prompt = '''
    You are an expert in understanding football match report. 
    You will receive input pdf as football match report and you will answer question
    based on the input pdf file.
'''

input = "game score"

get_gemini_reponse(input_prompt, 'docs.pdf', input)
