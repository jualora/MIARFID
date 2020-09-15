import sys
import numpy as numpy
import os
from xml.dom import minidom
from nltk.tokenize.casual import casual_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import neighbors
from sklearn.pipeline import Pipeline
from joblib import dump
from sklearn.preprocessing import scale

##CARGAMOS LOS DATOS##

for base, dirs, files in os.walk('./pan20-author-profiling-training-2020-02-23/en'):
    datasets_en = files
for base, dirs, files in os.walk('./pan20-author-profiling-training-2020-02-23/es'):
    datasets_es = files

for dataset in datasets_en:
    if dataset=='truth.txt':
        etiqs_en = datasets_en.pop(datasets_en.index(dataset))

for dataset in datasets_es:
    if dataset=='truth.txt':
        etiqs_es = datasets_es.pop(datasets_es.index(dataset))

archivo_en = open('./pan20-author-profiling-training-2020-02-23/en/'+etiqs_en).read()
archivo_es = open('./pan20-author-profiling-training-2020-02-23/es/'+etiqs_es).read()
Y_train_en = []
Y_train_es = []
ids_en = []
ids_es = []

for linea in archivo_en.split('\n'):
    for elemento in linea.split(':::'):
        if len(elemento)==1:
            Y_train_en.append(int(elemento))
        else:
            ids_en.append(elemento)
ids_en = ids_en[:-1]

for linea in archivo_es.split('\n'):
    for elemento in linea.split(':::'):
        if len(elemento)==1:
            Y_train_es.append(int(elemento))
        else:
            ids_es.append(elemento)
ids_es = ids_es[:-1]

X_train_en = []
X_train_es = []
for dataset in ids_en:
    data = './pan20-author-profiling-training-2020-02-23/en/'+dataset+".xml"
    xmldoc = minidom.parse(data)
    documents = xmldoc.getElementsByTagName('document')
    samples=[]
    for d in documents:
        for node in d.childNodes:
            samples.append(node.data)
    samples = ' '.join(samples)
    samples = samples.replace("\n", " ")
    X_train_en.append(samples)
for dataset in ids_es:
    data = './pan20-author-profiling-training-2020-02-23/es/'+dataset+".xml"
    xmldoc = minidom.parse(data)
    documents = xmldoc.getElementsByTagName('document')
    samples=[]
    for d in documents:
        for node in d.childNodes:
            samples.append(node.data)
    samples = ' '.join(samples)
    samples = samples.replace("\n", " ")
    X_train_es.append(samples)

##VECTORIZAMOS LOS DATOS##

steps_es = [('vectorizador', TfidfVectorizer(tokenizer=casual_tokenize, max_features=1000, max_df=0.8, ngram_range=(2,3), strip_accents='unicode')), ('clasificador', svm.LinearSVC(C=100, tol=0.01, loss='hinge', max_iter=100))] 
#steps_en = [('vectorizador', CountVectorizer(tokenizer=casual_tokenize, max_df=0.8)), ('clasificador', GradientBoostingClassifier(loss='deviance', learning_rate=0.01, n_estimators=250, verbose=1))]

#pipeline_en = Pipeline(steps_en)
pipeline_es = Pipeline(steps_es)

#pipeline_en.fit(X_train_en, Y_train_en)
pipeline_es.fit(X_train_es, Y_train_es)

#dump(pipeline_en, 'modelo_en.pkl')
dump(pipeline_es, 'modelo_es_p.pkl')

"""vectorizador = CountVectorizer(tokenizer=casual_tokenize, max_df=0.8)
vectorizador.fit(X_train_en)
vectorizador.fit(X_train_es)
matriz_train_en = vectorizador.transform(X_train_en)
matriz_train_es = vectorizador.transform(X_train_es)

##DEFINIMOS LOS MODELOS##

modelo_es = svm.LinearSVC(C=100, tol=0.01, loss='hinge', max_iter=100) #0.84es//0.63en
#modelo = svm.LinearSVC(C=1) #0.83es//0.64en
#modelo = MLPClassifier(hidden_layer_sizes=(15,), solver='adam', alpha=0.0001, batch_size=200, learning_rate='constant', learning_rate_init=0.001, random_state=1, max_iter=500, verbose=True, warm_start=True) #0.82es//0.65en
#modelo = SGDClassifier() #0.78es//0.67en
#modelo = GradientBoostingClassifier(verbose=1) #0.76es//0.71en
modelo_en = GradientBoostingClassifier(loss='deviance', learning_rate=0.01, n_estimators=250, verbose=1) #0.76es//0.73en
#modelo = svm.SVC(C=1) #0.74es//0.63en
#modelo = neighbors.KNeighborsClassifier() #0.74es//0.59en
#modelo = GaussianNB() #0.70es//0.64en

##REALIZAMOS LA VALIDACION CRUZADA CON 10 BLOQUES##

#scores_en = cross_val_score(modelo_en, matriz_train_en.toarray(), Y_train_en, cv=10, scoring='accuracy')
scores_es = cross_val_score(modelo_es, matriz_train_es.toarray(), Y_train_es, cv=10, scoring='accuracy')
#print("Accuracy (en): %0.2f (+/- %0.2f)" % (scores_en.mean(), scores_en.std() * 2))
print("Accuracy (es): %0.2f (+/- %0.2f)" % (scores_es.mean(), scores_es.std() * 2))

#print("Scores para el modelo en inglés --> " + str(scores_en))
print("Scores para el modelo en español --> " + str(scores_es))

##ENTRENAMOS NUESTROS MEJORES MODELOS PARA INGLÉS Y ESPAÑOL Y LOS GUARDAMOS##

modelo_es.fit(matriz_train_es.toarray(), Y_train_es)
#modelo_en.fit(matriz_train_en.toarray(), Y_train_en)

dump(modelo_es, 'modelo_es.pkl')
#dump(modelo_en, 'modelo_en.pkl')"""