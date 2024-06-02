#%%
from pprint import pprint
import chromadb
from tqdm.autonotebook import tqdm, trange
from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain_core.output_parsers import StrOutputParser

#------------------------   Initialize Variables  ------------------
dbname = "catholic"  # name of the vector database
newcol = "mary"  # name of a collection in the vector database
dbpath = "./" + dbname # adding name to path of vector database

#%% -----------------------  Get or Create a Collection ---------------------
# Create a reference to a new Vector Database and create a collection in db called ipcc
run_client = chromadb.PersistentClient(path=dbpath)  # open a persistent database
# pprint(chroma_db.heartbeat())
pprint(run_client.list_collections())
db = Chroma(
    client=run_client,
    collection_name=newcol,
    embedding_function=embedding_function,
)
resp=db.similarity_search("how old was mary",3)
pprint(resp)


#%%

db3 = Chroma(collection_name="IPCC",  embedding_function=embedding_function, persist_directory="B:/python/database/IPCC",)
# docs = db3.max_marginal_relevance_search(query,4)
# docs = db3.similarity_search(query,5)
docs = db3.similarity_search_with_relevance_scores(query,3)
pprint(docs)


# %%
text="where was jesus born"
mydb = Chroma(persist_directory="./catholic", embedding_function=embedding_function)
resp=mydb.similarity_search(text,3)
pprint(resp)
# %%
