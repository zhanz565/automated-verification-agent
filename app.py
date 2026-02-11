import streamlit as st
import os
from dotenv import load_dotenv

# LangChain Imports
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Page Configuration (The "Professional" Look)
st.set_page_config(
    page_title="BMS Verification Agent",
    page_icon="🔋",
    layout="wide"
)

# Load secrets
load_dotenv()

# 2. Load the "Brain" (Cached for speed)
@st.cache_resource
def load_chain():
    # Load Vector DB
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chroma_db", 
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Define System Prompt (Your Engineering Logic)
    system_prompt = (
        "You are a Senior Verification Engineer for an Automotive Battery System. "
        "Use the provided context to answer the user's request. "
        "\n\n"
        "If the user asks for a test script:"
        "1. Identify numerical limits (voltage, current, temp) from the context."
        "2. Generate a MATLAB/Simulink test script snippet."
        "3. Cite the section of the manual you used."
        "\n\n"
        "Context: {context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Build Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

# Load the chain
try:
    chain = load_chain()
except Exception as e:
    st.error(f"Error loading the brain: {e}")
    st.stop()

# 3. Sidebar (The Control Panel)
with st.sidebar:
    st.header("🔋 System Controls")
    st.markdown("This tool automates **ISO 26262** compliance checks.")
    st.info("Connected to: **BMS_Safety_Manual_v1.0**")
    if st.button("Clear Chat History"):
        st.session_state.messages = []

# 4. Main Chat Interface
st.title("⚡ Automated Verification Agent")
st.markdown("Ask engineering questions or request **MATLAB test scripts**.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ex: Write a MATLAB script to check over-current limits."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing Safety Requirements..."):
            response = chain.invoke({"input": prompt})
            answer = response["answer"]
            st.markdown(answer)
    
    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})