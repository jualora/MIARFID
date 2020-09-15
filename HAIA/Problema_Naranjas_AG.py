##PROBLEMA DE LA PESADORA DE NARANJAS CON ALGORITMOS GENÉTICOS##
import random
from random import randint
import time

def iniciarPopulacho(pobIni):
    #Creamos la población inicial.
    pueblo = []
    while len(pueblo)<pobIni:
        individuo = [0,0,0,0,0,0,0,0,0,0]
        while sum(individuo) < minCubeta:
            for i in range(len(individuo)):
                if sum(individuo) == maxCubeta:
                    break
                else:
                    aleatorio = randint(0,1)
                    if aleatorio==0:
                        individuo[i] = 1
        pueblo.append(individuo)
    return pueblo

def aptitud(individuo):
    #Definimos la función de aptitud de un individuo como la diferencia entre la malla total y el peso total de naranjas 
    #que deja pasar en función de las cubetas habilitadas que tiene.
    weight = 0

    for i in range(len(individuo)):
        weight += individuo[i] * pesos[i]

    if weight >= malla:
        apt = weight - malla 
    else:
        apt = malla * probCubeta * 100 - weight
    
    return apt

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
    #El cruce se hará eligiendo al mejor individuo como padre y al resto como madre, de manera que se generarán n-1 hijos, siendo n el tamaño de los seleccionados.
    #El cruce dará como resultado un individuo con los componentes impares del padre y los pares de la madre.
    #Como es probable que el hijo tenga más componentes a 1 que el máximo de cubetas o menos que el mínimo, se recorre la lista añadiendo o eliminando componentes.
    #El índice del componente que será eliminado o insertado se hace de forma aleatoria para no priorizar el orden ascendente o descendente de la lista.
    padre = seleccionados[0][0]
    hijos = []

    for madre in seleccionados[1:]:
        cruce = []
        for i in range(len(padre)):
            if i%2==1:
                cruce.append(padre[i])
            elif i%2==0:
                cruce.append(madre[0][i])
        while sum(cruce)>maxCubeta:
            indice = randint(0, len(cruce)-1)
            cruce[indice] = 0
        while sum(cruce)<minCubeta:
            indice = randint(0, len(cruce)-1)
            cruce[indice] = 1
        hijos.append(cruce)

    return hijos

def mutacion(nuevaGeneracion, probMutacion):
    #Mutacion por Intercambio Recíproco entre dos genes de la lista del individuo.
    i = 0
    while i < probMutacion*len(nuevaGeneracion):
        if sum(nuevaGeneracion[i])==len(nuevaGeneracion[i]):
            indice = randint(0, len(nuevaGeneracion[i])-1)
            if nuevaGeneracion[i][indice]==0:
                nuevaGeneracion[i][indice] = 1
            elif nuevaGeneracion[i][indice]==1:
                nuevaGeneracion[i][indice] = 0
        else:
            indice1 = -1
            indice2 = -1
            while indice1 == indice2 or nuevaGeneracion[i][indice1] == nuevaGeneracion[i][indice2]:
                indice1 = randint(0, len(nuevaGeneracion[i])-1)
                indice2 = randint(0, len(nuevaGeneracion[i])-1)
            aux = nuevaGeneracion[i][indice1]
            nuevaGeneracion[i][indice1] = nuevaGeneracion[i][indice2]
            nuevaGeneracion[i][indice2] = aux
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
    #Comprobamos si se ha generado un individuo que satisface el problema.
    for individuo in pueblo:
        if aptitud(individuo)==0:
            optimo = individuo
            return True, optimo
    return False, None

def genetico(maxIter, pobIni, probCruce, probMutacion):
    start_time = time.time()
    
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
    
    elapsed_time = time.time() - start_time
    elapsed_time = elapsed_time * 1000
    
    print("-------------------------------------------------------------")
    print("El algoritmo ha finalizado")
    print("-------------------------------------------------------------")
    if convergencia(pueblo)[0] == True:
        res = "La solución óptima es "
        resFin = " y ha tardado %0.10f milisegundos." % elapsed_time
        return res+str(convergencia(pueblo)[1])+resFin
    else:
        preseleccion = []
        for individuo in pueblo:
            validez = aptitud(individuo)
            preseleccion.append((individuo, validez))
        preseleccion = sorted(preseleccion, key = lambda tup:tup[1])
        res = "El mejor individuo es "
        res1 = ", con un fitness de "
        resFin = " y ha tardado %0.10f milisegundos." % elapsed_time
        return res+str(preseleccion[0][0])+res1+str(aptitud(preseleccion[0][0]))+resFin

if __name__ == "__main__":
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Bienvenido al Algoritmo Genético para resolver el Problema de la pesadora de naranjas.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Introduzca el peso de la malla:")
    malla = int(input())
    print("\nIntroduzca el porcentaje máximo por cubeta (en tanto por 1):")
    probCubeta = float(input())
    print("\nIntroduzca el número mínimo de cubetas a seleccionar:")
    minCubeta = int(input())
    print("\nIntroduzca el número máximo de cubetas a seleccionar:")
    maxCubeta = int(input())
    print("\nIntroduzca el número máximo de iteraciones del AG:")
    maxIter = int(input())
    
    pesoMax = int(malla*probCubeta)
    pesos = []
    for i in range(10):
        pesos.append(randint(0,pesoMax))
        
    print("\nIntroduzca el número máximo de individuos de la población inicial:")
    pobIni = int(input())
    print("\nIntroduzca el porcentaje de la población que será cruzada en cada iteración (en tanto por 1):")
    probCruce = float(input())
    print("\nIntroduzca el porcentaje de la nueva generación que será mutada en cada iteración (en tanto por 1):")
    probMutacion = float(input())
    print(genetico(maxIter, pobIni, probCruce, probMutacion))
    print("El peso de cada cubeta es: " + str(pesos))
