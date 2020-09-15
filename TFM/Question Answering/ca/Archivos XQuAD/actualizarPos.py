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

with open('xquad.es.json') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            for qas in muestra['qas']:
                for answer in qas['answers']:
                    posEs.append(answer['answer_start'])
    
posCa = []

with open('xquad.ca.json') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            parrafo = muestra['context']
            for qas in muestra['qas']:
                for answer in qas['answers']:
                    respuesta = answer['text']
                    n = parrafo.count(respuesta)
                    if n>1:
                        parrafoAux = parrafo
                        for i in range(n):
                            posCa.append(parrafoAux.find(respuesta))
                            parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                        dif = 1000
                        posDef = -1
                        for pos in posCa:
                            if dif > abs(pos - posEs[0]):
                                posDef = pos
                                dif = abs(pos - posEs[0])
                        posEs.pop(0)
                        posCa = []
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
                                posCa.append(parrafoAux.find(respuesta))
                                parrafoAux = parrafoAux.replace(respuesta, '<VISTO>', 1)
                            dif = 1000
                            posDef = -1
                            for pos in posCa:
                                if dif > abs(pos - posEs[0]):
                                    posDef = pos
                                    dif = abs(pos - posEs[0])
                            posEs.pop(0)
                            posCa = []
                            answer['answer_start'] = posDef
                        else:
                            answer['answer_start'] = parrafo.find(respuesta)
                            posEs.pop(0)

with open('xquad.ca.pos.json', 'w') as f:    
    f.write(json.dumps(data))  