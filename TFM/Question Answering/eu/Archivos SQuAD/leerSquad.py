import json

with open('SQuAD-v2.0-es_small_train.json') as f:
    data = json.load(f)

    titulos = []
    parrafos = []
    preguntas = []
    respuestas = []
    respuestasPlausibles = []
    
    for datos in data['data']:
        titulos.append(datos['title'])
        for muestra in datos['paragraphs']:
            parrafos.append(muestra['context'])
            for qas in muestra['qas']:
                preguntas.append(qas['question'])
                if len(qas['answers']) == 0:
                    for respuestaPlausible in qas['plausible_answers']:
                        respuestasPlausibles.append(respuestaPlausible['text'])
                else:
                    for answer in qas['answers']:
                        respuestas.append(answer['text'])
    
with open('titulosSQuAD.txt', "w") as f:
    for titulo in titulos:
        linea = titulo + '\n'
        f.write(linea) 

with open('contextosSQuAD.txt', "w") as f:
    for contexto in parrafos:
        linea = contexto + '\n'
        f.write(linea) 

with open('preguntasSQuAD.txt', "w") as f:
    for pregunta in preguntas:
        linea = pregunta + '\n'
        f.write(linea) 

with open('respuestasSQuAD.txt', "w") as f:
    for respuesta in respuestas:
        linea = respuesta + '\n'
        f.write(linea)

with open('respuestasPlausiblesSQuAD.txt', "w") as f:
    for respuesta in respuestasPlausibles:
        linea = respuesta + '\n'
        f.write(linea)
