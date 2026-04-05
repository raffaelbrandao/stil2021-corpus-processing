# Extração de textos de arquivos em PDF
# Usando PyMuPDF
import pymupdf
import os
import re

# Lista os arquivos em um diretório
def list_docs(path):
    docs = []

    if not os.path.exists(path):
        print(f"A pasta não foi encontrada: {path}")
        return docs

    for file in os.listdir(path):
        docs.append(os.path.join(path, file))

    return sorted(docs)

# Função que extrai todo texto de um arquivo
def extract_text(path):
    try:
        doc = pymupdf.open(path)

        for page in doc:
            full_text = page.get_text()

        doc.close()

        return full_text
    
    except Exception as e:
        print(f"Erro ao ler o caminho do arquivo {path}: {e}")
        return ""

# Limpa o texto removendo espaços e as quebras de linhas
def clean_text(text):
    # Remove múltiplos espaços e as quebras de linhas
    text = re.sub(r'\s+', ' ', text)

    # Remove espaços no início e fim
    text = text.strip()

    return text


