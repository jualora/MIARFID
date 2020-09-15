import nltk
import math
import matplotlib.pyplot as plt
from nltk.corpus import cess_esp
from nltk.tag import hmm
from nltk.tag import tnt
from nltk.tag import AffixTagger
from nltk.tag import DefaultTagger
from nltk.tag import brill, brill_trainer
from nltk.tag import UnigramTagger
from nltk.tag.perceptron import PerceptronTagger
from nltk.tbl.template import Template
from time import time
from random import shuffle

from pyfreeling import Analyzer
from lxml import etree

"""def procesarFrases(ls):
    res = ''
    for s in ls:
        for w in s:
            res += "palabra "+w.get_form()+"\n"
            res += " Possible analysis: {"
            for a in w:
                res += " ("+a.get_lemma()+","+a.get_tag()+")"
            res += " }\n"
            res += " Selected Analysis: ("+w.get_lemma()+","+w.get_tag()+")"
        print("\n")
    return res"""

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

    # Evaluamos su tasa de acierto sobre "test"
    evaluated = tagger_hmm.evaluate(test)
    return evaluated
    # print("Tasa de acierto con HMM: %s" % (evaluated))


def tntTest(train, test):
    # Lo entrenamos
    tagger_tnt = tnt.TnT()
    tagger_tnt.train(train)

    # Evaluamos su tasa de acierto sobre "test"
    evaluated = tagger_tnt.evaluate(test)
    return evaluated
    # print("Tasa de acierto con TNT: %s" % (evaluated))


