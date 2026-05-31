import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

st.set_page_config(page_title="Threat Intel RAG", page_icon=":lock:", layout="wide")
st.title("Cybersecurity Threat Intelligence Tool")
st.caption("Ask anything about ransomware, cybercrime, and threats -- powered by real government reports")
st.markdown("**Built by:** Fahim Uzzaman  |  **University:** Minnesota State University, Mankato  |  **Major:** B.S. Computer Information Technology")
st.markdown("---")

MITRE_MAPPING = {
    "phishing": "https://attack.mitre.org/techniques/T1566/",
    "ransomware": "https://attack.mitre.org/techniques/T1486/",
    "credential": "https://attack.mitre.org/techniques/T1078/",
    "brute force": "https://attack.mitre.org/techniques/T1110/",
    "malware": "https://attack.mitre.org/techniques/T1587/",
    "social engineering": "https://attack.mitre.org/techniques/T1598/",
    "data theft": "https://attack.mitre.org/techniques/T1041/",
}

THREAT_CATEGORIES = {
    "ransomware": "Ransomware",
    "phishing": "Phishing",
    "malware": "Malware",
    "fraud": "Fraud",
    "data breach": "Data Breach",
    "social engineering": "Social Engineering",
    "credential": "Credential Attack",
}

@st.cache_resource
def load_chain():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = ChatAnthropic(model="claude-haiku-4-5-20251001", anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context from cybersecurity threat reports.
If you cannot find the answer, say "I don't have enough information in my reports to answer this."
Always mention which report your answer comes from.

Context: {context}

Question: {question}

Answer:""")
    def format_docs(docs):
        return "\n\n".join(f"[{doc.metadata['source']}]: {doc.page_content}" for doc in docs)
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

chain, retriever = load_chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.title("Loaded Reports")
all_reports = ["cisa-ransomware-guide.txt", "ic3-2022-report.txt", "ic3-internet-crime-report.txt"]
selected_reports = st.sidebar.multiselect("Filter by report:", all_reports, default=all_reports)

st.sidebar.title("Suggested Questions")
suggestions = [
    "What is ransomware?",
    "How do cybercriminals steal data?",
    "What are the top cybercrimes reported to FBI?",
    "How can organizations protect against attacks?",
    "What is phishing and how does it work?"
]
for s in suggestions:
    if st.sidebar.button(s):
        st.session_state.question = s

st.sidebar.markdown("---")
st.sidebar.markdown("**Fahim Uzzaman**")
st.sidebar.markdown("Minnesota State University, Mankato")
st.sidebar.markdown("B.S. Computer Information Technology")
st.sidebar.markdown("[GitHub](https://github.com/Fahimuz/threat-intel-rag) | [LinkedIn](https://www.linkedin.com/in/fahimuzzam/)")

question = st.text_input("Ask a question:", value=st.session_state.get("question", ""), key="input")

if question:
    with st.spinner("Searching threat reports..."):
        answer = chain.invoke(question)
        docs = retriever.invoke(question)
        docs = [d for d in docs if d.metadata["source"] in selected_reports] or docs

    category = "General"
    for keyword, label in THREAT_CATEGORIES.items():
        if keyword in question.lower() or keyword in answer.lower():
            category = label
            break

    st.session_state.chat_history.append({"q": question, "a": answer, "category": category})

    st.markdown("### Answer")
    st.markdown(f"**Threat Category:** {category}")
    st.write(answer)

    mitre_links = []
    for keyword, url in MITRE_MAPPING.items():
        if keyword in answer.lower():
            mitre_links.append(f"[{keyword.title()}]({url})")
    if mitre_links:
        st.markdown("### MITRE ATT&CK References")
        st.markdown(" | ".join(mitre_links))

    st.markdown("### Sources Used")
    for i, doc in enumerate(docs):
        with st.expander(f"Source {i+1}: {doc.metadata['source']}"):
            st.write(doc.page_content)

if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### Chat History")
    for item in reversed(st.session_state.chat_history[-5:]):
        with st.expander(f"{item['category']} -- {item['q']}"):
            st.write(item["a"])
