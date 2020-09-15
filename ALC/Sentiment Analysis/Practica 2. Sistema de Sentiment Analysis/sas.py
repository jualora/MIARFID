from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from nltk.tokenize.casual import casual_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import neighbors
import re
from nltk.corpus import stopwords

def cargarDatos():
    x_train = []
    y_train = []
    x_dev = []
    y_dev = []
    x_test = []
    y_test = []

    with open("TASS2017_T1_training.txt") as f:
        datos = f.read()
        for tweet in datos.split("\n"):
            features = tweet.split(" ")
            for feature in features:
                if feature==features[1]:
                    y_train.append(feature)
                if feature==features[2]:
                    break
            contenido = ''
            for feature in features[2:]:
                contenido += feature + ' '
            contenido = contenido[:-1]
            x_train.append(contenido)

    with open("TASS2017_T1_development.txt") as f:
        datos = f.read()
        for tweet in datos.split("\n"):
            features = tweet.split(" ")
            for feature in features:
                if feature==features[1]:
                    y_dev.append(feature)
                if feature==features[2]:
                    break
            contenido = ''
            for feature in features[2:]:
                contenido += feature + ' '
            contenido = contenido[:-1]
            x_dev.append(contenido)
    
    with open("TASS2017_T1_test.txt") as f:
        datos = f.read()
        for tweet in datos.split("\n"):
            features = tweet.split(" ")
            for feature in features:
                if feature==features[0]:
                    y_test.append(feature)
                if feature==features[1]:
                    break
            contenido = ''
            for feature in features[2:]:
                contenido += feature + ' '
            contenido = contenido[:-1]
            x_test.append(contenido)
                    
    return x_train, y_train, x_dev, y_dev, x_test, y_test

def preproceso(x_train, x_dev, x_test):
    train = []
    dev = []
    test = []

    reMencionHashtag = re.compile(r'@+\w+' + '|' + '#+\w+')
    reWeb = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

    print('Limpiamos los datos...')
    for element in x_train:
        for item in re.finditer(reMencionHashtag, element):
            element = reMencionHashtag.sub('>tweet', element)
        for item in re.finditer(reWeb, element):
            element = reWeb.sub('>url', element)
        train.append(element)

    for element in x_dev:
        for item in re.finditer(reMencionHashtag, element):
            element = reMencionHashtag.sub('>tweet', element)
        for item in re.finditer(reWeb, element):
            element = reWeb.sub('>url', element)
        dev.append(element)

    for element in x_test:
        for item in re.finditer(reMencionHashtag, element):
            element = reMencionHashtag.sub('>tweet', element)
        for item in re.finditer(reWeb, element):
            element = reWeb.sub('>url', element)
        test.append(element)

    print('Vectorizamos...')
    vectorizador = TfidfVectorizer(tokenizer=casual_tokenize, max_df=0.8)
    vectorizador.fit(train)
    vectorizador.fit_transform(dev)
    vectorizador.fit_transform(test)
    matriz_train = vectorizador.transform(train)
    matriz_dev = vectorizador.transform(dev)
    matriz_test = vectorizador.transform(test)

    return matriz_train.toarray(), matriz_dev.toarray(), matriz_test.toarray()

def train(matriz_train, y_train):
    #modelo = svm.SVC(C=1)
    #modelo = svm.LinearSVC(C=1)
    modelo = svm.LinearSVC(C=100, tol=0.1, loss='hinge', max_iter=1000000000)
    #modelo = GaussianNB()
    #modelo = GradientBoostingClassifier()
    #modelo = SGDClassifier()
    #modelo = neighbors.KNeighborsClassifier()
    
    modelo.fit(matriz_train, y_train)

    return modelo

if __name__ == '__main__':

    print('Cargamos los datos...')
    x_train, y_train, x_dev, y_dev, x_test, y_test = cargarDatos()

    print('Preprocesamos los datos...')
    matriz_train, matriz_dev, matriz_test = preproceso(x_train, x_dev, x_test)

    print('Entrenamos el modelo...')
    modelo = train(matriz_train, y_train)

    print('Realizamos las predicciones...')
    predicciones = modelo.predict(matriz_dev)

    print("precision = ", accuracy_score(y_dev, predicciones))
    print("macro promedio = ", precision_recall_fscore_support(y_dev, predicciones, average='macro'))
    print("micro promedio = ", precision_recall_fscore_support(y_dev, predicciones, average='micro'))

    resultados_test = modelo.predict(matriz_test)

    with open('JuanLopez_svm.txt', 'a') as file:
        for i in range(len(y_test)):
            ids = y_test[i].split('\n')
            etiqueta = resultados_test[i].split('\n')
            file.write(ids[0]+'\t'+etiqueta[0]+'\n')

