import json

def obtenNGramas(listaPalabras, n):
    return [listaPalabras[i:i+n] for i in range(len(listaPalabras)-(n-1))]

def distanceLevenshtein(str1, str2):
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

posEs = []

with open('SQuAD-v2.0-es_small_train.json') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            for qas in muestra['qas']:
                if len(qas['answers']) == 0:
                    for respuestaPlausible in qas['plausible_answers']:
                        posEs.append(respuestaPlausible['answer_start'])
                else:
                    for answer in qas['answers']:
                        posEs.append(answer['answer_start'])

posEu = []

with open('SQuAD-v2.0-eu_small_train.json') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            parrafo = muestra['context']
            for qas in muestra['qas']:
                if len(qas['answers']) == 0:
                    for respuestaPlausible in qas['plausible_answers']:
                        respuesta = respuestaPlausible['text']
                        n = parrafo.count(respuesta)
                        if n>1:
                            parrafoAux = parrafo
                            for i in range(n):
                                posEu.append(parrafoAux.find(respuesta))
                                parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                            dif = 1000
                            posDef = -1
                            for pos in posEu:
                                if dif > abs(pos - posEs[0]):
                                    posDef = pos
                                    dif = abs(pos - posEs[0])
                            posEs.pop(0)
                            posEu = []
                            respuestaPlausible['answer_start'] = posDef
                        elif n==1:
                            respuestaPlausible['answer_start'] = parrafo.find(respuesta)
                            posEs.pop(0)
                        else:
                            m = len(respuesta.split(' '))
                            posiblesRespuestas = obtenNGramas(parrafo.split(' '), m)
                            distL = 10000000
                            for posibleRespuesta in posiblesRespuestas:
                                if distL > distanceLevenshtein(' '.join(posibleRespuesta), respuesta):
                                    distL = distanceLevenshtein(' '.join(posibleRespuesta), respuesta)
                                    candidata = posibleRespuesta
                            candidata = ' '.join(candidata)
                            respuestaPlausible['text'] = candidata
                            respuesta = respuestaPlausible['text']
                            n = parrafo.count(respuesta)
                            if n>1:
                                parrafoAux = parrafo
                                for i in range(n):
                                    posEu.append(parrafoAux.find(respuesta))
                                    parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                                dif = 1000
                                posDef = -1
                                for pos in posEu:
                                    if dif > abs(pos - posEs[0]):
                                        posDef = pos
                                        dif = abs(pos - posEs[0])
                                posEs.pop(0)
                                posEu = []
                                respuestaPlausible['answer_start'] = posDef
                            else:
                                respuestaPlausible['answer_start'] = parrafo.find(respuesta)
                                posEs.pop(0)
                else:
                    for answer in qas['answers']:
                        respuesta = answer['text']
                        n = parrafo.count(respuesta)
                        if n>1:
                            parrafoAux = parrafo
                            for i in range(n):
                                posEu.append(parrafoAux.find(respuesta))
                                parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                            dif = 1000
                            posDef = -1
                            for pos in posEu:
                                if dif > abs(pos - posEs[0]):
                                    posDef = pos
                                    dif = abs(pos - posEs[0])
                            posEs.pop(0)
                            posEu = []
                            answer['answer_start'] = posDef
                        elif n==1:
                            answer['answer_start'] = parrafo.find(respuesta)
                            posEs.pop(0)
                        else:
                            m = len(respuesta.split(' '))
                            posiblesRespuestas = obtenNGramas(parrafo.split(' '), m)
                            distL = 10000000
                            for posibleRespuesta in posiblesRespuestas:
                                if distL > distanceLevenshtein(' '.join(posibleRespuesta), respuesta):
                                    distL = distanceLevenshtein(' '.join(posibleRespuesta), respuesta)
                                    candidata = posibleRespuesta
                            candidata = ' '.join(candidata)
                            answer['text'] = candidata
                            respuesta = answer['text']
                            n = parrafo.count(respuesta)
                            if n>1:
                                parrafoAux = parrafo
                                for i in range(n):
                                    posEu.append(parrafoAux.find(respuesta))
                                    parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                                dif = 1000
                                posDef = -1
                                for pos in posEu:
                                    if dif > abs(pos - posEs[0]):
                                        posDef = pos
                                        dif = abs(pos - posEs[0])
                                posEs.pop(0)
                                posEu = []
                                answer['answer_start'] = posDef
                            else:
                                answer['answer_start'] = parrafo.find(respuesta)
                                posEs.pop(0)

with open('SQuAD-v2.0-eu_small_train_pos.json', 'w') as f:    
    f.write(json.dumps(data))  