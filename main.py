import os, uuid, textwrap

import openai
import streamlit as st

from style import HIDE_ELEMENTS, HIDE_STREAMLIT_CUSTOM_STYLE
from helpers import type_text, generate_summary, extract_text_from_pdf, read_file

def header():
    container = st.container()
    container.markdown("# Welcome to PDF Summariser")
    container.write("Summarise any Research PDF by uploading the file in the box on the right")

    file = st.file_uploader("", type="pdf")

    return(container, file)

def file_upload(container, file):
    file_name = f"{uuid.uuid4()}.pdf"
    if file is not None:
        with open(f"pdfs/{file_name}", "wb") as f:
            f.write(file.getbuffer())
        st.markdown(HIDE_ELEMENTS, unsafe_allow_html=True)
        return (container, file_name)
    else:
        return "error"
        
def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    st.markdown(HIDE_STREAMLIT_CUSTOM_STYLE, unsafe_allow_html=True)
    main_container, file = header()
    if st.button("Next"):
        result = file_upload(main_container, file)
        if result == "error":
            st.error("You didn't upload a pdf file yet!")
        else:
            container, file_name = result
            text = extract_text_from_pdf(f"pdfs/{file_name}")
            chunks = textwrap.wrap(text, 1000)
            for chunk in chunks:
                prompt = read_file("prompt.txt").replace('<<SUMMARY>>', chunk)
                summary = generate_summary(prompt)
                type_text(container, summary)

        type_text(container, "# That's all")


if __name__ == "__main__":
    main()
    
