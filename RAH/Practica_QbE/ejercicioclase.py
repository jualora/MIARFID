# -*- coding: utf-8 -*-

import numpy as np
from sys import *
from distances import get_distance_matrix
from matplotlib.pyplot import matshow, show, cm, plot

def lee_fichero(fichero):
	matriz=[]
	fichero=open(fichero,"r")
	lineas=fichero.readlines()
	matriz=[linea.split() for linea in lineas] 
	fichero.close()
	return np.array(matriz).astype(np.float)

#Implementar a partir de aqui
#sintaxis get_distance_matrix:
#distancias=get_distance_matrix(npmatriz1,npmatriz2,'cos')
#donde npmatriz1 y npmatriz2 son los vectores de características de los dos audios

query = lee_fichero("./mfc_queries/SEG-0062.mfc.raw")
audio = lee_fichero("largo250000.mfc.raw")

d = get_distance_matrix(query,audio,'cos')

m = np.zeros((len(query),len(audio),4))

for j in range(len(audio)):
	m[0][j][0] = d[0][j] #Coste
	m[0][j][1] = 1 #Longitud del camino
	m[0][j][2] = j #De donde vengo
	m[0][j][3] = d[0][j] #Normalización->Coste/Longitud

for i in range(1, len(query)-1):
	m[i][0][0] = d[i][0] + m[i-1][0][0] #Coste
	m[i][0][1] = i #Longitud del camino
	m[i][0][2] = 0 #De donde vengo
	m[i][0][3] = m[i][0][0]/m[i][0][1] #Normalización->Coste/Longitud

for j in range(1, len(audio)):
	for i in range(1, len(query)):
		triple = ((m[i-1][j][0]+d[i][j])/(m[i-1][j][1]+1), (m[i][j-1][0]+d[i][j])/(m[i][j-1][1]+1), (m[i-1][j-1][0]+d[i][j])/(m[i-1][j-1][1]+1)) 

		if min(triple)==triple[0]:
			m[i][j][0] = d[i][j] + m[i-i][j][0] #Coste
			m[i][j][2] = m[i-1][j][2] #De donde vengo
		elif min(triple)==triple[1]:
			m[i][j][0] = d[i][j] + m[i][j-1][0] #Coste
			m[i][j][2] = m[i][j-1][2] #De donde vengo
		elif min(triple)==triple[2]:
			m[i][j][0] = d[i][j] + m[i-1][j-1][0] #Coste
			m[i][j][2] = m[i-1][j-1][2] #De donde vengo

		m[i][j][1] = i #Longitud del camino
		m[i][j][3] = m[i][j][0]/m[i][j][1] #Normalización->Coste/Longitud


resultado = [m[len(query)-1][j][3] for j in range(1, len(audio))]
minimo = min(resultado)
indice = resultado.index(minimo)
i=len(query)-1
j = indice
while i>0:
	j = m[i][j][2]
	j = int(j)
	i-=1
print("El origen es %d, el final es %d, el coste es %.5f " %(j, indice, minimo))


		
		
	

