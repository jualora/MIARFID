import os
import openpyxl
import matplotlib.pyplot as plt
from translate.storage.tmx import tmxfile

for base, dirs, files in os.walk("./ParaProcesar"):
    datasets = files

datasetCa = datasets[0]
datasetEs = datasets[1]
data_path_Ca = "./ParaProcesar/"+datasetCa
data_path_Es = "./ParaProcesar/"+datasetEs
frases = []
name_dataset = data_path_Ca[15:-9]

frasesCa = open(data_path_Ca).readlines()
frasesEs = open(data_path_Es).readlines()

for i in range(len(frasesCa)):
    frases.append((frasesEs[i][:-1], frasesCa[i][:-1]))

menor10 = 0
menor20 = 0
menor30 = 0
menor40 = 0
menor50 = 0
menor60 = 0
menor70 = 0
menor80 = 0
menor90 = 0
for i in range(len(frases)):
    palabras = frases[i][1].split(' ')
    if len(palabras) <= 10:
        menor10 += 1
    elif len(palabras) <= 20:
        menor20 += 1
    elif len(palabras) <= 30:
        menor30 += 1
    elif len(palabras) <= 40:
        menor40 += 1
    elif len(palabras) <= 50:
        menor50 += 1
    elif len(palabras) <= 60:
        menor60 += 1
    elif len(palabras) <= 70:
        menor70 += 1
    elif len(palabras) <= 80:
        menor80 += 1
    elif len(palabras) <= 90:
        menor90 += 1

x = [menor10, menor20 ,menor30, menor40, menor50, menor60, menor70, menor80, menor90]

excel = openpyxl.load_workbook('Palabras por Frase.xlsx')
sheet = excel.get_sheet_by_name('Hoja1')

j = 2
for i in range(len(x)):
    sheet.cell(row = 44, column = j).value = x[i]
    j += 1

excel.save('Palabras por Frase.xlsx')