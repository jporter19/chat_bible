
#%%  - these are the importers 
import streamlit as st  # Streamlit is a package used for simple websites
import chromadb         # Chroma Db is an open source vector database
from langchain_chroma.vectorstores import Chroma
from pprint import pprint  # pprint is a bit better than print
from chromadb.config import Settings
from tqdm.autonotebook import tqdm, trange
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# from pypdf import PdfReader, PdfWriter  # reads pdf files
import pymupdf
import pdfplumber
from io import StringIO
import re   # re is regular expressions for pattern matching
#default_ef = embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


#%% - this is a path to the primary database, each database can have multiple collections
dbpath = "b:\\python\\database\\IPCC" # set the path to the DB
if 'col_choice' not in st.session_state:  #initialize selection of a collection
    st.session_state['col_choice']=None   # This could be set a default

#%%
# This function will produce a distinct list of collection to be displayed in drop down
def my_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections

#%%  ------------------  Open an Existing Chroma DB as a Client  -----------------------------
run_client = chromadb.PersistentClient(path=dbpath)
# --------------------  This is a side bar collection pickter  ----------------------------
st.session_state.col_choice = st.sidebar.selectbox("Pick a Collection",my_collections(run_client))
#%%  ---------If a Collection is selected Create a LangChain Chroma instance  ------------------
if st.session_state.col_choice:
    db= Chroma(persist_directory=dbpath,collection_name=st.session_state.col_choice,embedding_function=embedding_function)
resp_cnt = st.sidebar.slider(min_value=1,max_value=10,label="Set the Number of Response")
########### - Testing - ###########
# st.write(db._collection.count())

#%% 
def closest_index(dists, val):
    # --------------- the absolute value of subtracting 1 from every number above and below 1, the closest will be the smallest
    difference = [abs(dist-1) for dist in dists]
    # the absolute val list (difference) and the input list (dists) have the same indexes
    # ----------------  sorted_list will be the dists sorted by difference
    sorted_list = sorted(dists, key=lambda x: difference[dists.index(x)])
    # ----------------  sorted_list could be very long, closet 3 takes the 1st 3 in the sorted list
    closest = sorted_list[:val]
    # ---------------- add the index from dists to return_ids when it matches a distance in the closest list
    return_ids = [dists.index(i) for i in closest if i in dists]
    return return_ids

#%%  --------------- Main Program  -------------------------------
if 'prompt_res' not in st.session_state:
    st.session_state['prompt_res']=dict()

# Setup tabs 
tab1, tab2 = st.tabs(["Query","Admin"]) 

with tab1:
    # ------------- Display results in a container  ------------------
    with st.container():  # using a container pushes the input to the top of the page
        st.subheader(f'Collection: [{st.session_state.col_choice}]',divider=True)
        prompt=(st.chat_input('What is your question?'))
        if prompt: # if prompt has data then run this
            res = db.similarity_search_with_relevance_scores(prompt,resp_cnt)
            resp_cnt = len(res)
            for doc in res:
                # st.write(doc)
                st.write(doc[0].page_content)
                st.write(f'Source: {doc[0].metadata['source']}')
                st.button('See More',key=doc.index)

            #docs = closest_index(res["distances"][0],resp_cnt)
            #best_docs = ''
            #for d in docs:
            #    best_docs = best_docs + res["documents"][0][d] +  f'  \n :blue[Source:] *{res["metadatas"][0][d].get('source')}*' +'\n\n'
                # best_docs = best_docs + res["documents"][0][d] +  '  '  + 'www.newadvent.org'   
            # st.write(best_docs)
            prompt = prompt + ' -- Collection  \{'+st.session_state.col_choice+'\}'
            #st.session_state.prompt_res.update({prompt:best_docs[0]})
            #st.session_state.prompt_res.update({prompt:best_docs})
            response = st.container(height=600)
            with response:
                for key in st.session_state.prompt_res:
                    message = st.chat_message('user')
                    message.write(key)
                    mycont=st.container(height=250, border=True)
                    with mycont: st.write(st.session_state.prompt_res[key])
with tab2:
    #import 
    #%%
    from langchain_community.document_loaders import TextLoader

    #%%
    uploaded_file = st.file_uploader(':blue[Choose a File]',type=['txt','pdf'],accept_multiple_files=False,label_visibility='hidden')
    #uploaded_files = st.file_uploader(':blue[Choose a File]',type=['txt','pdf'],accept_multiple_files=True,label_visibility='hidden')
    if uploaded_file is not None:
        st.success("Uploaded the file")
        with pdfplumber.open(uploaded_file) as file:
            all_pages = file.pages
            st.write(len(all_pages))
            st.write(all_pages[0].extract_text()) # you can print and check the data from any page in pdf   