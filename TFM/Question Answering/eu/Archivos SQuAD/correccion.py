preguntasEs = open('preguntasSQuAD.txt').readlines()
preguntasEu = open('preguntasSQuAD_eu.txt').readlines()

intrusos = []

for i in range(len(preguntasEs)):
    if preguntasEs[i]==preguntasEu[i]:
        intrusos.append(preguntasEu[i])

with open("aRevisar.txt", "w") as f:
    for muestra in preguntasEu:
        if muestra in intrusos:
            f.write(muestra)
        else:
            f.write("1\n")

muestras = open("aRevisar.txt").readlines()

with open("aRevisarPreguntas.txt", "w") as f:
    for muestra in muestras:
        if muestra!='1\n':
            f.write(muestra)