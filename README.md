# STIL 2021 Corpus Processing

Processamento de corpus textual utilizando PyMuPDF e Stanza para NLP.

> Extração de informações e análise estatística de 30 artigos em português brasileiro do STIL 2021 utilizando Stanza (NLP para português).

**Disciplina:** PGCOMP/IC0058 - TÓPICOS EM BANCO DE DADOS II - T01 (2026.1)

**Instituição:** Universidade Federal da Bahia (UFBA)

**Programa:** PGCOMP - Programa de Pós-Graduação em Computação

---

## 📌 Sobre o Projeto

Este projeto tem como objetivo a extração e análise de informações de **30 artigos científicos** publicados no **STIL 2021** (Simpósio Brasileiro de Tecnologia da Informação e da Linguagem Humana), utilizando técnicas de Processamento de Linguagem Natural (PLN).

Os artigos são processados para gerar um dataset estruturado em JSON, contendo metadados e informações linguísticas para análise estatística.

---

## 🎯 Objetivos

- Extrair texto completo de artigos em PDF
- Realizar tokenização dos textos
- Aplicar POS Tagging (classificação de classes gramaticais)
- Realizar lematização das palavras
- Gerar estatísticas linguísticas do corpus
- Criar visualizações (nuvem de palavras)
- Estruturar os dados no formato JSON conforme template definido

---

## 📊 Estatísticas Extraídas

| Estatística | Descrição |
|-------------|-----------|
| Total de Tokens | Número total de palavras no artigo |
| Total de Types | Número de palavras únicas no artigo |
| Quantidade de Sentenças | Número de frases no artigo |
| Quantidade de Verbos | Total de verbos (classe VERB) |
| Quantidade de Substantivos | Total de substantivos (NOUN + PROPN) |
| Quantidade de Adjetivos | Total de adjetivos (classe ADJ) |
| Quantidade de Lemas | Número de lemas únicos |
| Top 10 Palavras | Palavras mais frequentes (stopwords mantidas) |

---

## 📋 Pré-requisitos

- **Python 3.11** (recomendado - compatível com PyTorch)
  > ⚠️ Python 3.14+ tem problemas de compatibilidade com PyTorch/Stanza
- Windows / Linux / Mac

## 🚀 Instalação

### 1. Verificar/Instalar Python 3.11 (Windows)

```bash
# Verificar versões instaladas
py --list

# Instalar Python 3.11 (se não tiver)
py install 3.11
```

### 2. Criar ambiente virtual com Python 3.11

```bash
# Criar ambiente
py -3.11 -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ou no Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências

#### Instalar PyTorch (compatível com Windows/CPU)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

##### Instalar outras bibliotecas

```bash
pip install PyMuPDF stanza pandas numpy tqdm
```

### 4. Verificar instalação

```bash
python -c "import pymupdf, stanza, torch; print('✅ Todos os módulos carregados!')"
```

### 5. Configurar Jupyter Notebook

#### Instalar kernel do ambiente
```bash
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name="Python 3.11 (STIL)"
```

No notebook, selecione o kernel:

- Kernel → Change kernel → Python 3.11 (STIL)

#### Importações no notebook
```bash
# Célula 1: Verificar ambiente
import sys
print(f"Python: {sys.version}")

# Célula 2: Imports principais
import pymupdf
import stanza
import torch

# Célula 3: Módulos do projeto
import sys
sys.path.append('..')

from src.extractor import list_docs
from src.processor import NPLProcessor

print("✅ Módulos carregados com sucesso!")
```

## ⚠️ Problemas comuns e soluções

### Erro: ModuleNotFoundError: No module named 'pymupdf'

```bash
%pip install PyMuPDF
import pymupdf
```

### Erro: WinError 1114 (DLL falhou)

**Causa**: Python 3.14+ incompatível com PyTorch

**Solução**: Usar Python 3.11 (seguir instalação acima)

### Erro: ModuleNotFoundError: No module named 'stanza'

```bash
%pip install stanza
```

### Aviso: pymupdf.exe not on PATH

**Ignorar** - não afeta o funcionamento do PyMuPDF no notebook.

## 📂 Estrutura e organização do projeto
```bash
stil2021-corpus-processing/
├── data/
│   ├── raw/           # Coloque os artigos em PDFs aqui
│   ├── processed/     # Arquivos gerados no template JSON para cada artigo
│   └── output/        # dataset final, unico e completo do processamento
├── notebooks/
│   └── processamento.ipynb
├── src/
│   ├── extractor.py   # Extração de textos dos PDFs
│   └── processor.py   # Processamento NLP com Stanza
└── README.md
```

### Como organizar seus arquivos

#### 1. Adicionar documentos para processamento

Coloque todos os seus arquivos PDF (ou outros formatos suportados) na pasta data/raw/:

```bash
# Exemplo de estrutura
data/
└── raw/
    ├── artigo_1.pdf
    ├── artigo_2.pdf
    ├── artigo_3.pdf
    └── ...
```

#### 2. Arquivos processados

- **data/processed/** - Armazena arquivos no template JSON gerados durante o processamento (ex: textos extraídos, dados serializados)
- **data/output/** - Contém os resultados finais (ex: JSON com lemas, POS tags, análises estatísticas)

> 💡 Dica: As pastas processed/ e output/ podem ser recriadas automaticamente pelo código se não existirem.

## 📦 Dependências principais
|Biblioteca |	Versão | Uso |
|-------------|-----------|-----------|
|PyMuPDF | 1.27.2+ | Leitura de PDF/documentos |
|Stanza | latest | NLP, lematização |
|PyTorch | 2.8.0+	| Backend do Stanza |
|pandas	| latest	| Manipulação de dados |

## 🎯 Teste rápido
```bash
import pymupdf
import stanza
import torch

# Testar PyMuPDF
doc = pymupdf.open()
page = doc.new_page()
page.insert_text((50, 50), "Teste")
print(f"✓ PyMuPDF: {pymupdf.__doc__.split(':')[0]}")

# Testar PyTorch
print(f"✓ PyTorch: {torch.__version__}")

# Baixar modelo Stanza (primeira execução)
stanza.download('pt')
print("✓ Stanza configurado")

doc.close()
```

## 📝 Observações finais
- Python 3.11 é a versão recomendada para este projeto
- O warning sobre pymupdf.exe no PATH pode ser ignorado
- Em caso de erros de DLL, verifique o Microsoft Visual C++ Redistributable
- ⚠️ Importante: A primeira vez que você executar stanza.download('pt') ou carregar o modelo em português, o download pode demorar alguns minutos (cerca de 700MB a 1GB). As execuções subsequentes serão rápidas, pois o modelo fica em cache local

## 🤝 Contribuição
Para contribuir com o projeto, mantenha o ambiente Python 3.11 para evitar problemas de compatibilidade.
