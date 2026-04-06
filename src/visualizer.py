# Geração de nuvens de palavras
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

#  Gera nuvem de palavras para cada documento
def generate_word_cloud(tokens, filename, output):
    os.makedirs(output, exist_ok=True)
    
    text = ' '.join(tokens)
    
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        max_words=200,
        colormap='viridis'
    ).generate(text)
    
    path = os.path.join(output, f"{filename}.png")
    
    wordcloud.to_file(path)
    
    return path

#  Gera nuvem de palavras para todo o corpus
def generate_corpus_cloud(tokens, output):
    os.makedirs(output, exist_ok=True)
    
    text = ' '.join(tokens)
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        max_words=200,
        colormap='viridis'
    ).generate(text)
    
    path = os.path.join(output, "corpus_stil_2021.png")
    wordcloud.to_file(path)
    
    return path

# Exibe uma nuvem de palavras
def cloud_show(path):
    from PIL import Image
    
    img = Image.open(path)
    plt.figure(figsize=(15, 8))
    plt.imshow(img, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def generate_and_display_corpus_cloud(tokens, output):
    os.makedirs(output, exist_ok=True)
    
    texto = ' '.join(tokens)
    
    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='white',
        max_words=200,
        colormap='viridis'
    ).generate(texto)
    
    path = os.path.join(output, "corpus_stil_2021.png")
    wordcloud.to_file(path)
    
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('NUVEM DE PALAVRAS - CORPUS COMPLETO STIL 2021', fontsize=20)
    plt.show()
    
    return path