#PROBLEMA DE LAS CARTAS CON ENFRIAMIENTO SIMULADO
#Tenemos una baraja de 10 cartas del mismo palo, numeradas del 1 al 10 sin repeticiones.
#Hay que separarlas en 2 pilas, de modo que en una el sumatorio de las cartas se acerque lo máximo posible a 36 y en la otra el productorio se acerque lo máximo a 360
import random
import math 
from random import randint
from random import choice
import time

def iniciar_individuo():
    tupla = ([], [])
    i = 1
    while i<11:
        aleatorio = randint(0,1)
        if aleatorio==0:
            tupla[0].append(i)
        else:
            tupla[1].append(i)
        i += 1
    return tupla
    

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

def suc(s_actual):
    sucesores = []
    while len(sucesores)<2*len(s_actual[0]):
        tupla = ([], [])
        i = 1
        while i<11:
            aleatorio = randint(0,1)
            if aleatorio==0:
                tupla[0].append(i)
            else:
                tupla[1].append(i)
            i += 1
        sucesores.append(tupla)
    return sucesores

def seleccionar_sucesor(sucesores):
    return sucesores.pop(sucesores.index(random.choice(sucesores)))

def actualizarT(i, k, t):
    return t/(1+k*t)

def convergencia(i, s_actual):
    if i>5000 or aptitud(s_actual)==0:
        return True
    else:
        return False

def enfriamiento_simulado(t_inicial, k):
    s_actual = iniciar_individuo()
    sucesores = suc(s_actual)
    s_mejor = s_actual
    t = t_inicial
    i = 0
    while len(sucesores)!=0 and not convergencia(i, s_actual):
        i=i+1
        print("-------------------------------------------------------------")
        print("Iteración ", i)
        print("-------------------------------------------------------------")
        s_nuevo = seleccionar_sucesor(sucesores)
        incremento = aptitud(s_actual)-aptitud(s_nuevo)
        if incremento>0:
            s_actual = s_nuevo
            sucesores = suc(s_actual)
            if aptitud(s_nuevo)<aptitud(s_mejor):
                s_mejor = s_nuevo
        else:
            if random.random() < math.e**(incremento/t):
                s_actual = s_nuevo
                sucesores = suc(s_actual)
                t = actualizarT(i, k, t)
        print("La solución actual es ", s_actual, ", con un fitness de ", aptitud(s_actual))
    return "\nLa solución es "+str(s_mejor)+", con un fitness de "+str(aptitud(s_mejor))


if __name__ == '__main__':
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Bienvenido al Enfriamiento Simulado para resolver el Problema de las Cartas.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Tenemos una baraja de 10 cartas del mismo palo, numeradas del 1 al 10 sin repeticiones. Las separamos en 2 pilas.")
    print("En una pila, el sumatorio de las cartas tiene que acercarse lo máximo posible a 36. En la otra, el productorio a 360.")
    print("----------------------------------------------------------------------------------------------------------------------")
    print("Introduzca la temperatura inicial:")
    t = int(input())
    print("\nIntroduzca la constante k para la actualización de la temperatura:")
    k = float(input())
    print(enfriamiento_simulado(t,k))
    
    