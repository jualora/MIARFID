#PROBLEMA DE LAS CARTAS CON ALGORITMOS GENÉTICOS
#Tenemos una baraja de 10 cartas del mismo palo, numeradas del 1 al 10 sin repeticiones.
#Hay que separarlas en 2 pilas, de modo que en una el sumatorio de las cartas se acerque lo máximo posible a 36 y en la otra el productorio se acerque lo máximo a 360
import random
from random import randint
import time

def iniciarPopulacho(pobIni):
    #Creamos la población inicial.
    pueblo = []
    while len(pueblo)<pobIni:
        tupla = ([], [])
        i = 1
        while i<11:
            aleatorio = randint(0,1)
            if aleatorio==0:
                tupla[0].append(i)
            else:
                tupla[1].append(i)
            i += 1
        if tupla not in pueblo:
            pueblo.append(tupla)
    return pueblo

def aptitud(individuo):
    #La función fitness f(x,y) que hemos definido es, suponiendo "x" la suma de la primera pila de cartas del individuo, e "y" el productorio del segundo:
    #f(x,y) = Valor absoluto(36-x) + Valor absoluto(360-y)
    #De esta forma, el fitness óptimo es 0 cuando "x" es 36 e "y" es 360.
    
    sumatorio = 0
    productorio = 1

    for elem in individuo[0]:
        sumatorio += elem
    for elem in individuo[1]:
        productorio *= elem

    sumatorio = abs(36-sumatorio)
    productorio = abs(360-productorio)

    return sumatorio+productorio

def seleccion(pueblo, probCruce):
    #Realizamos una selección basada en el parámetro probCruce que ha sido pasado por el usuario, seleccionando los mejores individuos.
    preseleccion = []
    for individuo in pueblo:
        validez = aptitud(individuo)
        preseleccion.append((individuo, validez))
    preseleccion = sorted(preseleccion, key = lambda tup:tup[1])
    
    res = []
    i = 0
    while i < probCruce*len(pueblo):
        res.append(preseleccion[i])
        i += 1
    return res

def cruce(seleccionados):
    #El cruce dará como resultado un individuo con la primera pila del padre y la segunda pila de la madre.
    #Como es altamente probable que se repitan números en ambas pilas, se recorre ambas listas eliminando repetidos.
    #De igual forma, si un número no está en ninguna lista, se añadirá a una de ellas.
    padre = seleccionados[0][0]
    hijos = []
    cruce1 = ([],[])
    for madre in seleccionados[1:]:
        cruce1 = (padre[0], madre[0][1])
        i = 1
        cont0 = 0
        cont1 = 0
        hijo = ([],[])
        while i<11:
            if (i in cruce1[0] and i in cruce1[1]) or (i not in hijo[0] and i not in hijo[1]):
                if cont0<cont1:
                    hijo[0].append(i)
                    cont0+=1
                else:
                    hijo[1].append(i)
                    cont1+=1
            elif i in cruce1[0]:
                hijo[0].append(i)
            elif i in cruce1[1]:
                hijo[1].append(i)
            i+=1
        hijos.append(hijo)
    return hijos


def mutacion(nuevaGeneracion, probMutacion):
    #Mutacion por Intercambio Recíproco entre un gen del conjunto del sumatorio y otro del productorio.
    
    i = 0
    while i < probMutacion*len(nuevaGeneracion):
        sel1 = random.choice(nuevaGeneracion[i][0])
        sel2 = random.choice(nuevaGeneracion[i][1])
        nuevaGeneracion[i][0].remove(sel1)
        nuevaGeneracion[i][1].remove(sel2)
        nuevaGeneracion[i][0].append(sel2)
        nuevaGeneracion[i][1].append(sel1)
        i+=1
    return nuevaGeneracion


def reemplazo(pueblo, nuevaGeneracion):
    #Se va a aplicar Reemplazo por Estado - Estacionario. 
    #El número de hijos generados será el número de individuos de la población (con menor fitness) que serán descartados.

    preseleccion = []
    for individuo in pueblo:
        validez = aptitud(individuo)
        preseleccion.append((individuo, validez))
    preseleccion = sorted(preseleccion, key = lambda tup:tup[1], reverse = True)

    i = 0
    while i < len(nuevaGeneracion):
        pueblo.remove(preseleccion[i][0])
        pueblo.append(nuevaGeneracion[i])
        i+=1

    return pueblo

def convergencia(pueblo):
    #Comprobamos si se ha generado un individuo que satisface el problema, es decir, si su función fitness es 0.
    for individuo in pueblo:
        if aptitud(individuo)==0:
            optimo = individuo
            return True, optimo
    return False, None

def genetico(maxIter, pobIni, probCruce, probMutacion):
    iteracion = 0
    terminar = False
    pueblo = iniciarPopulacho(pobIni)
    mejores = []
    
    while not terminar:
        seleccionados = seleccion(pueblo,probCruce)
        nuevaGeneracion = cruce(seleccionados)
        nuevaGeneracion = mutacion(nuevaGeneracion,probMutacion)
        pueblo = reemplazo(pueblo,nuevaGeneracion)
        iteracion += 1
        terminar = iteracion == maxIter or convergencia(pueblo)[0]
        preseleccion = []
        for individuo in pueblo:
            validez = aptitud(individuo)
            preseleccion.append((individuo, validez))
        preseleccion = sorted(preseleccion, key = lambda tup:tup[1])
        print("-------------------------------------------------------------")
        print("Iteración ", iteracion)
        print("-------------------------------------------------------------")
        if preseleccion[0] not in mejores:
            mejores.append(preseleccion[0])
            mensaje = "El mejor individuo por el momento es "+ str(mejores[-1][0])+", con una aptitud de "+ str(mejores[-1][1])+ ", encontrado en la iteración "+ str(iteracion)
        print(mensaje)
        print("\n")

    print("-------------------------------------------------------------")
    print("El algoritmo ha finalizado")
    print("-------------------------------------------------------------")
    if convergencia(pueblo)[0] == True:
        res = "La solución óptima es "
        return res+str(convergencia(pueblo)[1])
    else:
        preseleccion = []
        for individuo in pueblo:
            validez = aptitud(individuo)
            preseleccion.append((individuo, validez))
        preseleccion = sorted(preseleccion, key = lambda tup:tup[1])
        res = "El mejor individuo es "
        res1 = ", con un fitness de "
        return res+str(preseleccion[0][0])+res1+str(aptitud(preseleccion[0][0]))

if __name__ == "__main__":
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Bienvenido al Algoritmo Genético para resolver el Problema de las Cartas.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Tenemos una baraja de 10 cartas del mismo palo, numeradas del 1 al 10 sin repeticiones. Las separamos en 2 pilas.")
    print("En una pila, el sumatorio de las cartas tiene que acercarse lo máximo posible a 36. En la otra, el productorio a 360.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Introduzca el número máximo de iteraciones del AG:")
    maxIter = int(input())
    print("\nIntroduzca el número máximo de individuos de la población inicial:")
    pobIni = int(input())
    print("\nIntroduzca el porcentaje de la población que será cruzada en cada iteración (en tanto por 1):")
    probCruce = float(input())
    print("\nIntroduzca el porcentaje de la nueva generación que será mutada en cada iteración (en tanto por 1):")
    probMutacion = float(input())
    print(genetico(maxIter, pobIni, probCruce, probMutacion))
