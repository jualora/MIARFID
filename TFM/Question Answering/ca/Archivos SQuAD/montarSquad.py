import json

## EMPAREJAMOS LOS TITULOS ##

titulosEs = open('titulosSQuAD.txt').readlines()
titulosCa = open('titolsSQuAD.txt').readlines()
titulos = []

for i in range(len(titulosEs)):
    tituloEs = titulosEs[i]
    tituloCa = titulosCa[i]
    if tituloEs[-1] == '\n':
        tituloEs = tituloEs[:-1]
    if tituloCa[-1] == '\n':
        tituloCa = tituloCa[:-1]
    titulos.append((tituloEs,tituloCa))

## EMPAREJAMOS LOS PÁRRAFOS ##

parrafosEs = open('contextosSQuAD.txt').readlines()
parrafosCa = open('contextosSQuAD_ca.txt').readlines()
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

preguntasEs = open('preguntasSQuAD.txt').readlines()
preguntasCa = open('preguntesSQuAD.txt').readlines()
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

respuestasEs = open('respuestasSQuAD.txt').readlines()
respuestasCa = open('respostesSQuAD.txt').readlines()
respuestas = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaCa = respuestasCa[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaCa[-1] == '\n':
        respuestaCa = respuestaCa[:-1]
    respuestas.append((respuestaEs,respuestaCa))

## EMPAREJAMOS LAS RESPUESTAS PLAUSIBLES ##

respuestasEs = open('respuestasPlausiblesSQuAD.txt').readlines()
respuestasCa = open('respostesPlausiblesSQuAD.txt').readlines()
respuestasPlausibles = []

for i in range(len(respuestasEs)):
    respuestaEs = respuestasEs[i]
    respuestaCa = respuestasCa[i]
    while respuestaEs[-1] == '\n':
        respuestaEs = respuestaEs[:-1]
    while respuestaCa[-1] == '\n':
        respuestaCa = respuestaCa[:-1]
    respuestasPlausibles.append((respuestaEs,respuestaCa))

## MONTAMOS UNA PRIMERA INSTANCIA DEL DATASET SIN LAS POSICIONES ##

with open('SQuAD-v2.0-ca_small_train.json', 'r') as f:
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
    
with open('SQuAD-v2.0-ca_small_train.json', 'w') as f:    
    f.write(json.dumps(data))

