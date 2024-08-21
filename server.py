import rpyc
import rpyc.utils
import os
import pandas as pd
from threading import Thread

class Arquivos(rpyc.Service):
    def on_connect(self, conn):
        print("CONEXÃO ESTABELECIDA")

    def on_disconnect(self, conn):
        print("CONEXÃO DESFEITA")

    def exposed_listar_arquivos(self):
        return os.listdir("arquivos")
    
    def exposed_download(self, name_file):
        with open(f'arquivos/{name_file}', 'r') as file:
            data = file.read()
        return data
        
    def exposed_upload(self, name_file, data):
        with open(f"arquivos/{name_file}", 'w') as f:
            f.write(data)

    def exposed_listar_interesses(self, usuario):
        dados = pd.read_csv("interesses.csv")
        dados = dados.loc[dados["user"]== usuario]
        return dados.values.tolist()

    def exposed_adicionar_interesse(self, usuario, nome):
        try:
            dados = pd.read_csv("interesses.csv")

            user = dados["user"].to_list()
            interesse = dados["interesse"].to_list()
            existe = dados["existe"].to_list()

            user.append(usuario)
            interesse.append(nome)

            if nome in os.listdir("arquivos"): 
                existe.append("sim") 
            else: 
                existe.append("não")

            dados = pd.DataFrame({"user": user, "interesse": interesse, "existe": existe})

            dados.to_csv("interesses.csv")
            return True
        except Exception as e:
            print(e)
            return False

    def exposed_retirar_interesse(self, usuario, nome):
        try:
            dados = pd.read_csv("interesses.csv")
            index = dados.index[(dados["user"] == usuario) & (dados["interesse"] == nome)]

            dados = dados.drop([index[0]])

            user = dados["user"].to_list()
            interesse = dados["interesse"].to_list()
            existe = dados["existe"].to_list()

            dados = pd.DataFrame({"user": user, "interesse": interesse, "existe": existe})

            dados.to_csv("interesses.csv")

            return True
        except Exception as e:
            print(e)
            return False

    class exposed_user(object):
        def __init__(self, callback, user, interval = 1):
            self.user = user
            self.n_arquivos = len(os.listdir("arquivos"))
            self.interval = interval
            self.callback = rpyc.async_(callback)  
            self.active = True
            self.thread = Thread(target = self.work)
            self.thread.start()
        def exposed_stop(self):   # this method has to be exposed too
            self.active = False
            self.thread.join()
        def work(self):
            while self.active:
                n_arq = len(os.listdir("arquivos"))

                if self.n_arquivos != n_arq:
                    arquivos = os.listdir("arquivos")
                    dados = pd.read_csv("interesses.csv")
                    aux = dados.loc[dados["user"]== self.user]
                    interesse = aux["interesse"].to_list()

                    for arq in arquivos:
                        for index, inte in enumerate(interesse):
                            print(f"ARQUIVO: {arq}")
                            print(f"INTERESSE: {inte}")
                            if arq == inte:
                                user = dados["user"].to_list()
                                interesse = dados["interesse"].to_list()
                                existe = dados["existe"].to_list()

                                existe[index] = "sim"

                                dados = pd.DataFrame({"user": user, "interesse": interesse, "existe": existe})
                                dados.to_csv("interesses.csv")
                                self.callback(self.user, arq)
                self.n_arquivos = n_arq


if __name__ == "__main__":
    from rpyc.utils.server import ThreadPoolServer
    server = ThreadPoolServer(Arquivos, port=12345)
    server.start()