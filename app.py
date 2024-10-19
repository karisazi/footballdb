import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv() # load all environment variables from .env
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def get_gemini_reponse(file, info_prompt, output):
    input_prompt = f'''
    You are an expert in understanding football match report. 
    You will receive input pdf as football match report and you will answer question
    based on the input pdf file.
    You should return {output}
    '''
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(file)
    # response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
    response = model.generate_content([input_prompt, sample_pdf, info_prompt])
    print(response.text)
    


#case 22
# info_input = "championship"  
# output = 'output just the value of the input'

#case 2
info_input = 'player names'
output = 'output as player names in list with its team as the key'

get_gemini_reponse('docs.pdf', info_input, output)
