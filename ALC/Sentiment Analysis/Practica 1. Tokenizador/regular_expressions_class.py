
# coding: utf-8

# # INFO: Regular Expressions (python 3.x)
# 
# https://docs.python.org/3/library/re.html
# 
# https://docs.python.org/3/howto/regex.html#regex-howto
# 
# 

# # EJERCICIO 1: Quitar los signos de puntuación de la siguiente cadena:  ??. ppi. ¿casa?.. COSA. ??perro. ¿quesito? "qüestió" anar-hi.   

# In[1]:


import re
frase="??. ppi. PEPE ¿casa?.. COSA. ??perro. ¿quesito? qüestió anar-hi."
x=re.match(r'(?P<principi>\W*)(\w+)(\W*)', frase)
print(x)
print (x.group(1))
print (x.group(2))
print (x.group(3))
print ("->name: ",x.group('principi'))
print (x.span())
print (x.start())
print (x.end())
cadena=frase[x.start():x.end()]
print ("cadena=",cadena)
print (re.match(r'(la) \1 (lam)',"la la lam"))


# In[2]:


import re
frase='"t1 t2 t3 t4"'



# In[3]:


#Compilar la expresion
pattern=re.compile (r'(\W*)(\w+)(\W*)',re.I|re.U) 
#pattern es la expresión regular compilada, y sobre ella se pueden utilizar los métodos match, search, findall, ...

#Match: al principio de la cadena

mat=pattern.match(frase)
if mat:
    print (mat.group(1))
    print (mat.group(2))
    print (mat.group(3))


# In[4]:


#Search: la primera que encuentra en la cadena
sear=pattern.search(frase)
if sear:
    print (sear.group(1))
    print (sear.group(2))
    print (sear.group(3))


# In[5]:


#Finditer: Todas las ocurrencias de la cadena
fiiter=pattern.finditer(frase)
print ([x for x in fiiter])


# In[6]:


#Finditer:
fiiter=pattern.finditer(frase)
for i in fiiter:
    print (i.group(1))
    print (i.group(2))
    print (i.group(3))


# In[7]:


# Findall: Totes las ocurrencias de la cadena
fiall=pattern.findall(frase)
print (fiall)
for i in fiall:
    print (i[1])


# # EJERCICIO 2: "sustituye la palabra eso por  3 guiones, pero OJO con queso, o beso, o en ESO en mayúsculas"

# In[8]:


import re
frase1='sustituye la palabra eso por  3 guiones, pero OJO con: queso, o beso; ESO en mayúsculas sí.'
print (frase1)
susti=re.compile (r'(\beso\b)',re.I|re.U|re.X)
x=re.sub(susti,"---",frase1)
print(x)


# # EJERCICIO 3: encontrar fechas con formato dd/mm/aaaa, dd/mm. El separador también puede ser  un guión.

# In[9]:


import re
ejemplo="el 12/03/1987 el 23/03 o el 21-04 no "


# In[10]:


date="(\d{2}(/|-)\d{2}((/|-)\d{4})?)"
pattern=re.compile (date,re.I|re.U)


# In[11]:


fiiter=pattern.finditer(ejemplo)
for i in fiiter:
    print (ejemplo[i.start():i.end()])


# # EJERCICIO 4: definir una RE que reconozca las instancias de "Dani Alvez" del texto del ejemplo

# In[12]:


import re
texto= "#dani alves #daniel alves #danielalves99_k daniel @daniel_kk alves #alves alves"
pattern_con_grupos=re.compile(r'([#@]?dani\S*)? (\s)* ([#@]?alves\S*)+',re.I|re.X)
pattern_sin_grupos=re.compile(r'(?:[#@]?dani\S*)? (?:\s)* (?:[#@]?alves\S*)+',re.I|re.X)
#IMPORTANTE: poner la opciones:
# re.I: para olvidarte de mayúsculas y minúsculas
# re.X: para olvidarte de blancos y comentarios dentro de las expresiones regulares
#        si no se pone y dejas un blanco, es una parte mas de regex
# Ojo con los parentesis: cada vez que pones una expresión entre parentesis es un grupo 
# y a veces no interesa
# Si pones por ejemplo (xxx) es un grupo, si no quieres grupo (?:xxx)

#Con grupos
print("CON GRUPOS:")
print("----------") 
results_grupos=pattern_con_grupos.findall(texto)
for f in results_grupos:
    print (f)
print("----------")  

#Sin grupos
print("SIN GRUPOS:")
print("----------") 
results_sin_grupos=pattern_sin_grupos.findall(texto)
for f in results_sin_grupos:
    print (f)
print("----------") 


# # Ejercicio 5: Elongated words and censured words

# In[13]:


cad= 'soooo hiiiii whyyyy done calla callllllllla'
import re 
elongated = re.compile(r"(.)\1{2}")
print ([word for word in cad.split() if elongated.search(word)])


# In[14]:


import re
frase1='soooo hiiiii whyyyy done calla callllllllla'
norm=re.compile (r"(.)\1{2,}",re.I|re.U|re.X)
x=re.sub(norm,r"\1",frase1)
print(x)


# In[15]:


fraseC="p**a c**o puto m*****n"
censurado=re.compile (r'(?:\b\w+[*]+\w+\b)')
print([word for word in fraseC.split() if censurado.search(word)])                                

