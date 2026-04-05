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