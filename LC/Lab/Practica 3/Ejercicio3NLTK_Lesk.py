import nltk
""" nltk.download('wordnet')
nltk.download('stopwords') """
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

def wsd_lesk(frase, palabra):
    sentidos=wn.synsets(palabra)
    mejor_sentido = sentidos[0]
    max_overlap = 0
    stopWords = set(sw.words('english'))
    contexto = set(frase.split(" "))
    contexto = contexto.difference(stopWords)
    
    for sentido in sentidos[1:]:
        data = set((sentido.definition()+" "+" ".join(sentido.examples())).split(" "))
        data = data.difference(stopWords)
        overlap = len(contexto.intersection(data))
        if overlap > max_overlap:
            max_overlap = overlap
            mejor_sentido = sentido
    
    return mejor_sentido


if __name__ == '__main__':
    frase = "Yesterday I went to the bank to withdraw the money and the credit card did not work"
    palabra = "bank"

    print(wsd_lesk(frase, palabra))