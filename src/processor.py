# Processamento NLP com Stanza
import stanza
from collections import Counter

# Classe para processamento de texto
class NLPProcessor:
    def __init__(self):
        print("Carregando o modelo do Stanza para português...")
        self.nlp = stanza.Pipeline('pt', processors='tokenize,mwt,pos,lemma', verbose=False)
        print("Modelo carregado com sucesso.")
    
    def process(self, text):
        doc = self.nlp(text)
        
        tokens = []
        pos_tags = []
        lemmas = []
        sentences = []
        
        for sentence in doc.sentences:
            sentences.append(sentence.text)

            for word in sentence.words:
                tokens.append(word.text)
                pos_tags.append(word.upos)
                lemmas.append(word.lemma)
        
        return {
            'tokens': tokens,
            'pos_tags': pos_tags,
            'lemmas': lemmas,
            'sentences': sentences
        }
    
    # Calcula estatísticas
    def calculate_statistics(self, tokens, pos_tags, lemmas, sentences):
        # Quantidade de tokens
        total_tokens = len(tokens)
        # Quantidade de tipos
        total_types = len(set(tokens)) 
        # Quantidade de sentenças
        total_sentences = len(sentences)

        # Classe gramatical
        pos_counts = Counter(pos_tags)
        # Quantidade de verbos
        total_verbs = pos_counts.get('VERB', 0)
        # Quantidade de substantivos
        total_nouns = pos_counts.get('NOUN', 0) + pos_counts.get('PROPN', 0)
        # Quantidade de adjetivos
        total_adjectives = pos_counts.get('ADJ', 0)
        
        # Quantidade de lemas únicos
        total_lemmas = len(set(lemmas))
        
        # Lista das 10 palavras mais comum com stopwords
        token_frequency = Counter([token.lower() for token in tokens])
        top10_list = token_frequency.most_common(10)
        
        return {
            'total_tokens': total_tokens,
            'total_types': total_types,
            'total_sentences': total_sentences,
            'total_verbs': total_verbs,
            'total_nouns': total_nouns,
            'total_adjectives': total_adjectives,
            'total_lemmas': total_lemmas,
            'top10_list': top10_list
        }