if __name__ == "__main__":
    """
    # Tarea 1
    
    # Obtener corpus
    corpus = cess_esp.tagged_sents()

    # Reducir corpus
    corpus = reducirCorpus(corpus)

    number_sentences = len(corpus)
    hmm_barajado = []
    intervalosConfianza = []

    print("CORPUS BARAJADO:")
    shuffle(corpus)
    for i in range(10):
        # Separar corpus entre entrenamiento y test
        train = corpus[:i*number_sentences//10] + \
            corpus[i*number_sentences//10+number_sentences//10:]
        test = corpus[i*number_sentences//10:i *
                      number_sentences//10+number_sentences//10]

        n = len(test)

        print("  Cogiendo como test la parte %s/10 de la lista de oraciones:" % (i+1))
        evaluated = hmmTest(train, test)
        hmm_barajado.append(evaluated)
        intervalosConfianza.append(1.96*math.sqrt(evaluated*(1-evaluated)/n))
        print("    Tasa de acierto con HMM: %s con un intervalo de confianza de ±%s" %
              (evaluated, intervalosConfianza[-1]))

    # HMM BARAJADO
    y = hmm_barajado
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición como test')
    plt.title('Validación HMM con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()"""
    

    # Tarea 2
    '''
    # Obtener corpus
    corpus = cess_esp.tagged_sents()

    # Reducir corpus
    corpus = reducirCorpus(corpus)
    
    number_sentences = len(corpus)
    hmm_barajado = []
    intervalosConfianza = []

    print("CORPUS BARAJADO:")
    shuffle(corpus)

    corpusPartido = []
    for i in range(10):
        corpusPartido.append(
            corpus[i*number_sentences//10:(i+1)*number_sentences//10])

    print("  Cogiendo como test la parte 10/10 de la lista de oraciones:")
    test = corpusPartido.pop()
    train = []
    for c in corpusPartido:
        train += c
        evaluated = hmmTest(train, test)
        hmm_barajado.append(evaluated)
        n = len(test)
        intervalosConfianza.append(1.96*math.sqrt(evaluated*(1-evaluated)/n))
        print("    Tasa de acierto con HMM: %s con un intervalo de confianza de ±%s entrenando hasta la parte %s." %
              (evaluated, intervalosConfianza[-1], len(hmm_barajado)))

    y = hmm_barajado
    x = [i for i in range(len(y))]
    plt.axis([-1, 10, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Partición añadida como entrenamiento')
    plt.title('Validación HMM incremental con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()
    '''

    # Tarea 3
    '''
    # Obtener corpus
    corpus = cess_esp.tagged_sents()

    # Reducir corpus
    corpus = reducirCorpus(corpus)
    
    number_sentences = len(corpus)

    shuffle(corpus)
    medias_final = []
    intervalosConfianza = []
    n = 0

    for j in [0, 1, 2, 3, 4]:
        results_tnt = []
        start_time = time()
        for i in range(10):
            # Separar corpus entre entrenamiento y test
            train = corpus[:i*number_sentences//10] + \
                corpus[i*number_sentences//10+number_sentences//10:]
            test = corpus[i*number_sentences//10:i *
                          number_sentences//10+number_sentences//10]

            sufix_tagger = AffixTagger(train, affix_length=-j)
            tnt_tagger = tnt.TnT(N=100, unk=sufix_tagger, Trained=True)
            tnt_tagger.train(train)
            results_tnt.append(tnt_tagger.evaluate(test))
            n = len(test)
        evaluated = sum(results_tnt)/len(results_tnt)
        medias_final.append(evaluated)
        intervalosConfianza.append(1.96*math.sqrt(evaluated*(1-evaluated)/n))
        print("Media con %s sufijo(s): %s" %
              (j, medias_final[-1]))
        elapsed_time = time() - start_time
        print("Tiempo con %s sufijo(s): %0.10f seconds." %
              (j, elapsed_time))
    y = medias_final
    x = [i for i in range(5)]
    plt.axis([-1, 5, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Número de caracteres por sufijo')
    plt.title('Validación cruzada TNT y AffixTagger con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()
    '''

    # Tarea 4
    """
    # Obtener corpus
    corpus = cess_esp.tagged_sents()

    # Reducir corpus
    corpus = reducirCorpus(corpus)
    
    shuffle(corpus)

    medias_final = []
    number_sentences = len(corpus)
    n = 0

    for j in ["perceptron", "brillUnigram", "brillHMM", "tnt", "hmm"]:
        results = []
        start_time = time()
        for i in range(10):
            # Separar corpus entre entrenamiento y test
            train = corpus[:i*number_sentences//10] + \
                corpus[i*number_sentences//10+number_sentences//10:]
            test = corpus[i*number_sentences//10:i *
                          number_sentences//10+number_sentences//10]
            n = len(test)

            if j is "brillUnigram":
                Template._cleartemplates()
                templates = [Template(brill.Pos([-1])), Template(brill.Pos([-1]), brill.Word([0]))]
                tagger_brill_uni = brill_trainer.BrillTaggerTrainer(UnigramTagger(train), templates, trace=3).train(train)
                eval_brill_uni = tagger_brill_uni.evaluate(test)
                print("Brill con UniTagger, subconjunto: %s evaluación: %f" % (i, eval_brill_uni))
                results.append(eval_brill_uni)

            if j is "brillHMM":
                Template._cleartemplates()
                templates = [Template(brill.Pos([-1])), Template(brill.Pos([-1]), brill.Word([0]))]
                tagger_brill_hmm = brill_trainer.BrillTaggerTrainer(hmm.HiddenMarkovModelTagger.train(train), templates, trace=3).train(train)
                eval_brill_hmm = tagger_brill_hmm.evaluate(test)
                print("Brill con HMMTagger, subconjunto: %s evaluación: %f" % (i, eval_brill_hmm))
                results.append(eval_brill_hmm)

            if j is "hmm":
                evaluated = hmmTest(train, test)
                results.append(evaluated)
                print("HMM, subconjunto: %s evaluación: %f" % (i, evaluated))
                
            if j is "tnt":
                evaluated = tntTest(train, test)
                results.append(evaluated)
                print("TNT, subconjunto: %s evaluación: %f" % (i, evaluated))
            
            if j is "perceptron":
                pt = PerceptronTagger(load=False)
                pt.train(train)
                evaluated = pt.evaluate(test)
                results.append(evaluated)
                print("Perceptron, subconjunto: %s evaluación: %f" % (i, evaluated))

        medias_final.append(sum(results)/len(results))
        print("Media con %s: %s" %
              (j, medias_final[-1]))
        elapsed_time = time() - start_time
        print("Tiempo con %s: %0.10f seconds." %
              (j, elapsed_time))

    y = medias_final
    intervalosConfianza = []
    for evaluated in y:
        intervalosConfianza.append(1.96*math.sqrt(evaluated*(1-evaluated)/n))
    x = ["Perceptron", "BrillUnigram", "BrillHMM", "TNT", "HMM"]
    plt.axis([-1, 5, 0.80, 1.00])
    plt.ylabel('Tasa de acierto')
    plt.xlabel('Etiquetador a evaluar')
    plt.title('Validación cruzada de etiquetadores con diez particiones barajadas')
    plt.plot(x, y, 'ro')
    plt.errorbar(x, y, yerr=intervalosConfianza, linestyle='None')
    plt.show()"""
    

    # Tarea 6
    
    analyzer = Analyzer(config='es.cfg', lang='es')

    in_file = open("./Alicia_utf8.txt", "rb")
    bytes_file = in_file.read()
    in_file.close()

    xml = analyzer.run(bytes_file)

    """res = procesarFrases(etree.tostring(xml))

    file = open("./resultadosFreeling.txt", "w")
    file.write(res)
    file.close()"""

    print(etree.tostring(xml))
