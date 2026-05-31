from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

print("Loading and chunking text files...")
input_folder = "data_clean"
chunks_all = []

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = splitter.create_documents([text], metadatas=[{"source": filename}])
        chunks_all.extend(chunks)

print(f"Total chunks: {len(chunks_all)}")
print("Generating embeddings and storing in ChromaDB (this may take a minute)...")

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(chunks_all, embeddings, persist_directory="chroma_db")

print("Done! Vector database saved to chroma_db/")
