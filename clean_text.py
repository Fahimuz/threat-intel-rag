import os
import re
from pypdf import PdfReader

data_folder = "data"
output_folder = "data_clean"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(data_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(data_folder, filename)
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Clean the text
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\.{3,}', '', text)
        text = re.sub(r'\x00', '', text)
        text = text.strip()

        out_file = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Cleaned: {filename} -> {len(text)} characters")

print("Done!")
