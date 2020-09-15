import math
from subprocess import call

if __name__ == '__main__':
    # Calculamos PM(x) y lo guardamos en la carpeta ./probabilities
    for c in ["TS-EQ", "TS-IS", "TS-SC"]:
        for a in ["EQ","IS","SC"]:
            for g in ["G1","G2","G3"]:
                call("./scfg-toolkit/scfg_prob -g models/"+g+"-"+a+" -m corpus/"+c+" > probabilities/res_"+c+"_"+g+"_"+a, shell=True)
    
    # Calculamos el Test Set Perplexity para cada submodelo y cada conjunto de prueba, 
    # guardando los resultados en un fichero llamado perplexities.txt
    perplexities = []
    for c in ["TS-EQ", "TS-IS", "TS-SC"]:
        for g in ["G1","G2","G3"]:
            for a in ["EQ","IS","SC"]:
                f = open("./probabilities/res_"+c+"_"+g+"_"+a, "r")
                fichero = f.read()[:-1]
                sumatorio = 0
                N = 0
                for numero in fichero.split("\n"):
                    num = float(numero)
                    if num!=0:
                        sumatorio += math.log2(num)
                    N += 1
                perplexity = math.pow(2, (-1/N)*sumatorio)
                perplexities.append("Perplejidad en "+c+"_"+g+"_"+a+" es "+str(perplexity))
    with open("perplexities.txt", "w") as f:
            for i in perplexities:
                f.write(i+"\n")     

    # Clasificación
    for g in ["G1","G2","G3"]:
        for c in ["EQ", "IS", "SC"]:
            f1 = []
            f2 = []
            f3 = []
            i = 1
            for a in ["EQ","IS","SC"]:
                f = open("./probabilities/res_TS-"+c+"_"+g+"_"+a, "r")
                fichero = f.read()[:-1]
                for numero in fichero.split("\n"):
                    if i==1:
                        f1.append(float(numero))
                    elif i==2:
                        f2.append(float(numero))
                    else:
                        f3.append(float(numero))
                i+=1
            lista = zip(f1, f2, f3)
            res = []
            for tupla in lista:
                if max(tupla)==tupla[0]:
                    res.append("EQ")
                elif max(tupla)==tupla[1]:
                    res.append("IS")
                else:
                    res.append("SC")
            with open("fichero_res"+c+"_"+g+".txt", "w") as f:
                for i in res:
                    f.write(c+ " "+ i+"\n")

    for g in ["G1","G2","G3"]:
        res = []
        for c in ["EQ", "IS", "SC"]:
            f = open("fichero_res"+c+"_"+g+".txt", "r")
            fichero = f.read()[:-1]
            for linea in fichero.split("\n"):
                res.append(linea)
        
        with open("fichero_res_def"+g+".txt", "w") as f:
            for i in res:
                f.write(i+"\n")
    
    for g in ["G1","G2","G3"]:
        print("Resultados obtenidos con "+ g)
        call("./confus fichero_res_def"+g+".txt" ,shell=True)
        print("\n")
        


    

