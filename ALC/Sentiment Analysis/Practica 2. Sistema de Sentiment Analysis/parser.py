##Parser para la práctica de sentiment analysis utilizando el módulo minidom##
import sys
from xml.dom import minidom

dataset = sys.argv[1]
datasetParseado = ''
xmldoc = minidom.parse(dataset)
tweets = xmldoc.getElementsByTagName('tweet')

for t in tweets:
    for node in t.childNodes:
        if node.nodeName == 'tweetid':
            idTweet = node.firstChild.data
        elif node.nodeName == 'content':
            contenido = node.firstChild.data.replace("\n", " ")
        elif node.nodeName == 'sentiment':
            if 'test' not in dataset:
                for h in node.childNodes:
                    if h.nodeName == 'polarity':
                        if h.firstChild.nodeName == 'value':
                            polarizacion = h.firstChild.firstChild.data
    if 'test' not in dataset:
        datasetParseado += idTweet + ' ' + polarizacion + ' ' + contenido + "\n"
    else:
        datasetParseado += idTweet + ' ' + contenido + "\n"

datasetParseado = datasetParseado[:-1]
nombreDatasetParseado = dataset[:-4]
nombreDatasetParseado += '.txt'
with open(nombreDatasetParseado, 'w') as f:
    f.write(datasetParseado)
