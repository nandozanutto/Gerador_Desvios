import pandas as pd
import re
import itertools
import re
import random
from datetime import datetime


#definições
composto_dict = {"qu": "1", "ss":"3", "ch":"4", "nh":"5", "lh":"6", "rr":"7"}
composto_dict_reverse = {v: k for k, v in composto_dict.items()}

nao_omite = ['SN V', 'CN1 V', 'CN2 V', 'CA1 O', 'CA1 F', 'CA1 N', 'CA1 L', 'SA O', 'SA F', 'SA N', 'SA L']
dictSom = {'1': 'k', "c":"s", "2":"s", "ç":"s", "x":"s", "s":"z"}
composto_fonetica = {"qu":"1", "ss":"2"}
composto_fonetica_inverse = {'1':"qu", "2":"ss"}


SC = ['p', 't', 'd', 'c', 'g', 'f', 's', 'z', 'm', 'n', 'l', 'r']
CA = ['pl', 'pr', 'ps', 'pn', 'bl', 'br', 'tl', 'tr', 'ts', 'dr', 'cl', \
      'cr', 'gl', 'gr', 'fl', 'fr', 'vl', 'vr']

CC = ['ns', 'rs']

dictClasses = {
    "O": "oclusiva",
    "F": "fricativa",
    "N": "nasal",
    "L": "líquida"
}

dictEtiquetas = {
                    "SC O": ["p", "t", "d", "c", "g"],
                    "SC F": ['f', 's', 'z'],
                    "SC N": ['m', 'n'],
                    "SC L": ['l', 'r'],
                    "SA O": ['p', 'b', 't', 'd', 'c', '1', 'g'],
                    "SA F": ['f','v','s','3','c','x','z','4','j','g'],
                    "SA N": ['m', 'n', '5'],
                    "SA L": ['l', '6', 'r', '7'],
                    "CA2 L": ['r', 'l'],
                 }
# word = "queijo:"

dictETI_NAMES = {
                    "SA O": "consoante oclusiva em posição de ataque simples",
                    "SA F": "consoante fricativa em posição de ataque simples",
                    "SA N": "consoante nasal em posição de ataque simples",
                    "SA L": "consoante líquida em posição de ataque simples",
                    
                    "SC O": "consoante oclusiva em posição de coda simples",
                    "SC F": "consoante fricativa em posição de coda simples",
                    "SC N": "consoante nasal em posição de coda simples",
                    "SC L": "consoante líquida em posição de coda simples",

                    "CA1 O": "consoante oclusiva em posição 1 de ataque complexo",
                    "CA1 F": "consoante fricativa em posição 1 de ataque complexo",
                    "CA1 N": "consoante nasal em posição 1 de ataque complexo",
                    "CA1 L": "consoante líquida em posição 1 de ataque complexo",

                    "CA2 O": "consoante oclusiva em posição 2 de ataque complexo",
                    "CA2 F": "consoante fricativa em posição 2 de ataque complexo",
                    "CA2 N": "consoante nasal em posição 2 de ataque complexo",
                    "CA2 L": "consoante líquida em posição 2 de ataque complexo",
                 
                    "CC1 F": "consoante fricativa em posição 1 de coda complexa",
                    "CC1 N": "consoante nasal em posição 1 de coda complexa",
                    "CC1 L": "consoante líquida em posição 1 de coda complexa",

                    "CC2 F": "consoante fricativa em posição 2 de coda complexa",
                    "CC2 N": "consoante nasal em posição 2 de coda complexa",
                    "CC2 L": "consoante líquida em posição 2 de coda complexa",

                 }



