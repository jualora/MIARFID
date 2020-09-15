import json

with open('xquad.es.json') as f:
    data = json.load(f)

    parrafos = []
    preguntas = []
    respuestas = []

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            parrafos.append(muestra['context'])
            for qas in muestra['qas']:
                preguntas.append(qas['question'])
                for answer in qas['answers']:
                    respuestas.append(answer['text'])

with open('contextosXQuAD.txt', "w") as f:
    for contexto in parrafos:
        linea = contexto + '\n'
        f.write(linea) 

with open('preguntasXQuAD.txt', "w") as f:
    for pregunta in preguntas:
        linea = pregunta + '\n'
        f.write(linea) 

with open('respuestasXQuAD.txt', "w") as f:
    for respuesta in respuestas:
        linea = respuesta + '\n'
        f.write(linea)
