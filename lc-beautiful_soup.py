
#%%
from pprint import pprint
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load HTML
# loader = AsyncChromiumLoader(["https://www.wsj.com"])
# loader = AsyncChromiumLoader(["https://www.newadvent.org"])
loader = AsyncChromiumLoader(["https://catholicaudiobooks.wordpress.com/fiction/"])
html = loader.load()
# print(html)g

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    html, tags_to_extract=["p", "li", "div", "a"]
)
pprint(docs_transformed[0].page_content[0:4000])
# %%
