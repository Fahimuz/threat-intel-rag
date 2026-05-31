from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

input_folder = "data_clean"
chunks_all = []

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        
        chunks = splitter.create_documents(
            [text],
            metadatas=[{"source": filename}]
        )
        chunks_all.extend(chunks)
        print(f"{filename} -> {len(chunks)} chunks")

print(f"Total chunks: {len(chunks_all)}")
