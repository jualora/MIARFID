def ej1(cadena):
    categorias = {}
    
    #Recorremos cada subcadena y guardamos su categoría correspondiente.
    #Si esa categoría está en el diccionario, aumentamos en 1 su valor actual. Si no, la añadimos con un valor de 1.
    for subcadena in cadena.split(" "):
        cat = subcadena.split("/")[1]
        if cat not in categorias:
            categorias[cat] = 1
        else:
            categorias[cat] += 1
    
    #Ordenamos alfabéticamente el diccionario, guardando el resultado en una lista de tuplas.
    #Con dicha lista, formamos nuestro diccionario ya ordenado.
    aux = sorted(categorias.items())
    res = {}
    for elem in aux:
        res[elem[0]] = elem[1]
    
    return res

def ej2(cadena):
    palabras = {}

    #Recorremos cada subcadena y guardamos su palabra (en minúsculas) y su categoría correspondientes.
    #Si la palabra está en el diccionario, aumentamos en 1 la primera parte de su valor. 
    #Si no, la añadimos al diccionario con la primera parte de su valor a 1. La segunda parte es un diccionario vacío para sus posibles categorías.
    #Si la categoría está en el subdiccionario de la palabra, aumentamos su valor en 1. Si no lo está, la añadimos con un valor de 1.
    for subcadena in cadena.split(" "):
        palabra = subcadena.split("/")[0].lower()
        categoria = subcadena.split("/")[1]
        
        if palabra not in palabras:
            palabras[palabra] = [1, {}]
        else:
            palabras[palabra][0] +=1
        
        if categoria not in palabras[palabra][1]:
            palabras[palabra][1][categoria] = 1
        else:
            palabras[palabra][1][categoria] +=1
    
    #Ordenamos alfabéticamente el diccionario, guardando el resultado en una lista de tuplas.
    #Con dicha lista, formamos nuestro diccionario ya ordenado.
    aux = sorted(palabras.items())
    res = {}
    for elem in aux:
        res[elem[0]] = elem[1]
    
    return res

def ej3(cadena):
    frecuencias = {}
    bigramas = []

    #Guardamos cada subcadena en una lista
    subcadena = cadena.split(" ")

    #Recorremos cada subcadena. Para cada una de ellas, nos guardamos su categoría y su posición en la cadena.
    #Si esa subcadena está en la última posición, añadimos la tupla del símbolo final y la categoría a la lista de bigramas.
    #Si está en la primera posición, añadimos la tupla del símbolo inicial y la categoría a la lista de bigramas.
    #En cualquier otro caso, añadimos la tupla de la categoría actual y la siguiente a la lista de bigramas.
    for i in range(0,len(subcadena)):
        categoria = subcadena[i].split("/")[1]

        if i==len(subcadena)-1:
            bigramas.append([categoria, '</S>'])
        else:
            nextcategoria = subcadena[i+1].split("/")[1]
            if i==0:
                bigramas.append(['<S>', categoria])
            bigramas.append([categoria, nextcategoria])
    
    #Para cada bigrama, si está en el diccionario de frecuencias, aumentamos su valor en 1.
    #Si no lo está, lo añadimos con el valor 1.
    for bigrama in bigramas:
        tupla = (bigrama[0], bigrama[1])
        if tupla not in frecuencias:
            frecuencias[tupla] = 1
        else:
            frecuencias[tupla] += 1
    
    #Mostramos por pantalla cada bigrama y su frecuencia correspondiente.
    for bigrama in frecuencias:
        print(bigrama, " ", frecuencias[bigrama])
    
    return ""

def ej4(palabra, cadena):
    #Creamos un diccionario de palabras y otro de categorías usando los modelos creados en el ejercicio 1 y 2.
    dicCategorias = ej1(cadena)
    dicPalabras = ej2(cadena)
    
    #Si la palabra no está en el diccionario, devolvemos un mensaje de error.
    #Si está, calculamos las probabilidades condicionales de la palabra y sus posibles categorías.
    #Finalmente, las mostramos por pantalla.
    if palabra not in dicPalabras:
        return "La palabra es desconocida"
    else:
        w = dicPalabras[palabra]
        res = []
        for i in w[1]:
            pcatDpal = round(w[1][i]/w[0], 3)
            ppalDcat = round(w[1][i]/dicCategorias[i], 3)
            print("P(", i, "|", palabra,") = ", pcatDpal)
            print("P(", palabra, "|", i,") = ", ppalDcat)
    
    return ""           
            
if __name__ == "__main__":
    cadena ="El/DT perro/N come/V carne/N de/P la/DT carnicería/N y/C de/P la/DT nevera/N y/C canta/V el/DT la/N la/N la/N ./Fp"
    print("Se va a trabajar con la siguiente cadena:\n")
    print(cadena, "\n")
    while True:
        print("Introduzca el número del ejercicio (1-4)", "\n")
        ejer = int(input())
        if ejer>4 or ejer<1:
            print("Introduzca un número válido", "\n")
        elif ejer==1:
            print(ej1(cadena), "\n")
        elif ejer==2:
            print(ej2(cadena), "\n")
        elif ejer==3:
            print(ej3(cadena), "\n")
        elif ejer==4:  
            print("Introduzca la palabra a analizar", "\n")
            pal = input()
            print(ej4(pal, cadena), "\n")
