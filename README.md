# ⚡ Enterprise Verification Agent (EVA)
### Automated Compliance & Code Generation for High-Stakes Industries

![Project Demo](demo.png)

## 🚀 The Mission
Engineers and analysts often face "document fatigue" when checking technical systems against 1000+ pages of safety standards or financial regulations. 

This project solves that by using **Retrieval-Augmented Generation (RAG)** to bridge the gap between unstructured PDF requirements and executable verification logic.

## 🏗️ Multi-Domain Architecture
The system is designed with a **Domain-Agnostic Knowledge Pipeline**. By utilizing a directory-based ingestion strategy, the agent can pivot between industry contexts seamlessly:

- **🔋 Automotive (ISO 26262):** Parses BMS safety manuals to auto-generate MATLAB/Simulink test scripts for over-voltage, thermal protection, and current limits.
- **🏦 Finance (BMO/Banking Regs):** Analyzes regulatory compliance documents (e.g., OSFI guidelines) to verify banking procedures and audit requirements.

## 🛠️ Technical Stack
* **LLM Engine:** OpenAI GPT-4o (State-of-the-art reasoning for code and logic).
* **Framework:** LangChain (Orchestrating the retrieval and memory chain).
* **Vector Database:** ChromaDB (Persistent semantic storage for document chunks).
* **Interface:** Streamlit (Professional web-based dashboard).
* **Memory:** Stateful Conversation History (Remembers context across follow-up questions).

## 🔋 Advanced Features
- **Semantic Chunking:** Advanced text splitting that preserves the context of engineering tables and numerical limits.
- **Traceability:** Every response includes citations from the source material to meet audit standards.
- **Professional MATLAB Output:** Generates standalone, commented functions ready for integration into Simulink Test.

## 💻 Installation & Usage
1. **Clone Repo:** `git clone https://github.com/zhanz565/automated-verification-agent.git`
2. **Environment:** Add your `OPENAI_API_KEY` to a `.env` file.
3. **Ingest Data:** Place PDFs in `data_vault/automotive` or `data_vault/finance`, then run `python ingest.py`.
4. **Launch Web App:** `streamlit run app.py`

---
*Developed by Zhenxin Zhang - Specialized in AI Automation and Embedded Systems Verification.*