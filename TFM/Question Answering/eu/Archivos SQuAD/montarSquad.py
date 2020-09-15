import json

## EMPAREJAMOS LOS TITULOS ##

titulosEs = open('titulosSQuAD.txt').readlines()
titulosEu = open('titulosSQuAD_eu.txt').readlines()
titulos = []

for i in range(len(titulosEs)):
    tituloEs = titulosEs[i]
    tituloEu = titulosEu[i]
    if tituloEs[-1] == '\n':
        tituloEs = tituloEs[:-1]
    if tituloEu[-1] == '\n':
        tituloEu = tituloEu[:-1]
    titulos.append((tituloEs,tituloEu))

## EMPAREJAMOS LOS PÁRRAFOS ##

parrafosEs = open('contextosSQuAD.txt').readlines()
parrafosEu = open('contextosSQuAD_eu.txt').readlines()
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

preguntasEs = open('preguntasSQuAD.txt').readlines()
preguntasEu = open('preguntasSQuAD_eu.txt').readlines()
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

respuestasEs = open('respuestasSQuAD.txt').readlines()
respuestasEu = open('respuestasSQuAD_eu.txt').readlines()
respuestas = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaEu = respuestasEu[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaEu[-1] == '\n':
        respuestaEu = respuestaEu[:-1]
    respuestas.append((respuestaEs,respuestaEu))

## EMPAREJAMOS LAS RESPUESTAS PLAUSIBLES ##

respuestasEs = open('respuestasPlausiblesSQuAD.txt').readlines()
respuestasEu = open('respuestasPlausiblesSQuAD_eu.txt').readlines()
respuestasPlausibles = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaEu = respuestasEu[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaEu[-1] == '\n':
        respuestaEu = respuestaEu[:-1]
    respuestasPlausibles.append((respuestaEs,respuestaEu))

## MONTAMOS UNA PRIMERA INSTANCIA DEL DATASET SIN LAS POSICIONES ##

with open('SQuAD-v2.0-eu_small_train.json', 'r') as f:
    data = json.load(f)

    for datos in data['data']:
        datos['title'] = titulos[0][1]
        titulos.pop(0)
        for muestra in datos['paragraphs']:
            muestra['context'] = parrafos[0][1]
            parrafos.pop(0)
            for qas in muestra['qas']:
                qas['question'] = preguntas[0][1]
                preguntas.pop(0)
                if len(qas['answers']) == 0:
                    for respuestaPlausible in qas['plausible_answers']:
                        respuestaPlausible['text'] = respuestasPlausibles[0][1]
                        respuestasPlausibles.pop(0)
                        respuestaPlausible['answer_start'] = -1
                else:
                    for answer in qas['answers']:
                        answer['text'] = respuestas[0][1]
                        respuestas.pop(0)
                        answer['answer_start'] = -1
    
with open('SQuAD-v2.0-eu_small_train.json', 'w') as f:    
    f.write(json.dumps(data))

