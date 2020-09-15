import json

def noRespuestaIntegra(res, pos, contexto):
    n = len(res)
    if contexto[pos:pos+n] != res:
        return True
    else:
        return False

with open('SQuAD-v2.0-eu_small_train_revisado.json') as f:
    data = json.load(f)

    titulos = []
    parrafos = []
    preguntas = []
    respuestas = []
    respuestasPlausibles = []
    
    for datos in data['data']:
        for muestra in datos['paragraphs']:
            for qas in muestra['qas']:
                pregunta = qas['question']
                qas_id = qas['id']
                if len(qas['answers']) == 0:
                    for answer in qas['plausible_answers']:
                        if qas_id == '56d4e0e92ccc5a1400d832dc':
                            answer['answer_start'] = 429
                            answer['text'] = 'Jean-Michel Basquiat'
                else:
                    for answer in qas['answers']:
                        if qas_id == '56d4e0e92ccc5a1400d832dc':
                            answer['answer_start'] = 429
                            answer['text'] = 'Jean-Michel Basquiat'

with open('SQuAD-v2.0-eu_small_train_revisado.json', 'w') as f:    
    f.write(json.dumps(data))