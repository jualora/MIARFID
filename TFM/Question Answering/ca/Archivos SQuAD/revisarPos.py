import json

with open('SQuAD-v2.0-ca_small_train_pos.json') as f:
    data = json.load(f)

    for datos in data['data']:
        for muestra in datos['paragraphs']:
            parrafo = muestra['context']
            for qas in muestra['qas']:
                pregunta = qas['question']
                if len(qas['answers']) == 0:
                    for respuestaPlausible in qas['plausible_answers']:
                        if respuestaPlausible["answer_start"] == -1:
                            print("PARRAFO: \n")
                            print("--------------------\n")
                            print(parrafo)
                            print("\n\n")
                            print("PREGUNTA: \n")
                            print("--------------------\n")
                            print(pregunta)
                            print("\n\n")
                            print("RESPUESTA: \n")
                            print("--------------------\n")
                            print(respuestaPlausible["text"])
                            print("\n\n")
                else:
                    for answer in qas['answers']:
                        if answer["answer_start"] == -1:
                            print("PARRAFO: \n")
                            print("--------------------\n")
                            print(parrafo)
                            print("\n\n")
                            print("PREGUNTA: \n")
                            print("--------------------\n")
                            print(pregunta)
                            print("\n\n")
                            print("RESPUESTA: \n")
                            print("--------------------\n")
                            print(answer["text"])
                            print("\n\n")