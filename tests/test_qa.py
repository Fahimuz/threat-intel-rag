import os
import sys
sys.path.append("..")
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))
prompt = ChatPromptTemplate.from_template("""Answer the question based only on the following context from cybersecurity threat reports.
If you cannot find the answer, say "I don't have enough information in my reports to answer this."

Context: {context}
Question: {question}
Answer:""")
def format_docs(docs):
    return "\n\n".join(f"[{doc.metadata['source']}]: {doc.page_content}" for doc in docs)
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

test_questions = [
    "What is ransomware?",
    "How do cybercriminals demand payment?",
    "What industries are most targeted by ransomware?",
    "How does phishing work?",
    "What are the top cybercrimes reported to the FBI?",
    "How much money was lost to cybercrime?",
    "What should organizations do to prevent attacks?",
    "What is business email compromise?",
    "How do attackers encrypt files?",
    "What is the role of CISA in cybersecurity?"
]

print("=" * 60)
print("THREAT INTEL RAG -- TEST RESULTS")
print("=" * 60)

passed = 0
failed = 0

for i, question in enumerate(test_questions):
    print(f"\nTest {i+1}: {question}")
    print("-" * 40)
    answer = chain.invoke(question)
    
    if "don't have enough information" in answer.lower():
        print("RESULT: FAIL -- No relevant info found")
        failed += 1
    else:
        print(f"RESULT: PASS")
        print(f"Answer preview: {answer[:200]}...")
        passed += 1

print("\n" + "=" * 60)
print(f"FINAL SCORE: {passed}/{len(test_questions)} tests passed")
print(f"Accuracy: {round(passed/len(test_questions)*100)}%")
print("=" * 60)
