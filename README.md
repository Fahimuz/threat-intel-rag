# Cybersecurity Threat Intelligence Tool

A RAG-based AI tool that lets security analysts query real government cybersecurity threat reports using natural language -- like Google, but only for threat intelligence documents.

Built by **Fahim Uzzaman** | Minnesota State University, Mankato | B.S. Computer Information Technology

---

## What It Does

Instead of manually reading hundreds of pages of threat reports, analysts can type a question like:
> "How does LockBit ransomware operate?"

And instantly get a cited answer from real CISA and FBI reports.

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI / LLM | Anthropic Claude (claude-haiku) |
| RAG Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Frontend | Streamlit |
| PDF Processing | pypdf |

---

## Architecture

PDF Reports --> Text Extraction --> Chunking (500 tokens) --> Embeddings --> ChromaDB
User Question --> Embedding --> Similarity Search --> Top 3 Chunks --> Claude AI --> Answer

---

## Features

- Natural language search across 3 real threat intelligence reports
- Threat category tagging (Ransomware, Phishing, Malware, Fraud, etc.)
- MITRE ATT&CK framework references linked automatically
- Multi-document filtering
- Chat history for follow-up questions
- Source citations for every answer

---

## Threat Reports Loaded

- CISA Ransomware Guide (CISA / MS-ISAC)
- IC3 Internet Crime Report 2022 (FBI)
- IC3 Internet Crime Report 2023 (FBI)

---

## How to Run

1. Clone the repo
   git clone https://github.com/Fahimuz/threat-intel-rag.git
   cd threat-intel-rag

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your API key
   Create a .env file:
   ANTHROPIC_API_KEY=your_key_here

5. Build the vector database
   python build_vectordb.py

6. Run the app
   streamlit run app.py

---

## Test Results

Accuracy: 70% (7/10 test questions answered correctly)
Adding more threat reports will increase accuracy significantly.

---

## Future Improvements

- Add more threat reports (Mandiant M-Trends, Microsoft MSTIC)
- Real-time CVE database integration
- User authentication for enterprise use
- Docker containerization

---

## Contact

- GitHub: https://github.com/Fahimuz
- LinkedIn: https://www.linkedin.com/in/fahimuzzam/
- Portfolio: https://bold.pro/my/fnu-fahimuzzaman-260212134518
