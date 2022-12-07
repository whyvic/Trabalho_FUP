import math

def norma(dict):
    soma_dos_quadrados = 0.0
    for x in dict:
        soma_dos_quadrados += dict[x] * dict[x]

    return math.sqrt(soma_dos_quadrados)

def similaridade_cosseno(dict_1, dict_2):

    p_escalar = 0
    for a in dict_1:
        if a in dict_2:
            p_escalar += dict_1[a] * dict_2[a]
    p_mag = norma(dict_1) * norma(dict_2)
    return p_escalar / p_mag

def constroi_descritores_semanticos(sentencas):
    dicionario = {}
    for sentenca in sentencas:
        palavras_sentenca = []
        for palavras in sentenca:
            if palavras not in palavras_sentenca:
                palavras_sentenca.append(palavras)
        for palavra_x in palavras_sentenca:
            if palavra_x not in dicionario:
                dicionario[palavra_x] = {}
            for palavra_seg in palavras_sentenca:
                if palavra_x != palavra_seg:
                    if palavra_seg not in dicionario[palavra_x]:
                        dicionario[palavra_x][palavra_seg] = 0
                    dicionario[palavra_x][palavra_seg] += 1
    return dicionario

def constroi_descritores_semanticos_de_arquivos(nomes_arquivos):

    L = []
    for text in nomes_arquivos:
        file = open(text, encoding="utf8").read().lower().replace("\n", " ").replace(',', ' ').replace('-',
                                                                                                       ' ').replace(
            '--', ' ').replace(':', ' ').replace(';', ' ').split('.')
        for i in range(len(file)):
            file[i] = file[i].split('!')
            for j in range(len(file[i])):
                file[i][j] = file[i][j].split('?')
                for k in range(len(file[i][j])):
                    file[i][j][k] = file[i][j][k].split()
                    L.append(file[i][j][k])
    g = constroi_descritores_semanticos(L)
    return g

def palavra_mais_similar(palavra, escolhas, descritores_semanticos, funcao_similaridade):

    x = []
    if palavra not in descritores_semanticos:
        return -1
    for escolha in escolhas:
        if escolha not in descritores_semanticos:
            x.append(-1)
            continue
        x.append(funcao_similaridade(descritores_semanticos[palavra], descritores_semanticos[escolha]))
    return escolhas[x.index(max(x))]

def executa_teste_similaridade(nome_arquivo, descritores_semanticos, funcao_similaridade):

    correto = 0
    file = open(nome_arquivo, encoding="latin1").read().split("\n")
    for i in range(len(file)):
        file[i] = file[i].split()
        if len(file[i]) == 0:
            del file[i]
            i -= 1
            continue
        if file[i][1] == palavra_mais_similar(file[i][0], file[i][2:], descritores_semanticos, funcao_similaridade):
            correto = correto + 1

    return correto / len(file) * 100


if __name__ == "__main__":
    #A
    print(similaridade_cosseno({"i": 3, "am": 3, 'a': 2, 'sick': 1, 'spiteful': 1, 'an': 1, 'unattractive': 1},
                               {'i': 1, 'believe': 1, 'my': 1, 'is': 1, 'diseased': 1}))
    print(similaridade_cosseno({"a": 1, "b": 2, 'c': 3}, {'b': 4, 'c': 5, 'd': 6}))

    # B
    frases = [["i", "am", "a", "sick", "man"],
              ["i", "am", "a", "spiteful", "man"],
              ["i", "am", "an", "unattractive", "man"],
              ["i", "believe", "my", "liver", "is", "diseased"],
              ["however", "i", "know", "nothing", "at", "all", "about", "my",
               "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    print(constroi_descritores_semanticos(frases))

    # C
    arquivos = ["war_and_peace.txt", "swanns_way.txt"]
    descritores_semanticos = constroi_descritores_semanticos_de_arquivos(arquivos)


    # D
    print(palavra_mais_similar("cowardice", ["fear", "successive"], descritores_semanticos, similaridade_cosseno))
    print(palavra_mais_similar("connection", ["pipe", "relation", "connecticut", "excited"], descritores_semanticos,
                                similaridade_cosseno))

    # E
    print(executa_teste_similaridade("teste.txt", descritores_semanticos, similaridade_cosseno))
