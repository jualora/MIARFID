import sys
import os 
import matplotlib as plt
import numpy as np  
from numpy import linalg as LA              
import matplotlib.pyplot as plt   
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score
from eigenfaces import read_pgm, procesarDatos, PCA, kvecino

##El primer argumento del script es el parámetro k del algoritmo de 
##k-vecinos más cercanos. El segundo es la reducción PCA que se va aplicar previa a LDA.
v = int(sys.argv[1])
d_pca = int(sys.argv[2])

##Definimos un método para PCA donde le pasamos los datos (entrenamiento y test), 
##la lista Nc con el número de muestras por clase y la reducción que 
##le queremos aplicar, devolviéndonos los datos con la dimensionalidad reducida.
def LDA(x_training, x_test, Nc, d_):
    #Calculamos el vector promedio
    mu = np.mean(x_training, axis=1)
    
    #Calculamos la matriz de medias por clase
    mu_c = []
    for i, nc in enumerate(Nc):
        j=nc
        while j>0:
            mu_c.append(x_training[:,i*nc:(i*nc)+nc].mean(axis=1))
            j-=1
    mu_c = np.matrix(np.array(mu_c)).T
    if mu_c.shape[1]==1:
        mu_c = mu_c.T

    #Calculamos la matriz entre-clases Sb (d x d)
    Sb = mu_c - mu
    nc = np.mean(Nc)
    Sb = nc * Sb * Sb.T
    
    #Obtenemos la matriz intra-clases Sw (d x d)
    Sw = x_training - mu_c
    Sw = Sw * Sw.T
   
    #Calculamos la matriz de covarianzas, que en este caso es el resultado
    #de multiplicar la inversa de Sw por Sb
    C = LA.inv(Sw)*Sb

    #Calculamos los eigevalues y los eigenvectores de la matriz de covarianzas.
    delta, B = LA.eigh(C)

    #Ordenamos los eigenvectores y eigenvalues
    ordenados = np.flip(np.argsort(delta))
    delta = delta[ordenados]
    B = B[:,ordenados] 

    #Aplicamos la reducción con los d_ primeros eigenvectores
    Bd = B[:,:d_]
    Bdt = Bd.T
    x_training_red = Bdt * x_training
    x_test_red = Bdt * x_test

    return x_training_red, x_test_red

##Implementamos FisherFaces, haciendo previamente una reducción con PCA.
x_training, y_training, x_test, y_test, Nc = procesarDatos()
precisiones = []
reduccionesLDA = [i for i in np.arange(5, 205, 5)]
for d_lda in reduccionesLDA:
    x_training_pca, x_test_pca = PCA(x_training, x_test, d_pca)
    x_training_lda, x_test_lda = LDA(x_training_pca, x_test_pca, Nc, d_lda)
    precision = kvecino(v, x_training_lda, y_training, x_test_lda, y_test)
    precisiones.append(precision)

max_precision = max(precisiones)
indice = precisiones.index(max_precision)
mejor_reduccion = reduccionesLDA[indice]
print("Con una reducción previa de PCA de %d, la mejor reducción con LDA es %d, obteniendo una precision de %f" % (d_pca, mejor_reduccion, max_precision))
title = "Reducción PCA+LDA y Clasificación con "+str(v)+"-NN"
plt.title(title)
plt.plot(reduccionesLDA, precisiones)
plt.xlabel("Valor de d' para LDA con una reducción previa de %d con PCA" % d_pca)
plt.ylabel("Precisión (%)")
nombre = "Resultados_PCA_LDA_"+str(v)+"nn.png"
plt.savefig(nombre)



