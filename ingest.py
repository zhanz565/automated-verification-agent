import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def ingest_all_domains():
    print("🚀 Initializing Multi-Domain Ingestor...")
    
    # Path configuration
    base_data_path = "./data_vault"
    persist_directory = "./chroma_db"
    
    # Ensure data_vault exists
    if not os.path.exists(base_data_path):
        os.makedirs(f"{base_data_path}/automotive")
        os.makedirs(f"{base_data_path}/finance")
        print(f"📁 Created folders. Please put your PDFs in {base_data_path}")
        return

    all_docs = []
    
    # Loop through subfolders (Automotive, Finance, etc.)
    for domain in os.listdir(base_data_path):
        domain_path = os.path.join(base_data_path, domain)
        if os.path.isdir(domain_path):
            print(f"📂 Processing Domain: {domain.upper()}")
            for file in os.listdir(domain_path):
                if file.endswith(".pdf"):
                    loader = PyPDFLoader(os.path.join(domain_path, file))
                    raw_docs = loader.load()
                    # Add metadata so the AI knows which 'domain' the info belongs to
                    for doc in raw_docs:
                        doc.metadata["domain"] = domain
                    all_docs.extend(raw_docs)

    # Semantic Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_chunks = text_splitter.split_documents(all_docs)

    # Vector Storage
    print(f"🧠 Embedding {len(final_chunks)} chunks into Vector DB...")
    vectorstore = Chroma.from_documents(
        documents=final_chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_directory
    )
    print("✅ Multi-Domain Brain Built Successfully!")

if __name__ == "__main__":
    ingest_all_domains()