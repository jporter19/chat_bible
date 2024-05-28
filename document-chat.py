
#%%  - these are the importers
import streamlit as st
import chromadb
from pprint import pprint
from chromadb.config import Settings
import re


#%% - this is a path
dbpath = "b:\\python\\holy-vec\\database\\holy_db" # set the path to the DB

if 'col_choice' not in st.session_state:  #initialize selection of a collection
    st.session_state['col_choice']=None

#%%
# This function will produce a distinct list of collection to be displayed in drop down
def my_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections

#%%
chroma_db = chromadb.PersistentClient(path=dbpath)  # open a persistent database
st.session_state.col_choice = st.sidebar.selectbox("Pick a Collection",my_collections(chroma_db))
if st.session_state.col_choice:
    # st.write(col_choice)
    chroma_collection = chroma_db.get_collection(st.session_state.col_choice)
resp_cnt = st.sidebar.slider(min_value=1,max_value=10,label="Set the Number of Response")



# chroma_collection = chroma_db.get_collection(col_nm)  # Create a collection
# pprint(chroma_db.list_collections()) # print all collections in database
# ***** chroma_db.delete_collection("bluemetal")
#  This code will produce a list of collection names in the DB


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
# ------------- Display results in a container  ------------------
with st.container():  # using a container pushes the input to the top of the page
    st.subheader(f'Collection: [{st.session_state.col_choice}]',divider=True)
    prompt=(st.chat_input('What is your question?'))
    if prompt: # if prompt has data then run this
        res = chroma_collection.query(query_texts=prompt, 
            n_results=18,
            include=["distances","documents","embeddings","metadatas"])
        docs = closest_index(res["distances"][0],resp_cnt)
        best_docs = ''
        for d in docs:
             best_docs = best_docs + res["documents"][0][d] +  f'  \n :blue[Source:] *{res["metadatas"][0][d].get('source')}*' +'\n\n'
            # best_docs = best_docs + res["documents"][0][d] +  '  '  + 'www.newadvent.org'
            
        # st.write(best_docs)
        prompt = prompt + ' -- Collection  \{'+st.session_state.col_choice+'\}'
        #st.session_state.prompt_res.update({prompt:best_docs[0]})
        st.session_state.prompt_res.update({prompt:best_docs})
        response = st.container(height=600)
        with response:
            for key in st.session_state.prompt_res:
                message = st.chat_message('user')
                message.write(key)
                mycont=st.container(height=250, border=True)
                with mycont: st.write(st.session_state.prompt_res[key])
    


