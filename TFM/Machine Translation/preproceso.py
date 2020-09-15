## COGER LAS FRASES DE LOS DATASETS ##

# EN EL CASO DEL CATALÁN #

import os
from translate.storage.tmx import tmxfile

frases = []

for base, dirs, files in os.walk("./ParaProcesar"):
    datasets = files

print(datasets)
datasetCa = datasets[0]
datasetEs = datasets[1]
data_path_Ca = "./ParaProcesar/"+datasetCa
data_path_Es = "./ParaProcesar/"+datasetEs
frases = []
name_dataset = data_path_Ca[15:-9]

print(name_dataset)

frasesCa = open(data_path_Ca).readlines()
frasesEs = open(data_path_Es).readlines()

for i in range(len(frasesCa)):
    frases.append((frasesEs[i][:-1], frasesCa[i][:-1]))

frasesTrain = frases[:19431]
frasesDev = frases[19431:20250]
frasesTest = frases[20250:20454]

resInputTrain = ""
resOutputTrain = ""
resInputDev = ""
resOutputDev = ""
resInputTest = ""
resOutputTest = ""

for frase in frasesTrain:
    resInputTrain += frase[0]
    resOutputTrain += frase[1]
    if frase is not frasesTrain[-1]:
        resInputTrain += '\n'
        resOutputTrain += '\n'

for frase in frasesDev:
    resInputDev += frase[0]
    resOutputDev += frase[1]
    if frase is not frasesDev[-1]:
        resInputDev += "\n"
        resOutputDev += "\n"

for frase in frasesTest:
    resInputTest += frase[0]
    resOutputTest += frase[1]
    if frase is not frasesTest[-1]:
        resInputTest += "\n"
        resOutputTest += "\n"

with open("./datasets/100K_20w_s/es-ca/trainEs/train"+name_dataset+".es", "w") as f:
    f.write(resInputTrain)

with open("./datasets/100K_20w_s/es-ca/trainCa/train"+name_dataset+".ca", "w") as f:
    f.write(resOutputTrain)

with open("./datasets/100K_20w_s/es-ca/devEs/dev"+name_dataset+".es", "w") as f:
    f.write(resInputDev)

with open("./datasets/100K_20w_s/es-ca/devCa/dev"+name_dataset+".ca", "w") as f:
    f.write(resOutputDev)

with open("./datasets/100K_20w_s/es-ca/testEs/test"+name_dataset+".es", "w") as f:
    f.write(resInputTest)

with open("./datasets/100K_20w_s/es-ca/testCa/test"+name_dataset+".ca", "w") as f:
    f.write(resOutputTest)

# EN EL CASO DEL ESPAÑOL Y EL EUSKERA #

import os
from translate.storage.tmx import tmxfile

for base, dirs, files in os.walk("./ParaProcesar"):
    datasets = files

dataset = datasets[0]
data_path = "./ParaProcesar/"+dataset
frases = []
name_dataset = data_path[15:-10]

print(name_dataset)

with open(data_path, 'rb') as fin:
    tmx_file = tmxfile(fin, 'en', 'es')

for node in tmx_file.unit_iter():
    palabras = node.gettarget().split(' ')
    if len(palabras) <= 20:
        frases.append((node.getsource(), node.gettarget()))

print("Hay %d frases en este dataset" % len(frases))

frasesTrain = frases[:13520]
frasesDev = frases[13520:20280]
frasesTest = frases[20280:27040]

resInputTrain = ""
resOutputTrain = ""
resInputDev = ""
resOutputDev = ""
resInputTest = ""
resOutputTest = ""

for frase in frasesTrain:
    resInputTrain += frase[0]
    resOutputTrain += frase[1]
    if frase is not frasesTrain[-1]:
        resInputTrain += '\n'
        resOutputTrain += '\n'

for frase in frasesDev:
    resInputDev += frase[0]
    resOutputDev += frase[1]
    if frase is not frasesDev[-1]:
        resInputDev += "\n"
        resOutputDev += "\n"

for frase in frasesTest:
    resInputTest += frase[0]
    resOutputTest += frase[1]
    if frase is not frasesTest[-1]:
        resInputTest += "\n"
        resOutputTest += "\n"

with open("./datasets/500K_max_20w_s/en-es/trainEn/train"+name_dataset+".en", "w") as f:
    f.write(resInputTrain)

with open("./datasets/500K_max_20w_s/en-es/trainEs/train"+name_dataset+".es", "w") as f:
    f.write(resOutputTrain)

with open("./datasets/500K_max_20w_s/en-es/devEn/dev"+name_dataset+".en", "w") as f:
    f.write(resInputDev)

with open("./datasets/500K_max_20w_s/en-es/devEs/dev"+name_dataset+".es", "w") as f:
    f.write(resOutputDev)

with open("./datasets/500K_max_20w_s/en-es/testEn/test"+name_dataset+".en", "w") as f:
    f.write(resInputTest)

with open("./datasets/500K_max_20w_s/en-es/testEs/test"+name_dataset+".es", "w") as f:
    f.write(resOutputTest)

## UNIR LAS FRASES ESCOGIDAS EN UN MISMO FICHERO ##

import os
import sys

fichero = sys.argv[1]
idioma = sys.argv[2]

for base, dirs, files in os.walk("./datasets/100K_20w_s/"+idioma+"/"+fichero+"/"):
    datasets = files
res = ""
for i in range(len(datasets)):
    frases = open("./datasets/100K_20w_s/"+idioma+"/"+fichero+"/"+datasets[i]).readlines()
    for frase in frases:
        res += frase
        if frase == frases[-1]:
            res += '\n'
lan = fichero[-2:].lower()
fichero = fichero[:-2]
with open("./datasets/100K_20w_s/"+idioma+"/"+fichero+"."+lan, "w") as f:
    f.write(res)