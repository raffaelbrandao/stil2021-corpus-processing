# Extração de textos de arquivos em PDF
# Usando PyMuPDF
import pymupdf
import os
import re
from pathlib import Path
import unicodedata
from collections import Counter

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
def extract_text_simple(path):
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
def clean_text_simple(text):
    # Remove múltiplos espaços e as quebras de linhas
    text = re.sub(r'\s+', ' ', text)

    # Remove espaços no início e fim
    text = text.strip()

    return text

def fix_hyphenation(text):
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    return text

def fix_combining_accents(text):

    accent_map = {
        "´": {"a":"á","e":"é","i":"í","o":"ó","u":"ú",
              "A":"Á","E":"É","I":"Í","O":"Ó","U":"Ú"},
        "ˆ": {"a":"â","e":"ê","i":"î","o":"ô","u":"û",
              "A":"Â","E":"Ê","I":"Î","O":"Ô","U":"Û"},
        "˜": {"a":"ã","o":"õ","A":"Ã","O":"Õ"},
        "`": {"a":"à","A":"À"},
        "¸": {"c":"ç","C":"Ç"},
        "¨": {"u":"ü","U":"Ü"},
    }

    for accent, letters in accent_map.items():
        for letter, replacement in letters.items():
            text = re.sub(rf"{accent}\s*{letter}", replacement, text)

    return text

def normalize_unicode(text):
    text = unicodedata.normalize("NFC", text)
    return text

def remove_repeated_lines(text, min_repetition=3):

    lines = text.split("\n")
    line_counts = Counter(lines)

    cleaned_lines = [
        line for line in lines
        if line_counts[line] < min_repetition or len(line.strip()) < 5
    ]

    return "\n".join(cleaned_lines)

def clean_structure(text):
    # Remove múltiplas quebras de linha
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove múltiplos espaços
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove espaço antes de pontuação
    text = re.sub(r'\s+([.,;:])', r'\1', text)

    return text.strip()

def fix_broken_paragraphs(text):
    # Junta linhas que não terminam com pontuação forte
    text = re.sub(r'(?<![.!?])\n(?!\n)', ' ', text)
    return text

def fix_ligatures(text):
    ligatures = {
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬀ": "ff",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "œ": "oe",
        "æ": "ae",
    }

    for wrong, correct in ligatures.items():
        text = text.replace(wrong, correct)

    return text

def fix_remaining_artifacts(text):
    text = re.sub(r'[cC]¸\s*˜\s*a\s*o', 'ção', text)
    text = re.sub(r'[cC]¸\s*˜\s*o\s*e\s*s?', 'ções', text)

    text = text.replace("c¸", "ç")
    text = text.replace("C¸", "Ç")

    text = text.replace("´ı", "í")
    text = text.replace("`ı", "ì")

    text = re.sub(r'([a-zA-Z])https?://', r'\1 https://', text)

    return text

def fix_backtick_artifacts(text):
    text = text.replace("ç`", "ç")
    text = text.replace("a`", "à")
    text = text.replace("e`", "è")
    text = text.replace("i`", "ì")
    text = text.replace("o`", "ò")
    text = text.replace("u`", "ù")
    text = text.replace("ç`oes", "ções")

    return text

def isolate_references(text):
    text = re.sub(r'\s+(Referências)', r'\n\n\1', text)
    return text

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

def clean_text(text):
    text = fix_hyphenation(text)
    text = fix_ligatures(text)
    text = fix_combining_accents(text)
    text = fix_backtick_artifacts(text)
    text = fix_remaining_artifacts(text)
    text = normalize_unicode(text)
    text = isolate_references(text)
    text = remove_repeated_lines(text)
    text = fix_broken_paragraphs(text)
    text = clean_structure(text)

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
            title = clean_text(title)
        
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
        
        return title
    
    except Exception as e:
       print(f"Erro ao extrair título pelo tamanho da fonte: {e}")
       return ""

# Extrai autores
def extract_authors_and_affiliations(path):
    doc = pymupdf.open(path)
    pagina = doc[0]
    texto_inicio = pagina.get_text()
    texto_inicio = clean_text(texto_inicio)
    doc.close()

    linhas = texto_inicio.split('\n')
    
    # Encontra a linha com autores
    linha_autores = None
    for linha in linhas:
        if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+.*\d+', linha):
            linha_autores = linha
            break
    
    if not linha_autores:
        return [{"nome": "Revisar no PDF", "afiliacao": "Instituição não identificada", "orcid": "N/A"}]
    
    # Extrai autores da linha
    autores_temp = []
    partes = linha_autores.split(',')
    
    for parte in partes:
        parte = parte.strip()
        match = re.search(r'^(.+?)(\d+(?:,\d+)*)$', parte)
        if match:
            nome = match.group(1).strip()
            numeros = match.group(2).strip()
            autores_temp.append((nome, numeros))
    
    # Extrai instituições
    instituicoes = {}
    for linha in linhas:
        linha = linha.strip()
        if re.match(r'^\d+', linha) and ',' in linha and len(linha) < 200:
            if not re.match(r'^\d+\.', linha):
                match = re.match(r'^(\d+)([^,]+),\s*(.+)$', linha)
                if match:
                    num = match.group(1)
                    instituicao = match.group(2).strip()
                    pais = match.group(3).strip()
                    instituicoes[num] = f"{instituicao}, {pais}"
    
    # Associa autores às instituições
    autores = []
    for nome, numeros in autores_temp:
        lista_nums = numeros.split(',')
        afiliacoes = []
        for num in lista_nums:
            num = num.strip()
            if num in instituicoes:
                afiliacoes.append(instituicoes[num])
        
        if not afiliacoes:
            afiliacoes = ["Instituição não identificada"]
        
        autores.append({
            "nome": nome,
            "afiliacao": " / ".join(afiliacoes),
            "orcid": "N/A"
        })
    
    return autores if autores else [{"nome": "Revisar no PDF", "afiliacao": "Instituição não identificada", "orcid": "N/A"}]

