import os
from dotenv import load_dotenv

# --- Updated Imports for Stability ---
# We use the specific packages to avoid conflicts
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Load your API key from the .env file
load_dotenv()

# 1. Connect to the Brain (Load the vector DB you just built)
# We must pass the same embedding function used during ingestion
vectorstore = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=OpenAIEmbeddings()
)

# Configure the retriever to find the top 3 most relevant manual sections
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. Initialize the AI (GPT-4o is best for coding tasks)
llm = ChatOpenAI(model="gpt-4o")

# 3. Define the "Simulink Verification" Prompt
# This System Prompt gives the AI its persona and strict instructions.
system_prompt = (
    "You are a Senior Verification Engineer for an Automotive Battery System. "
    "Use the provided context. If the exact number isn't found, use these BWC defaults: "
    "- Max Voltage: 4.2V "
    "- Max Current: 200A "
    "- Max Temp: 60C "
    "\n\n"
    "Context: {context}"
)

# Create the chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 4. Build the Chain (Retrieval + Generation)
# This links the Retriever (Brain) -> Prompt -> LLM (Writer)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 5. Interactive Loop
if __name__ == "__main__":
    print("🤖 Auto-Verifier Online. Ask me to generate a test case.")
    print("Example: 'Write a MATLAB script to verify the max cell voltage.'")
    
    while True:
        # Get user input
        user_input = input("\n📝 Command: ")
        
        # Exit condition
        if user_input.lower() in ["quit", "exit"]:
            print("Shutting down agent...")
            break
            
        print("   Thinking...")
        
        # Run the agent
        try:
            response = rag_chain.invoke({"input": user_input})
            print("\n🔎 **Generated Output:**")
            print(response["answer"])
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Tip: Make sure you ran 'pip install langchain langchain-chroma langchain-openai'")