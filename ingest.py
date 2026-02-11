import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load your API key
load_dotenv()

def ingest_documents():
    print("🚀 Starting Ingestion Process...")
    
    # 1. Load the Technical Manual
    # This reads the text from your PDF
    loader = PyPDFLoader("manual.pdf")
    raw_documents = loader.load()
    print(f"   - Loaded {len(raw_documents)} pages from manual.pdf")

    # 2. Semantic Chunking (The Engineering Logic)
    # We split text into chunks of 1000 characters.
    # 'overlap' ensures we don't cut a sentence in half (like "Max voltage is... [cut] ...4.2V").
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"   - Split into {len(documents)} searchable knowledge chunks.")

    # 3. Create the Vector Database (The Brain)
    # This sends your text to OpenAI, gets the "embedding" (math representation),
    # and saves it locally in a folder called 'chroma_db'.
    print("   - Embedding data... (this might take 10-20 seconds)")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_db" 
    )
    
    print("✅ Success! Your PDF is now a searchable AI database.")

if __name__ == "__main__":
    ingest_documents()