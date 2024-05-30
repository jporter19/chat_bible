#%%
from pprint import pprint
from langchain_chroma.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain_core.output_parsers import StrOutputParser

query="what is global warming"
db3 = Chroma(collection_name="IPCC",  embedding_function=embedding_function, persist_directory="B:/python/database/IPCC",)
docs = db3.max_marginal_relevance_search(query,4)
# docs = db3.similarity_search(query,5)
# docs = db3.similarity_search_with_relevance_scores(query,3)
pprint(docs[0])

