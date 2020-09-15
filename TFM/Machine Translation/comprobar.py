import os

def palabras(x):
    return x.split(' ')

frasesEn = open('./ParaProcesar/frases.en').readlines()
frasesEs = open('./ParaProcesar/frases.es').readlines()

frasesPalEn = list(map(lambda x:palabras(x), frasesEn))
frasesPalEs = list(map(lambda x:palabras(x), frasesEs))

print(list(map(len, frasesPalEn)).index(max(map(len, frasesPalEn))))
print(list(map(len, frasesPalEs)).index(max(map(len, frasesPalEs))))

print(max(map(len, frasesPalEn)))
print(max(map(len, frasesPalEs)))
