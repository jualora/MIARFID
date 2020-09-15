from googletrans import Translator

translator = Translator()

muestras = open('preguntasSQuAD.txt').readlines()

i = 40874

with open("preguntasSQuAD_eu_2.txt", "w") as f:
    for muestra in muestras[40874:]:
        result = translator.translate(muestra[:-1], src='es', dest='eu').text
        trad = result + '\n'
        f.write(trad)
        print(i)
        i+=1