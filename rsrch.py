# run: pip install langchain-openai langchain playwright beautifulsoup4 streamlit
# run: playwright install

import streamlit as st
import pprint
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

#Load Text
# loader = WebBaseLoader("https://openai.com/blog/new-embedding-models-and-api-updates")
# data = loader.load()
# print(data)

# Load HTML
loader = AsyncChromiumLoader(["https://openai.com/blog/new-embedding-models-and-api-updates"])
html = loader.load()
pprint.pprint(html)

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    html, tags_to_extract=["p"]
)
pprint.pprint(docs_transformed)