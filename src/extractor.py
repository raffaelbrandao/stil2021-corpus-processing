import pymupdf
import os
import re
import unicodedata
from pathlib import Path

def list_docs(path):
    docs = []
    if not os.path.exists(path):
        return docs
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            docs.append(os.path.join(path, file))
    return sorted(docs)

def extract_text(path):
    try:
        doc = pymupdf.open(path)
        full_text = "".join([page.get_text() for page in doc])
        doc.close()
        return full_text
    except Exception:
        return ""

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def build_doc_url(filename):
    doc_id = filename.split('-')[0]
    return f"https://sol.sbc.org.br/index.php/stil/article/view/{doc_id}"

def extract_title(path):
    try:
        doc = pymupdf.open(path)
        first_page = doc[0]
        blocks = first_page.get_text("dict")
        font_map = {}
        for block in blocks.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_size = span.get("size", 0)
                    text = span.get("text", "").strip()
                    if text and len(text) > 3:
                        font_map.setdefault(font_size, []).append(text)
        doc.close()
        if not font_map: return "Título não identificado"
        max_font = max(font_map.keys())
        return " ".join(font_map[max_font]).strip()
    except:
        return "Título não identificado"

def extract_abstract(texto_inicio):
    texto_busca = clean_text(texto_inicio)
    padroes = [
        r'Resumo\s*[:\.\-]?\s*(.*?)\s*(?:Abstract|Palavras[-\s]chave|Keywords|1\.\s+Introdução)',
        r'Abstract\s*[:\.\-]?\s*(.*?)\s*(?:Keywords|1\.\s+Introduction)'
    ]
    for padrao in padroes:
        match = re.search(padrao, texto_busca, re.IGNORECASE | re.DOTALL)
        if match: return match.group(1).strip()
    
    paragrafos = [p for p in texto_busca.split('. ') if 100 < len(p) < 1500]
    return paragrafos[0] + "." if paragrafos else "Não identificado"

def extract_keywords(texto_inicio):
    texto_busca = clean_text(texto_inicio)
    padroes = [
        r'Palavras[-\s]chave\s*[:\.]?\s*(.*?)\s*(?:Abstract|Keywords|1\.)',
        r'Keywords\s*[:\.]?\s*(.*?)\s*(?:Resumo|1\.)'
    ]
    for padrao in padroes:
        match = re.search(padrao, texto_busca, re.IGNORECASE | re.DOTALL)
        if match:
            raw = re.sub(r'[^\w\s,;\.-]', '', match.group(1))
            return [k.strip().lower() for k in re.split(r'[,;\.]', raw) if len(k.strip()) > 2]
    return []

def extract_references(texto_completo):
    texto_busca = clean_text(texto_completo)
    ref_match = re.search(r'(?:Referências|References)\s*(.*?)(?:\Z|$)', texto_busca, re.IGNORECASE | re.DOTALL)
    if ref_match:
        conteudo_ref = ref_match.group(1)
        referencias_raw = re.split(r'\[\d+\]|\d+\.', conteudo_ref)
        return [r.strip() for r in referencias_raw if len(r.strip()) > 20][:15]
    return []

def extrair_dados_estatisticos(caminho_pdf, processador):
    doc = pymupdf.open(caminho_pdf)
    primeira_pagina = doc[0]
    blocos = primeira_pagina.get_text("blocks")
    
    texto_inicio = ""
    for i in range(min(2, len(doc))):
        texto_inicio += doc[i].get_text() + "\n"
    
    texto_completo = extract_text(caminho_pdf)
    titulo = extract_title(caminho_pdf)

    # --- LÓGICA DE AUTORES CORRIGIDA ---
# Função: Extrai autores e afiliações
def extract_authors_and_affiliations(texto_inicio):
    """Extrai autores e afiliações do artigo"""
    linhas = texto_inicio.split('\n')
    
    # Encontra a linha com autores
    linha_autores = None
    for linha in linhas:
        if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+.*\d+', linha):
            linha_autores = linha
            break
    
    if not linha_autores:
        return []
    
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

    # --- FIM DA LÓGICA DE AUTORES ---refactor: lista authors and relantionship

    resumo = extract_abstract(texto_inicio)
    keywords = extract_keywords(texto_inicio)
    referencias = extract_references(texto_completo)
    filename = Path(caminho_pdf).name
    url = build_doc_url(filename)

    try:
        res_nlp = processador.process(texto_completo)
    except:
        res_nlp = {'tokens': texto_completo.split()[:100], 'pos_tags': [], 'lemmas': []}

    doc.close()

    return {
        "titulo": titulo,
        "informacoes_url": url,
        "idioma": "Português",
        "storage_key": f"files/{filename}",
        "autores": autores_final,
        "data_publicacao": "2021",
        "resumo": resumo,
        "keywords": keywords,
        "referencias": referencias,
        "artigo_completo": texto_completo,
        "artigo_tokenizado": res_nlp['tokens'],
        "pos_tagger": res_nlp['pos_tags'],
        "lema": res_nlp['lemmas']
    }
# --- EXECUÇÃO DO LOOP (EXEMPLO) ---
# lista_artigos = list_docs("caminho/para/seu/diretorio")
# corpus_final_ufba = []
# 
# for caminho in lista_artigos:
#     try:
#         print(f"\n📄 Processando: {Path(caminho).name}")
#         dados = extrair_dados_estatisticos(caminho, processador)
#         corpus_final_ufba.append(dados)
#         
#         print(f"   📌 Título: {dados['titulo'][:70]}...")
#         print(f"   📝 Resumo: {dados['resumo'][:100]}...")
#         print(f"   🏷️ Keywords: {', '.join(dados['keywords'][:3]) if dados['keywords'] else 'Não identificadas'}")
#         
#     except Exception as e:
#         print(f"   ❌ Erro: {e}")
# 
# print(f"\n✅ Concluído! {len(corpus_final_ufba)} artigos processados.")
