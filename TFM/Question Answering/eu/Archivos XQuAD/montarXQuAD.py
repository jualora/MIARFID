import json

## EMPAREJAMOS LOS PÁRRAFOS ##

parrafosEs = open('contextosXQuAD.txt').readlines()
parrafosEu = open('contextosXQuAD_eu.txt').readlines()
parrafos = []

for i in range(len(parrafosEs)):
    parrafoEs = parrafosEs[i]
    parrafoEu = parrafosEu[i]
    while parrafoEs[-1] == '\n':
        parrafoEs = parrafoEs[:-1]
    while parrafoEu[-1] == '\n':
        parrafoEu = parrafoEu[:-1]
    parrafos.append((parrafoEs,parrafoEu))

## EMPAREJAMOS LAS PREGUNTAS ##

preguntasEs = open('preguntasXQuAD.txt').readlines()
preguntasEu = open('preguntasXQuAD_eu.txt').readlines()
preguntas = []

for i in range(len(preguntasEs)):
    preguntaEs = preguntasEs[i]
    preguntaEu = preguntasEu[i]
    while preguntaEs[-1] == '\n':
        preguntaEs = preguntaEs[:-1]
    while preguntaEu[-1] == '\n':
        preguntaEu = preguntaEu[:-1]
    preguntas.append((preguntaEs,preguntaEu))

## EMPAREJAMOS LAS RESPUESTAS ##

respuestasEs = open('respuestasXQuAD.txt').readlines()
respuestasEu = open('respuestasXQuAD_eu.txt').readlines()
respuestas = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaEu = respuestasEu[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaEu[-1] == '\n':
        respuestaEu = respuestaEu[:-1]
    respuestas.append((respuestaEs,respuestaEu))

## MONTAMOS UNA PRIMERA INSTANCIA DEL DATASET SIN LAS POSICIONES ##

with open('xquad.eu.json', 'r') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            if len(parrafos) == 1:
                print(muestra['context'])
                print(parrafos[0])
            muestra['context'] = parrafos[0][1]
            parrafos.pop(0)
            for qas in muestra['qas']:
                qas['question'] = preguntas[0][1]
                preguntas.pop(0)
                for answer in qas['answers']:
                    answer['text'] = respuestas[0][1]
                    respuestas.pop(0)
                    answer['answer_start'] = -1

with open('xquad.eu.revisar.json', 'w') as f:    
    f.write(json.dumps(data))