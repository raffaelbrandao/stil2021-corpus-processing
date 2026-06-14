#!/bin/bash
# Script de Finetuning do Qwen 2.5 1.5B para Classificação de Estilos
echo "========================================="
echo "FINETUNING QWEN 2.5 1.5B - ESTILOS DE ESCRITA"
echo "========================================="

# Criar modelo base com configurações
echo "1. Criando modelo base com configurações personalizadas..."
ollama create qwen-styles-base -f ./Modelfile

# Para finetuning real, use o comando:
# ollama finetune qwen-styles-base --data ./train.jsonl --output qwen-styles-finetuned

echo ""
echo "2. Opções de Finetuning:"
echo "   a) Via API do Ollama (se disponível):"
echo "      ollama finetune qwen-styles-base --data ./train.jsonl --output qwen-styles-finetuned"
echo ""
echo "   b) Via LoRA com script Python:"
echo "      python finetune_lora.py"
echo ""
echo "   c) Testar com few-shot prompting:"
echo "      python test_fewshot.py"

echo ""
echo "Modelo base criado: qwen-styles-base"
echo "Para testar: ollama run qwen-styles-base"
