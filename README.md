# ⚡ Automated Verification Agent

## 🚀 Overview
This tool automates the validation of **Battery Management Systems (BMS)** by bridging the gap between static PDF requirements (ISO 26262) and executable validation scripts.

Engineers can ask natural language questions about safety limits, and the agent uses **RAG (Retrieval-Augmented Generation)** to:
1.  **Retrieve** specific technical thresholds from OEM manuals.
2.  **Generate** executable **MATLAB/Simulink** test scripts.
3.  **Cite** the exact source page for traceability.

## 🛠️ Tech Stack
* **Core Logic:** Python, LangChain
* **AI Model:** OpenAI GPT-4o
* **Vector Database:** ChromaDB (Semantic Retrieval)
* **Interface:** Streamlit
* **Data Processing:** Unstructured.io (PDF Chunking)

## 📸 Demo
![Agent Interface](YOUR_SCREENSHOT_FILENAME.png) 
*(Replace this with the "Money Shot" you took in Move 1)*

## 🔋 Key Features
* **Semantic Chunking:** Keeps related engineering constraints (Voltage/Current tables) together.
* **Code Generation:** Auto-writes `.m` scripts for Simulink verification.
* **Safety Compliance:** System prompts enforced to prioritize ISO 26262 standards.