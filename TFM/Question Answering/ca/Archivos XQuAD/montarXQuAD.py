import json

## EMPAREJAMOS LOS PÁRRAFOS ##

parrafosEs = open('contextosXQuAD.txt').readlines()
parrafosCa = open('contextosXQuAD_ca.txt').readlines()
parrafos = []

for i in range(len(parrafosEs)):
    parrafoEs = parrafosEs[i]
    parrafoCa = parrafosCa[i]
    while parrafoEs[-1] == '\n':
        parrafoEs = parrafoEs[:-1]
    while parrafoCa[-1] == '\n':
        parrafoCa = parrafoCa[:-1]
    parrafos.append((parrafoEs,parrafoCa))

## EMPAREJAMOS LAS PREGUNTAS ##

preguntasEs = open('preguntasXQuAD.txt').readlines()
preguntasCa = open('preguntesXQuAD.txt').readlines()
preguntas = []

for i in range(len(preguntasEs)):
    preguntaEs = preguntasEs[i]
    preguntaCa = preguntasCa[i]
    while preguntaEs[-1] == '\n':
        preguntaEs = preguntaEs[:-1]
    while preguntaCa[-1] == '\n':
        preguntaCa = preguntaCa[:-1]
    preguntas.append((preguntaEs,preguntaCa))

## EMPAREJAMOS LAS RESPUESTAS ##

respuestasEs = open('respuestasXQuAD.txt').readlines()
respuestasCa = open('respostesXQuAD.txt').readlines()
respuestas = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaCa = respuestasCa[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaCa[-1] == '\n':
        respuestaCa = respuestaCa[:-1]
    respuestas.append((respuestaEs,respuestaCa))

## MONTAMOS UNA PRIMERA INSTANCIA DEL DATASET SIN LAS POSICIONES ##

with open('xquad.ca.json', 'r') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            muestra['context'] = parrafos[0][1]
            parrafos.pop(0)
            for qas in muestra['qas']:
                qas['question'] = preguntas[0][1]
                preguntas.pop(0)
                for answer in qas['answers']:
                    answer['text'] = respuestas[0][1]
                    respuestas.pop(0)
                    answer['answer_start'] = -1

with open('xquad.ca.revisar.json', 'w') as f:    
    f.write(json.dumps(data))