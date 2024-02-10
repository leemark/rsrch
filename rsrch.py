# run: pip install langchain-openai langchain playwright beautifulsoup4 streamlit python-dotenv
# run: playwright install

import streamlit as st
import pprint
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables i.e. API keys and langsmith config
load_dotenv()

# # Load HTML
# loader = AsyncChromiumLoader(["https://openai.com/blog/new-embedding-models-and-api-updates"])
# html = loader.load()


# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(
#     html, tags_to_extract=["p"]
# )


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

schema = {
    "properties": {
        "blog_article_title": {"type": "string"},
        "blog_article_summary": {"type": "string"},
    },
    "required": ["blog_article_title", "blog_article_summary"],
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content


urls = ["https://openai.com/blog/openai-announces-leadership-transition"]
extracted_content = scrape_with_playwright(urls, schema=schema)







# ref: https://python.langchain.com/docs/use_cases/web_scraping