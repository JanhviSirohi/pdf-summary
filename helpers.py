import re, os, time

import fitz
import openai
from dotenv import load_dotenv

load_dotenv()

def type_text(container, text):
    placeholder = container.empty()

    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.write(typed_text, unsafe_allow_html=True)
        time.sleep(0.005)

def extract_text_from_pdf(pdf_file) -> str:
    pdf = fitz.open(pdf_file)
    text = "Input: "
    
    for page in pdf:
        page_text = page.get_text("text")
        text += page_text + "\n"

    pdf.close()
    return text

def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def generate_summary(prompt, stop=['<<END>>']):
    retry = 0
    while retry <= 5:
        try:
            response = openai.Completion.create(
                prompt=prompt,
                engine=os.getenv("GPT3_ENGINE"),
                temperature=float(os.getenv("GPT3_TEMP")),
                max_tokens=int(os.getenv("GPT3_TOKENS")),
                top_p=float(os.getenv("GPT3_TOP_P")),
                frequency_penalty=float(os.getenv("GPT3_FREQ_PEN")),
                presence_penalty=float(os.getenv("GPT3_PRES_PEN")),
                stop=stop
            )
            text = response.choices[0].text.strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            print('Error communicating with OpenAI:', str(oops))
            time.sleep(1)
    
    else:
        return 'GPT3 error:'