# Extrai resumo
def extract_abstract(path):
    try:
        doc = pymupdf.open(path)

        abstract = extract_abstract_by_format(doc)

        doc.close()

        if abstract:
            if isinstance(abstract, list):
                abstract = " ".join(abstract)

            abstract = clean_text(abstract).strip()
            return abstract
        else:
            return ""

    except Exception as e:
        print(f"Erro ao extrair resumo: {e}")
        return ""

# Extrai resumo baseado no nome da seção
def extract_abstract_by_format(doc):
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

# Extrai palavras-chave / keywords
def extract_keywords(path):
    try:
        doc = pymupdf.open(path)
        
        keywords = extract_keywords_by_format(doc)
        
        doc.close()
        
        if keywords and isinstance(keywords, list):
            keywords = [clean_text(kw).strip() for kw in keywords if clean_text(kw).strip()]
        
        return keywords
    
    except Exception as e:
        print(f"Erro ao extrair palavras-chave: {e}")
        return ""

# Extrai palavras-chave baseado no nome da seção.
def extract_keywords_by_format(doc):
    try:
        keywords_parts = []
        found_keywords = False

        page = doc[0]
        blocks = page.get_text("dict")

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

                line_lower = line_text.lower()

                if not found_keywords:
                    if any(phrase in line_lower for phrase in ["palavras chaves"]):
                        found_keywords = True

                        for phrase in ["palavras chaves"]:
                          line_text = re.sub(re.escape(phrase), "", line_text, flags=re.IGNORECASE)

                        line_text = line_text.strip(".:; ")

                        if line_text:
                            keywords_list = split_keywords(line_text)
                            keywords_parts.extend(keywords_list)
                    continue
                
                if found_keywords:
                    if (line_lower.startswith(("1.introdu", "1. introdu", "I.introdu", "I. introdu")) or
                        any(phrase in line_lower for phrase in ["introdução", "Introdu"])):
                        return keywords_parts
                    
                    keywords_list = split_keywords(line_text)
                    keywords_parts.extend(keywords_list)
        
        return keywords_parts
    
    except Exception as e:
        print(f"Erro ao extrair palavras-chave: {e}")
        return []

def split_keywords(text):
    if not text:
        return []
    
    # Remove ponto final no final se existir
    text = text.rstrip('.')
    
    # Divide por vírgula
    keywords = [kw.strip() for kw in text.split(',')]
    
    # Remove qualquer keyword vazia
    keywords = [kw for kw in keywords if kw]
    
    return keywords

# Extrai referências
def extract_references(path):
    try:
        doc = pymupdf.open(path)

        references_parts = []
        found_references = False

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text = clean_text(text)

            if not found_references:
                ref_match = search_references_section(text)

                if ref_match is not None:
                    found_references = True
                    remaining_text = text[ref_match:]
                    references_parts.append(remaining_text)
            else:
                if is_next_section(text):
                    break
                references_parts.append(text)

        doc.close()

        if references_parts:
            full_references = '\n'.join(references_parts)
            return references_to_list(full_references)

        return []

    except Exception as e:
        print(f"Erro ao extrair referências: {e}")
        return []

def search_references_section(text):
    patterns = [
        r'Referências',
        r'Referencias',
        r'REFERÊNCIAS',
        r'REFERENCIAS',
        r'Referˆencias',
        r'References',
        r'REFERENCES',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.start()

    return None

def is_next_section(text):
    next_section_patterns = [
        r'^\s*(?:Apêndice|Appendix|Anexo|ANNEX|Glossário|Glossary)',
        r'^\s*\d+\.\s*(?:Apêndice|Appendix|Anexo)',
        r'^\s*[IVXLCDM]+\.\s*(?:Apêndice|Appendix)',
    ]

    text_start = text[:500]

    for pattern in next_section_patterns:
        if re.search(pattern, text_start, re.IGNORECASE | re.MULTILINE):
            return True

    return False

def references_to_list(references_text):
    if not references_text:
        return []

    references_text = re.sub(r'^Refer[\w]+\s*\n?', '', references_text, flags=re.IGNORECASE)
    references_text = re.sub(r'^Referˆencias\s*\n?', '', references_text, flags=re.IGNORECASE)
    references_text = re.sub(r'^References\s*\n?', '', references_text, flags=re.IGNORECASE)
    references_text = re.sub(r'-\n\s*', '', references_text, flags=re.IGNORECASE)

    lines = references_text.split('\n')

    ref_list = []
    current_ref = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue
        
        is_new_ref = re.match(r'^[A-ZÀ-ÖØ-Ý][^()]*?\(\d{4}\)\.', line, re.IGNORECASE)

        if is_new_ref:
            if current_ref:
                current_ref = re.sub(r'\s+', ' ', current_ref)
                ref_list.append(current_ref)
            current_ref = line
        else:
            if current_ref:
                current_ref += " " + line
            else:
                current_ref = line

    if current_ref:
        current_ref = re.sub(r'\s+', ' ', current_ref)
        ref_list.append(current_ref)

    return ref_list