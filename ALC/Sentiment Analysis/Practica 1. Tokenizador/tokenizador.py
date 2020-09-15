import re

res = ''

with open('entrada_tokenizador.txt', 'r') as f:

    reHora_Acronimo = re.compile(r'(\d{1,2}(:)\d{1,2})'+'|'+'(?:[A-Z]+\.)+')

    reWeb = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

    reDecimal = re.compile(r'\d+\.\d+'+'|'+"\d+\,\d+")

    reUsuario_Hashtag = re.compile(r'[^@]+@[^@]+\.[^@]+'+'|'+'@+[^@]+'+'|'+'#+[^#]')

    reFechaFormato = re.compile(r'(\d{1,2}(/|-)\d{1,2}((/|-)\d{2,4})?)')

    reGuion = re.compile(r'(\w+(-)\w+)')

    reFecha = re.compile(r'(\d{1,2})(\s+)(\w{2})(\s+)(\w+)(\s+)(\w{2})(\s+)(\d{2,4})')


    while True:
        frase = f.readline()
        res += frase + '\n'
        if frase == "":
            break

        aux = []
        for item in re.finditer(reFecha, frase):
            frase = reFecha.sub('MatchingFecha', frase)
            aux.append(item.group())

        for e in frase.split():
            if e == 'MatchingFecha':
                res += aux.pop(0) + '\n'
            elif reWeb.match(e):
                res += e +'\n'
            elif reDecimal.match(e):
                res += reDecimal.match(e)[0] + '\n'
                for caracter in e:
                    if caracter not in reDecimal.match(e)[0]:
                        res += caracter + '\n'
            elif reUsuario_Hashtag.match(e):
                res += e +'\n'
            elif reHora_Acronimo.match(e):
                res += reHora_Acronimo.match(e)[0] + '\n'
                for caracter in e:
                    if caracter not in reHora_Acronimo.match(e)[0]:
                        res += caracter + '\n'
            elif reFechaFormato.match(e):
                res += reFechaFormato.match(e)[0] + '\n'
                for caracter in e:
                    if caracter not in reFechaFormato.match(e)[0]:
                        res += caracter + '\n'
            elif reGuion.match(e):
                res += reGuion.match(e)[0] + '\n'
                for caracter in e:
                    if caracter not in reGuion.match(e)[0]:
                        res += caracter + '\n'

            else:

                reNoAlfNum = re.compile('[^#(\w+)]')
                reAlfNum = re.compile('[#(\w+)]')

                for caracter in e:
                    if reNoAlfNum.match(caracter):
                        res += caracter + '\n'
                        e = e[1:]
                    else:
                        break

                alfNum = reNoAlfNum.sub('', e)
                if alfNum is not "":
                    res += alfNum + '\n'
                noAlfNum = reAlfNum.sub('', e)
                if noAlfNum is not "":
                    if noAlfNum == '...':
                        res += noAlfNum + '\n'
                    else:
                        for caracter in noAlfNum:
                            res += caracter + '\n'

with open('salida_tokenizador_res.txt', 'w') as f:
    f.write(res)