class Gerador:
    def __init__(self, queue, check):
        self.queue = queue
        self.df = pd.read_csv('etiquetas.csv')
        self.df = self.df.drop(self.df.columns[[4]], axis=1)
        self.df.columns = ['Palavra', 'Silaba', 'Fonética', 'Etiqueta']
        self.list_words = list(self.df["Palavra"].str.replace(":", ""))
        self.check = check


    def search_word(self, word):
        row_word = word + ":"
        row_word = self.df.loc[self.df['Palavra'] == row_word]
        if(row_word.empty):
            self.queue(f"Palavra '{word}' não encontrada!")
            return False
        dict_word = row_word.to_dict(orient='records')[0]
        etiqueta = dict_word["Etiqueta"]
        self.sep_silaba = dict_word["Silaba"]
        self.fonetica = dict_word["Fonética"]
        self.fonetica_ori = dict_word["Fonética"]
        self.palavra = dict_word["Palavra"].replace(":", "")
        etiqueta = re.findall(r'\[(.*?)\]', etiqueta)
        # etiqueta = ''.join([i for i in etiqueta if not i.isdigit()])
        # etiqueta = etiqueta.replace("[", "")
        # etiqueta = etiqueta.replace("]", "")
        # etiqueta = etiqueta.split('.')
        self.final_etiqueta = []


        self.sep_silaba_modi = self.sep_silaba

        for doubledLetter, abre in composto_fonetica.items():
            self.sep_silaba_modi = self.sep_silaba_modi.replace(doubledLetter, abre)

        self.sep_silaba_modi = self.sep_silaba_modi.replace("'", "")
        self.sep_silaba_modi = self.sep_silaba_modi.split('.')
        self.fonetica = self.fonetica.replace("'", "")
        self.fonetica = self.fonetica.split('.')


        for eti in etiqueta:
            eti_list = re.split(r'[()]', eti)
            eti_list = [i for i in eti_list if i]
            self.final_etiqueta.append(eti_list)

        # final_etiqueta
        self.final_etiqueta2 = list(itertools.chain.from_iterable(self.final_etiqueta))

        self.palavra_modi = self.palavra
        for doubledLetter, abre in composto_dict.items():
            self.palavra_modi = self.palavra_modi.replace(doubledLetter, abre)

        return True
    
    def gerar_omissao(self):
        omissao_list = []
        for etiqueta in range(len(self.final_etiqueta2)):
            if self.final_etiqueta2[etiqueta] not in nao_omite:
                omissao_list.append(etiqueta)

        resultList = []
        for omissao in omissao_list:
            # print(f"tirando a letra {self.palavra_modi[omissao]}")
            result = self.palavra_modi[0 : omissao : ] + self.palavra_modi[omissao + 1 : :]
            resultList.append(result)

        for result in range(len(resultList)):
            for doubledLetter, abre in composto_dict.items():
                resultList[result] = resultList[result].replace(abre, doubledLetter)

        # self.omissao = resultList

        list_desc = [self.final_etiqueta2[omissao] for omissao in omissao_list]
        list_omitido = [composto_dict_reverse[self.palavra_modi[omissao]] if self.palavra_modi[omissao].isnumeric() else self.palavra_modi[omissao] for omissao in omissao_list]
        list_omitido = [(i, '-') for i in list_omitido]
        omissao_list = [(i,'-') for i in omissao_list]
        if(resultList):
            df = pd.DataFrame(list(zip(resultList,omissao_list,list_omitido,list_desc)))
            df = df.set_axis(['Desvio', 'Índice', 'Mudança', 'Descrição'], axis=1)
            df.insert(0, "Palavra Original", self.palavra)
            df.insert(1, "Separação Silábica", self.sep_silaba)
            df.insert(2, "Fonética", self.fonetica_ori)
            df.insert(4, "Categoria de Desvio", "Omissão")
            return df
        else:
            return pd.DataFrame()

    @staticmethod
    def substitui(silaba, subindex, index, som, sep_silaba, resultList):
        temp = list(silaba)
        temp[subindex] = som
        string = "".join(temp)
        sep_silaba_aux = sep_silaba.copy()
        sep_silaba_aux[index] = string
        resultList.append("".join(sep_silaba_aux))

    def subs_nao_fonologica(self):
        #substituição não fonológica
        #trocar do ch/x também
        resultList = []
        lista_sons = []
        lista_letras = []
        lista_indices = []


        for (index,silaba), fonema in zip(enumerate(self.sep_silaba_modi), self.fonetica):
            for (subindex, letra), som in zip(enumerate(silaba), fonema):
                if(dictSom.get(letra, "Not found") == som):
                    # index = sep_silaba.index(silaba)#silaba
                    # subindex = silaba.index(letra)#onde eu quero subtituir na silaba
                    self.substitui(silaba, subindex, index, som, self.sep_silaba_modi, resultList)
                    lista_sons.append(som)
                    lista_letras.append(letra)
                    lista_indices.append((index, subindex))
                if(letra == "2"):
                    self.substitui(silaba, subindex, index, "ç", self.sep_silaba_modi, resultList)
                    lista_sons.append("ç")
                    lista_letras.append(letra)
                    lista_indices.append((index, subindex))
                if(letra == "2" and silaba[subindex+1] in ["e","i"]):
                    self.substitui(silaba, subindex, index, "c", self.sep_silaba_modi, resultList)
                    lista_sons.append("c")
                    lista_letras.append(letra)
                    lista_indices.append((index, subindex))

        for result in range(len(resultList)):
            for doubledLetter, abre in composto_fonetica.items():
                resultList[result] = resultList[result].replace(abre, doubledLetter)          

        lista_letras = [composto_fonetica_inverse[letra] if letra.isnumeric() else letra for letra in lista_letras]
        lista_final= list(zip(lista_letras,lista_sons))
        lista_desc = [self.final_etiqueta[i[0]][i[1]] for i in lista_indices]
        
        if(resultList):
            df = pd.DataFrame(list(zip(resultList,lista_indices, lista_final, lista_desc)))
            df = df.set_axis(['Desvio', 'Índice', 'Mudança', 'Descrição'], axis=1)
            df.insert(0, "Palavra Original", self.palavra)
            df.insert(1, "Separação Silábica", self.sep_silaba)
            df.insert(2, "Fonética", self.fonetica_ori)
            df.insert(4, "Categoria de Desvio", "Substituição não fonológica")
            return df
        else:
            return pd.DataFrame()



    def subs_orto_classe(self):
        #substituição ortografia fonologica dentro da classe
        resultList = []
        lista_letra = []
        lista_subs = []
        lista_classe = []
        lista_indices = []


        for (index,letra), etiqueta in zip(enumerate(self.palavra_modi), self.final_etiqueta2):
            for subs in dictEtiquetas.get(etiqueta, []):
                if(letra == subs):
                    continue
                if(etiqueta == "CA2 L"):
                    if(self.palavra_modi[index-1] + subs not in CA):
                        continue
                tempList = list(self.palavra_modi)
                tempList[index] = subs
                lista_letra.append(letra)
                lista_subs.append(subs)
                lista_indices.append(index)
                lista_classe.append(etiqueta.split()[1])
                string = "".join(tempList)
                resultList.append(string)

        for result in range(len(resultList)):
            for doubledLetter, abre in composto_dict.items():
                resultList[result] = resultList[result].replace(abre, doubledLetter)
        
        # self.subs_orto_classe = resultList
        lista_desc = [self.final_etiqueta2[i] for i in lista_indices]
        lista_subs = [composto_dict_reverse[subs] if subs.isnumeric() else subs for subs in lista_subs]
        lista_letra = [composto_dict_reverse[letra] if letra.isnumeric() else letra for letra in lista_letra]
        lista_final = list(zip(lista_letra, lista_subs))
        lista_indices = [(i,'-') for i in lista_indices]
        
        if(resultList):
            df = pd.DataFrame(list(zip(resultList,lista_indices, lista_final, lista_desc)))
            df = df.set_axis(['Desvio', 'Índice', 'Mudança', 'Descrição'], axis=1)
            df.insert(0, "Palavra Original", self.palavra)
            df.insert(1, "Separação Silábica", self.sep_silaba)
            df.insert(2, "Fonética", self.fonetica_ori)
            df.insert(4, "Categoria de Desvio", "Substituição fonológica")
            return df
        else:
            return pd.DataFrame()

    @staticmethod
    def troca(silab_word_l, a, b, sep_silaba, resultList,index_silab):
        silab_word_l[a], silab_word_l[b] = silab_word_l[b], silab_word_l[a]
        sep_silaba_copy = sep_silaba.copy()
        troca = "".join(silab_word_l)
        sep_silaba_copy[index_silab] = troca
        resultList.append("".join(sep_silaba_copy))
        return troca

    def transposicao_dentro(self):
        #transposições dentro da silaba
        resultList = []
        lista_troca = []
        lista_desc = []
        lista_silab = []
        lista_indices = []


        for silab_eti, (index_silab,silab_word) in zip(self.final_etiqueta, enumerate(self.sep_silaba_modi)):
            caso = [i.split()[0] for i in silab_eti]
            silab_word_l = list(silab_word)
            if(caso == ['CA1', 'CA2', 'SN']):
                if(silab_word_l[1] in SC):
                    troca_result = Gerador.troca(silab_word_l, 1, 2, self.sep_silaba_modi, resultList,index_silab)
                    lista_desc.append("CA CA SN - SA SN SC")
                    lista_troca.append(troca_result)
                    lista_silab.append(silab_word)
                    lista_indices.append((index_silab, 1, 2))  

            if(caso == ['SA', 'SN', 'SC']):
                if((silab_word_l[0] + silab_word_l[2]) in CA):
                    troca_result = Gerador.troca(silab_word_l, 1, 2, self.sep_silaba_modi, resultList,index_silab)
                    lista_desc.append("SA SN SC - CA CA SN")
                    lista_troca.append(troca_result)
                    lista_silab.append(silab_word)
                    lista_indices.append((index_silab, 1, 2))                
                
                if((silab_word_l[0] + silab_word_l[2]) in CC):
                    troca_result = Gerador.troca(silab_word_l, 0, 1, self.sep_silaba_modi, resultList,index_silab)
                    lista_desc.append("SA SN SC - SN CC CC")
                    lista_troca.append(troca_result)
                    lista_silab.append(silab_word)
                    lista_indices.append((index_silab, 1, 2))        
        
        # self.transposicao_silaba = resultList
        for result in range(len(resultList)):
            for doubledLetter, abre in composto_fonetica.items():
                resultList[result] = resultList[result].replace(abre, doubledLetter)
        
        lista_final = list(zip(lista_silab, lista_troca))
        if(resultList):
            df = pd.DataFrame(list(zip(resultList, lista_indices, lista_final, lista_desc)))
            df = df.set_axis(['Desvio', 'Índice', 'Mudança', 'Descrição'], axis=1)
            df.insert(0, "Palavra Original", self.palavra)
            df.insert(1, "Separação Silábica", self.sep_silaba)
            df.insert(2, "Fonética", self.fonetica_ori)
            df.insert(4, "Categoria de Desvio", "Transposições")
            return df
        else:
            return pd.DataFrame()


    def gerar_n_desvios_aleatorios(self, quantidade, categoria):
        self.queue(f"Gerando {quantidade} da categoria {categoria}")
        
        df_final = pd.DataFrame(columns=["Palavra Original", "Separação Silábica", "Desvio", "Categoria de Desvio", "Índice", "Mudança", "Descrição"])
        obtido = 0
        escolhido = []
        dict_escolha = {"omissao": self.gerar_omissao, "nao fonologica": self.subs_nao_fonologica, "fonologica": self.subs_orto_classe, "transposicao": self.transposicao_dentro}

        while(obtido < quantidade):
            word = random.choice(self.list_words)
            if(word in escolhido):
                continue
            else:
                escolhido.append(word)
            self.search_word(word)
            try:
                df = dict_escolha[categoria]()
            except:
                continue
            if(not df.empty):
                df_final = pd.concat([df_final, df])
            obtido += len(df.index)
    
        df_final = df_final.reset_index(drop=True)
        df_final = df_final.head(quantidade)
        return df_final
    
    def gerar_desvios(self, list_word):
        
        df_final = pd.DataFrame(columns=["Palavra Original", "Separação Silábica", "Fonética", "Desvio", "Categoria de Desvio", "Índice", "Mudança", "Descrição"])
        dict_escolha = {"omissões": self.gerar_omissao, "substituições não fonológicas": self.subs_nao_fonologica, "substituições fonológicas": self.subs_orto_classe, "transposições": self.transposicao_dentro}
        for word in list_word:
            if(not self.search_word(word)):
                continue
            
            for nome, funcao in dict_escolha.items():
                try:
                    df1 = funcao()
                    if(df1.empty):
                        self.queue(f"Não há {nome} para a palavra '{word}'!")
                    else:
                        df_final = pd.concat([df_final, df1])
                except:
                    self.queue(f"Não foi possível gerar {nome} da palavra '{word}'!")

        if(df_final.empty):
            self.queue("Nenhum desvio gerado com as palavras inseridas!")
            return
        
        df_final = df_final.reset_index(drop=True)
        result = list(df_final["Desvio"])
        result = "\n".join(result)
        self.queue(f"Gerou\n{result}")
        if(self.check == "on"):
            self.queue("Escrevendo arquivo")
            name = f"Desvio_{datetime.now().hour}_{datetime.now().minute}.xlsx"
            df_final.to_excel(name, sheet_name="Desvios", index=False)
            self.queue("Arquivo escrito!")

    def gerar_desvios_categorias(self, dict_categorias):
        if(not any(list(dict_categorias.values()))):
            self.queue("Categorias vazias!")
            return
        df_final = pd.DataFrame(columns=["Palavra Original", "Separação Silábica", "Fonética", "Desvio", "Categoria de Desvio", "Índice", "Mudança", "Descrição"])
        for categoria, quantidade in dict_categorias.items():
            df_aux = self.gerar_n_desvios_aleatorios(quantidade, categoria)
            df_final = pd.concat([df_final, df_aux])
        df_final = df_final.reset_index(drop=True)
        result = list(df_final["Desvio"])
        result = "\n".join(result)
        self.queue(f"Gerou\n{result}")
        if(self.check == "on"):
            self.queue("Escrevendo arquivo")
            name = f"Desvio_{datetime.now().hour}_{datetime.now().minute}.xlsx"
            df_final.to_excel(name, sheet_name="Desvios", index=False)
            self.queue("Arquivo escrito!")

# gerador = Gerador("")
# print(gerador.gerar_desvios_categorias({"omissao": 10, "fonologica":2}))
# print(gerador.gerar_n_desvios_aleatorios(100, "nao fonologica"))
# print(gerador.gerar_desvios(["professor", "belo"]))
# list_word = ["professor", "exceção", "belo", "perguntas"]

# gerador.search_word("professor")
# df1 = gerador.gerar_omissao()
# df2 = gerador.subs_nao_fonologica()
# df3 = gerador.subs_orto_classe()
# df4 = gerador.transposicao_dentro()
# dfFinal = pd.concat([df1,df2,df3,df4])
# print(dfFinal)
# print(df3)
# dfFinal.to_excel("Professor.xlsx", sheet_name="Desvios", index=False)