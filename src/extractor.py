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

# Extrai todo texto de um arquivo
def extract_text(path):
    try:
        doc = pymupdf.open(path)
        full_text = ""

        for page in doc:
            full_text += page.get_text()

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

# Monta o URL
def build_doc_url(filename):
   doc_id = filename.split('-')[0]
   
   return f"https://sol.sbc.org.br/index.php/stil/article/view/{doc_id}"

# Extrai o titulo
def extract_title(path):
    try:
        doc = pymupdf.open(path)

        title = extract_title_by_font_size(doc)
        
        doc.close()
        
        if title:
            title = clean_title(title)
        
        return title
    
    except Exception as e:
        print(f"Erro ao extrair título: {e}")
        return ""

# Extrai título baseado no tamanho da fonte
def extract_title_by_font_size(doc):
    try:
        first_page = doc[0]
        blocks = first_page.get_text("dict")
        
        font_map = {}
        
        for block in blocks.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_size = span.get("size", 0)
                    text = span.get("text", "").strip()
                    
                    font_map.setdefault(font_size, []).append(text)
        
        if not font_map:
            return ""
        
        max_font = max(font_map.keys())
        
        title = ' '.join(font_map[max_font])
        
        title = clean_title(title)
        
        return title
    
    except Exception as e:
       print(f"Erro ao extrair título pelo tamanho da fonte: {e}")
       return ""

# Limpa o título
def clean_title(title):
    if not title:
        return ""

    # Remove números de página
    title = re.sub(r'\b\d+\s*$', '', title)

    # Remove múltiplos espaços
    title = re.sub(r'\s+', ' ', title)

    # Remove quebras de linha
    title = title.replace('\n', ' ').replace('\r', ' ')

    # Remove espaços no início e fim
    title = title.strip()

    return title
    
# Extrai resumo
def extract_abstract(path):
    try:
        doc = pymupdf.open(path)

        abstract = extract_title_by_italic_format(doc)

        doc.close()

        if abstract:
            abstract = clean_abstract(abstract)

        return abstract
    
    except Exception as e:
        print(f"Erro ao extrair resumo: {e}")
        return ""

# Extrai resumo baseado no nome da seção
def extract_title_by_italic_format(doc):
    try:
        first_page = doc[0]
        blocks = first_page.get_text("dict")

        abstract_parts = []
        found_abstract = False

        for block in blocks.get("blocks", []):
            for line in block.get("lines", []):
                line_text = ""

                for span in line.get("spans", []):
                    text = span.get("text", "").strip()

                    if text:
                        line_text += text + " "

                line_text = line_text.strip()

                if not line_text:
                    continue

                if "Resumo" in line_text or "resumo" in line_text:
                    found_abstract = True
                    line_text = line_text.replace("Resumo", "").replace("resumo", "").strip(".: ")

                    if line_text:
                        abstract_parts.append(line_text)
                    continue

                if found_abstract:
                    line_lower = line_text.lower()
                    if (line_lower.startswith(("1.introdu", "1. introdu", "I.introdu", "I. introdu")) or
                        any(phrase in line_text.lower() for phrase in ["introdução", "Introdu", "palavras chaves", "keywords"])):
                        return abstract_parts

                    abstract_parts.append(line_text)

        return abstract_parts

    except Exception as e:
        print(f"Erro ao extrair resumo: {e}")
        return ""
    
# Limpa o resumo
def clean_abstract(abstract):
    if not abstract:
        return ""

    if abstract:
            abstract = ' '.join(abstract)
            abstract = ' '.join(abstract.split())
            return abstract

    return ""