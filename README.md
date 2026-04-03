# STIL 2021 - Corpus Processing

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
