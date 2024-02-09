# run: pip install langchain-openai langchain playwright beautifulsoup4 streamlit python-dotenv
# run: playwright install

import streamlit as st
import pprint
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from dotenv import load_dotenv

# Load environment variables i.e. API keys and langsmith config
load_dotenv()

# Load HTML
loader = AsyncChromiumLoader(["https://openai.com/blog/new-embedding-models-and-api-updates"])
html = loader.load()
pprint.pprint(html)

bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(
    html, tags_to_extract=["p"]
)
pprint.pprint(docs_transformed)







# ref: https://python.langchain.com/docs/use_cases/web_scraping