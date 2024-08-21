import rpyc
from tkinter import messagebox 

class Gerente():
    def __init__(self, user, event):
        self.user = user
        self.conn = rpyc.connect("localhost", 12345)
        self.gerente_arquivos = self.conn.root

        self.bgsrv = rpyc.BgServingThread(self.conn) 

        self.event_listener = self.conn.root.user(event, self.user)
    
    def evento(self, nome_arquivo):
        messagebox.showinfo("showinfo", f"{self.user}, 0 arquivo {nome_arquivo} de seu interesse foi carregado")

    def get_arquivos(self):
        return self.gerente_arquivos.listar_arquivos()
    
    def download(self, nome):
        return self.gerente_arquivos.download(nome)
    
    def upload(self, nome, dados):
        return self.gerente_arquivos.upload(nome, dados)
    
    def get_interreses(self):
        return self.gerente_arquivos.listar_interesses(self.user)
    
    def set_novo_interesse(self, nome):
        return self.gerente_arquivos.adicionar_interesse(self.user, nome)
    
    def drop_interesse(self, nome):
        self.gerente_arquivos.retirar_interesse(self.user, nome)

    def close(self):
        self.event_listener.stop()
        self.bgsrv.stop()
        self.conn.close()
