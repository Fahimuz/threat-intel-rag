import os
from pypdf import PdfReader

data_folder = "data"

for filename in os.listdir(data_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(data_folder, filename)
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        print(f"File: {filename}")
        print(f"Characters extracted: {len(text)}")
        print(f"Pages: {len(reader.pages)}")
        print("---")
