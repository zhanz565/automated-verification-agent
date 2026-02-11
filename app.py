import streamlit as st
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- Page Setup ---
st.set_page_config(page_title="AI Engineering Agent", page_icon="⚡", layout="wide")
load_dotenv()

# --- Memory & Logic ---
@st.cache_resource
def load_ai_system():
    vectorstore = Chroma(
        persist_directory="./chroma_db", 
        embedding_function=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # PRO SYSTEM PROMPT: Optimized for BMO (Compliance) and Johnson (MATLAB)
    system_prompt = (
        "You are a Senior Verification Engineer specializing in Safety-Critical Systems (ISO 26262) "
        "and Regulatory Compliance. Use the provided context and history to assist the user.\n\n"
        "GUIDELINES:\n"
        "1. If generating MATLAB: Provide a full, standalone function with professional comments.\n"
        "2. For Financial Queries: Prioritize accuracy and cite specific regulatory sections.\n"
        "3. Maintain 'Traceability': Always mention which document or section provided the limit.\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)

# --- UI Interface ---
st.title("⚡ Enterprise Verification Agent")
st.markdown("*Bridging Requirements to Executable Code*")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Conversation History"):
        st.session_state.messages = []
    st.divider()
    st.info("Architecture: RAG (Retrieval-Augmented Generation) with ChromaDB persistence.")

# Load system
rag_chain = load_ai_system()

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_query := st.chat_input("Ask about safety limits or MATLAB test generation..."):
    st.chat_message("user").markdown(user_query)
    
    # Prepare history for the AI
    chat_history = []
    for m in st.session_state.messages:
        chat_history.append((m["role"], m["content"]))

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Knowledge Base..."):
            response = rag_chain.invoke({
                "input": user_query,
                "chat_history": chat_history
            })
            answer = response["answer"]
            st.markdown(answer)
    
    # Save to session
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.session_state.messages.append({"role": "assistant", "content": answer})