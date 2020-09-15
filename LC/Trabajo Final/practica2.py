#!/usr/bin/python3

import nltk
import math
from nltk.corpus import cess_esp
from nltk.tag import hmm, tnt
from random import shuffle
import matplotlib.pyplot as plt

# nltk.download('cess_esp')


def reducirCorpus(corpus_original):
    # Eliminar equiquetas > 2 y verbos > 3 caracteres
    # Eliminar anotaciones (u'*0*', u'sn')
    corpus = []
    for frase in corpus_original:
        # Por cada frase

        corpus.append([])
        for palabra, etiqueta in frase:
            # Por cada palabra

            if palabra == "*0*":
                # Si palabra es u'*0*'
                pass
            elif etiqueta[0] in ["v", "F"]:
                # Si es verbo o signo de puntuación
                corpus[-1].append((palabra, etiqueta[:3]))
            else:
                # Si es caracter
                corpus[-1].append((palabra, etiqueta[:2]))
    return corpus


def hmmTest(train, test):
    # Lo entrenamos
    tagger_hmm = hmm.HiddenMarkovModelTagger.train(train)
    """
    # Etiquetamos las palabras de la frase 0
    tagged_0 = tagger_hmm.tag([(w, c)[0] for (w, c) in test[0]])
    print(tagged_0)
    """
    # Evaluamos su tasa de acierto sobre "test"
    evaluated = tagger_hmm.evaluate(test)
    return evaluated
    # print("Tasa de acierto con HMM: %s" % (evaluated))


def tntTest(train, test):
    # Lo entrenamos
    tagger_tnt = tnt.TnT()
    tagger_tnt.train(train)
    """
    # Etiquetamos las palabras de la frase 0
    tagged_0 = tagger_tnt.tag([(w, c)[0] for (w, c) in test[0]])
    print(tagged_0)
    """
    # Evaluamos su tasa de acierto sobre "test"
    evaluated = tagger_tnt.evaluate(test)
    return evaluated
    # print("Tasa de acierto con TNT: %s" % (evaluated))


if __name__ == "__main__":

    # Obtener corpus
    corpus = cess_esp.tagged_sents()

    # Reducir corpus
    corpus = reducirCorpus(corpus)

    """
    # Separar corpus entre entrenamiento y test
    number_sentences = len(corpus)
    train = corpus[:9*number_sentences//10]
    test = corpus[9*number_sentences//10:]

    # Etiquetador hmm
    print(hmmTest(train, test))

    # Etiquetador tnt
    print(tntTest(train, test))
    """

    number_sentences = len(corpus)
    hmm_sin_barajar = []
    tnt_sin_barajar = []
    print("CORPUS SIN BARAJAR:")
    for i in range(10):
        # Separar corpus entre entrenamiento y test
        train = corpus[:i*number_sentences//10] + \
            corpus[i*number_sentences//10+number_sentences//10:]
        test = corpus[i*number_sentences//10:i *
                      number_sentences//10+number_sentences//10]

        print("  Cogiendo como test la parte %s de la lista de oraciones:" % (i+1))
        evaluated = hmmTest(train, test)
        hmm_sin_barajar.append(evaluated)
        print("    Tasa de acierto con HMM: %s" % (evaluated))
        evaluated = tntTest(train, test)
        tnt_sin_barajar.append(evaluated)
        print("    Tasa de acierto con TNT: %s" % (evaluated))

    hmm_barajado = []
    tnt_barajado = []
    print("CORPUS BARAJADO:")
    shuffle(corpus)
    for i in range(10):
        # Separar corpus entre entrenamiento y test
        train = corpus[:i*number_sentences//10] + \
            corpus[i*number_sentences//10+number_sentences//10:]
        test = corpus[i*number_sentences//10:i *
                      number_sentences//10+number_sentences//10]

        print("  Cogiendo como test la parte %s de la lista de oraciones:" % (i+1))
        evaluated = hmmTest(train, test)
        hmm_barajado.append(evaluated)
        print("    Tasa de acierto con HMM: %s" % (evaluated))
        evaluated = tntTest(train, test)
        tnt_barajado.append(evaluated)
        print("    Tasa de acierto con TNT: %s" % (evaluated))

    n = len(test)  # sum([len(frase) for frase in test])
    # HMM SIN BARAJAR
    y = hmm_sin_barajar
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición como test')
    plt.title('Validación HMM con diez particiones sin barajar')
    plt.plot(x, y, 'ro')
    intervalosConfianza = []
    for p in y:
        intervalosConfianza.append(1.96*math.sqrt(p*(1-p)/n))
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()

    # HMM BARAJADO
    y = hmm_barajado
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición como test')
    plt.title('Validación HMM con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    intervalosConfianza = []
    for p in y:
        intervalosConfianza.append(1.96*math.sqrt(p*(1-p)/n))
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()

    # TNT SIN BARAJAR
    y = tnt_sin_barajar
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición como test')
    plt.title('Validación TNT con diez particiones sin barajar')
    plt.plot(x, y, 'ro')
    intervalosConfianza = []
    for p in y:
        intervalosConfianza.append(1.96*math.sqrt(p*(1-p)/n))
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()

    # TNT BARAJADO
    y = tnt_barajado
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición como test')
    plt.title('Validación TNT con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    intervalosConfianza = []
    for p in y:
        intervalosConfianza.append(1.96*math.sqrt(p*(1-p)/n))
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()
