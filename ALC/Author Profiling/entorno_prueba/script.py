import sys
import numpy as np
import os
from xml.dom import minidom
from nltk.tokenize.casual import casual_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
import argparse
from joblib import load
import xml.etree.ElementTree as ET

def cargarDatos(datasetArg):
    for base, dirs, files in os.walk(datasetArg+'/en'):
        datasets_en = files
    for base, dirs, files in os.walk(datasetArg+'/es'):
        datasets_es = files

    X_train_en = []
    X_train_es = []
    for dataset in datasets_en:
        data = datasetArg+'/en/'+dataset
        xmldoc = minidom.parse(data)
        documents = xmldoc.getElementsByTagName('document')
        samples=[]
        for d in documents:
            for node in d.childNodes:
                samples.append(node.data)
        samples = ' '.join(samples)
        samples = samples.replace("\n", " ")
        X_train_en.append(samples)
    for dataset in datasets_es:
        data = datasetArg+'/es/'+dataset
        xmldoc = minidom.parse(data)
        documents = xmldoc.getElementsByTagName('document')
        samples=[]
        for d in documents:
            for node in d.childNodes:
                samples.append(node.data)
        samples = ' '.join(samples)
        samples = samples.replace("\n", " ")
        X_train_es.append(samples)
    
    return X_train_en, X_train_es, datasets_en, datasets_es

if __name__ == "__main__":
    datasetArg = sys.argv[2]
    outputDir = sys.argv[4]
    
    X_train_en, X_train_es, ids_en, ids_es = cargarDatos(datasetArg)
    
    modelo_en = load('modelo_en.pkl')
    modelo_es = load('modelo_es.pkl')

    pred_en = modelo_en.predict(X_train_en)
    pred_es = modelo_es.predict(X_train_es)

    os.makedirs(outputDir+'/en', exist_ok=True)
    os.makedirs(outputDir+'/es', exist_ok=True)
    i=0
    for ident in ids_en:
        xml = ET.Element('author', attrib={'id':ident[:-4], 'lang':'en', 'type':str(pred_en[i])})
        ET.dump(xml)
        tree = ET.ElementTree(xml)
        tree.write(outputDir+'/en/'+ident)
        i+=1
    i=0
    for ident in ids_es:
        xml = ET.Element('author', attrib={'id':ident[:-4], 'lang':'es', 'type':str(pred_es[i])})
        ET.dump(xml)
        tree = ET.ElementTree(xml)
        tree.write(outputDir+'/es/'+ident)
        i+=1

