#%%
import streamlit as st
import pymupdf

# input_file = st.file_uploader("hi")
uploaded_files = st.file_uploader('Upload a file',accept_multiple_files=True)
if uploaded_files:
   # uploaded_file.seek(0,0)
    for df in uploaded_files:
        if df.type == "application/pdf": file_type="pdf"
        elif df.type == "text/plain": file_type = "txt"
        elif df.type == "application/epub+zip": file_type = "epub"
        elif df.type == "application/octet-stream": file_type = "txt"
        # elif df.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document": file_type = "docx"
        # elif df.type == "application/vnd.oasis.opendocument.text" : file_type = "odt"
        # elif df.type == "application/vnd.oasis.opendocument.spreadsheet" : file_type = "ods"
        elif df.type == "text/csv" : file_type = "txt"
        # elif df.type == "application/msword" : file_type = "doc"
        elif df.type == "text/html" : file_type = "txt"
        # elif df.type == "application/rtf" : file_type = "rtf"
        else: 
            st.write(f"{df.type} is not a supported file type")
            break
        st.write(df.size)
        st.write(df.type)
        df.seek(0,0)
        if df.size > 0:
            docs = pymupdf.open(stream=df.read(),filetype=file_type)
            for page in docs:
                st.write(page.get_text())
                #for page in doc: # iterate the document pages
                splitter_text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
                st.write(splitter_text)

# doc = pymupdf.open("b:\\python\\data\\file1.pdf") # open a document
#this is not working!
