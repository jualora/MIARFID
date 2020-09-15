import json

def noRespuestaIntegra(res, pos, contexto):
    n = len(res)
    if contexto[pos:pos+n] != res:
        return True
    else:
        return False

with open('xquad.eu.json') as f:
    data = json.load(f)

    titulos = []
    parrafos = []
    preguntas = []
    respuestas = []
    respuestasPlausibles = []
    
    for datos in data['data']:
        for muestra in datos['paragraphs']:
            context_text = muestra['context']
            for qas in muestra['qas']:
                pregunta = qas['question']
                qas_id = qas['id']
                for answer in qas['answers']:
                    answer_text = answer['text']
                    answer_position = answer['answer_start']
                    if noRespuestaIntegra(answer_text, answer_position, context_text):
                        if context_text.count(answer_text) == 1:
                            answer['answer_start'] = context_text.index(answer_text)
                        elif context_text.count(answer_text) > 1:
                            n = context_text.count(answer_text)
                            parrafoAux = context_text
                            posiblesPos = []
                            for i in range(n):
                                posiblesPos.append(parrafoAux.find(answer_text))
                                j = len(answer_text)
                                cadVista = ''
                                for k in range(j):
                                    cadVista += '<'
                                parrafoAux = parrafoAux.replace(answer_text, cadVista, 1)
                            dif = 1000
                            posDef = -1
                            posActual = answer_position
                            for pos in posiblesPos:
                                if dif > abs(pos - posActual):
                                    posDef = pos
                                    dif = abs(pos - posActual)
                            answer['answer_start'] = posDef

with open('xquad.eu.revisado.json', 'w') as f:    
    f.write(json.dumps(data))