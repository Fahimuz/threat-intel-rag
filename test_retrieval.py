from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

query = "How does ransomware attack a victim?"
print(f"Query: {query}")
print("---")

results = db.similarity_search(query, k=3)
for i, doc in enumerate(results):
    print(f"Result {i+1} (from {doc.metadata['source']}):")
    print(doc.page_content[:300])
    print("---")
