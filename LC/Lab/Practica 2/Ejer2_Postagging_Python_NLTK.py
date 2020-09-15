import nltk
import numpy as np
import math
#nltk.download('cess_esp')
from nltk.corpus import cess_esp
from nltk.tag import hmm
from nltk.tag import tnt
from random import shuffle
import matplotlib.pyplot as plt

corpus = cess_esp.tagged_sents()

def eval_HMM_cross_validation(barajado):
    if(barajado):
        shuffle(res)
    k=10
    tamParticion = int(len(res)/k)
    particiones = [res[i*tamParticion: i*tamParticion+tamParticion] for i in range(k)]
    precisionesHMM = []
    intervalosHMM = []

    for i in range(0,len(particiones)):
        aux = particiones.copy()
        test = aux.pop(i)
        train = []

        for particion in aux:
            train += particion

        n = len(test)

        tagger_hmm = hmm.HiddenMarkovModelTagger.train(train)
        evaluacion = tagger_hmm.evaluate(test)
        print("El modelo HMM da un porcentaje de acierto de ", evaluacion*100, "% ")
        precisionesHMM.append(evaluacion)
        intervalosHMM.append(1.96*math.sqrt((1-evaluacion)*evaluacion/n))

    x = [0,1,2,3,4,5,6,7,8,9]
    y = precisionesHMM
    y_ = intervalosHMM
    plt.axis([-1, 10, 0.80, 0.97])
    plt.ylabel("Precision")
    plt.xlabel('Partición')
    if(barajado):
        plt.title("10-fold Cross Validation HMM con barajado")
    else:
        plt.title("10-fold Cross Validation HMM sin barajado")
    plt.errorbar(x, y, yerr=y_, linestyle='None', marker='o', ecolor='red')
    plt.show()

def eval_TNT_cross_validation(barajado):
    if(barajado):
        shuffle(res)
    k=10
    tamParticion = int(len(res)/k)
    particiones = [res[i*tamParticion: i*tamParticion+tamParticion] for i in range(k)]
    precisionesTNT = []
    intervalosTNT = []

    for i in range(0,len(particiones)):
        aux = particiones.copy()
        test = aux.pop(i)
        train = []

        for particion in aux:
            train += particion

        n = len(test)

        tagger_tnt = tnt.TnT()
        tagger_tnt.train(train)
        evaluacion = tagger_tnt.evaluate(test)
        print("El modelo TNT da un porcentaje de acierto de ", evaluacion*100, "%")
        precisionesTNT.append(evaluacion)
        intervalosTNT.append(1.96*math.sqrt((1-evaluacion)*evaluacion/n))

    x = [0,1,2,3,4,5,6,7,8,9]
    y = precisionesTNT
    y_ = intervalosTNT
    plt.axis([-1, 10, 0.80, 0.97])
    plt.ylabel("Precision")
    plt.xlabel('Partición')
    if(barajado):
        plt.title("10-fold Cross Validation TNT con barajado")
    else:
        plt.title("10-fold Cross Validation TNT sin barajado")
    plt.errorbar(x, y, yerr=y_, linestyle='None', marker='o', ecolor='red')
    plt.show()

if __name__ == '__main__':
    #Ejercicio 1
    res = []
    for frase in corpus:
        frase_reducida = []
        for palabra, categoria in frase:
            if palabra!='*0*' and categoria[0:2]!='sn':
                if categoria[0] != 'v' or categoria[0]!='F':
                    frase_reducida.append((palabra, categoria[0:2]))
                else:
                    frase_reducida.append((palabra, categoria[0:3]))
        res.append(frase_reducida)
    
    longitud = int(len(res)*0.9)

    train = res[:longitud]
    test = res[longitud:]

    print("Introduzca (0) si desea hacer un uso de etiquetadores morfosintacticos con la partición de entrenamiento previamente establecida (Ejercicio 2) o (1) para hacer una evaluación 10-fold cross validation (Ejercicio 3)")
    ejer = int(input())

    if ejer==0:
        #Ejercicio 2
        results = []
        intervalos = []
        n=len(test)
        tagger_hmm = hmm.HiddenMarkovModelTagger.train(train)
        evaluacion = tagger_hmm.evaluate(test)
        print("El modelo HMM da un porcentaje de acierto de ", evaluacion*100, "%")
        results.append(evaluacion)
        intervalos.append(1.96*math.sqrt((1-evaluacion)*evaluacion/n))

        tagger_tnt = tnt.TnT()
        tagger_tnt.train(train)
        evaluacion = tagger_tnt.evaluate(test)
        print("El modelo TNT da un porcentaje de acierto de ", evaluacion*100, "%")
        results.append(evaluacion)
        intervalos.append(1.96*math.sqrt((1-evaluacion)*evaluacion/n))

        x = ["HMM", "TNT"]
        y = results
        y_ = intervalos
        plt.axis([-1, 10, 0.70, 0.97])
        plt.ylabel("Precision")
        plt.xlabel('Modelo empleado')
        plt.title("Etiquetador morfosintáctico con HMM y TNT")
        plt.errorbar(x, y, yerr=y_, linestyle='None', marker='o', ecolor='red')
        plt.show()
    elif ejer==1:
        #Ejercicio 3
        print("Introduzca (0) para realizar una evaluación por HMM o (1) por TNT")
        evaluation = int(input())
        print("Introduzca (0) para realizar las particiones con el corpus original reducido o (1) si prefiere hacer un barajado de este")
        aux = int(input())
        if aux==0:
            barajado = False
        elif aux==1:
            barajado = True
        if evaluation==0:
            eval_HMM_cross_validation(barajado)
        elif evaluation==1:
            eval_TNT_cross_validation(barajado)


    


