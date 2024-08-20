import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import simpledialog
from client import Gerente
from tkinter import messagebox 
import os

user = simpledialog.askstring(title="USER", prompt="NOME DE USUÁRIO")

# Objeto que conecta com o arquivo cliente
gen = Gerente(user)

# Cria a janela principal da aplicação e define suas propriedades.
app = tk.Tk("Aplicacao")
app.title("Gerente de Arquivos")
app.geometry("680x300")

background = "#aea9ba"

app.configure(bg=background)

"""SEÇÃO: ARQUIVOS DISPONÍVEIS"""
# Cria uma seção para exibir os arquivos disponíveis.
lblFrm_consult_section = tk.LabelFrame(master=app, text="CONSULTA", font=("Arial", 12, "bold"), bg=background)
lblFrm_consult_section.grid(column=0, row=0, rowspan=2)

# TreeView que mostra os arquivos disponíveis na seção de consulta.
tv_consult = ttk.Treeview(lblFrm_consult_section, columns=('nome', 'tamanho'), show='headings')
tv_consult.column('nome', minwidth=10, width=200)
tv_consult.column('tamanho', minwidth=10, width=100)
tv_consult.heading('nome', text='NOME')
tv_consult.heading('tamanho', text='TAMANHO(B)')
tv_consult.grid(column=0, row=0, columnspan=2)

# Listar os arquivos disponíveis através do metodo de listagem
for arq in gen.get_arquivos():
    tv_consult.insert("", "end", values=(arq, os.stat(f"Arquivos/{arq}").st_size))

# Criação de uma Scrollbar vertical para a TreeView.
scrollbar_consult = ttk.Scrollbar(lblFrm_consult_section, orient="vertical", command=tv_consult.yview)
# Configura a TreeView para usar a Scrollbar.
tv_consult.configure(yscrollcommand=scrollbar_consult.set)
# Coloca a Scrollbar ao lado direito da TreeView.
scrollbar_consult.grid(column=2, row=0, sticky='NS')

def download():
    # Pega as informações do treeView e faz download do item
    id_item = tv_consult.focus()
    json_dados = tv_consult.item(id_item)
    nome_arquivo = json_dados["values"][0]
    dados = gen.download(nome_arquivo) # Download
    
    # Abre uma caixa de diálogo e escreve os dados na pasta selecionada
    directory = askdirectory()
    with open(f"{directory}/{nome_arquivo}", 'w') as f:
        f.write(dados)
    
    messagebox.showinfo("showinfo", f"Download para {directory} de {nome_arquivo} realizado com sucessor")

# Botão para realizar o download do arquivo selecionado (ação precisa ser implementada).
btn_download = tk.Button(
    master=lblFrm_consult_section,
    background="#4d4dff",
    text="DOWNLOAD",
    foreground="white",
    font=("Arial", 12, "bold"),
    command=lambda: download()  # Placeholder para a função de download
)
btn_download.grid(column=0, row=1, sticky="EW", padx=5, pady=5)

"""SEÇÃO: UPLOAD""" 

def upload_area():
    up_app = tk.Tk("Aplicacao")
    up_app.title("UPLOAD")
    up_app.geometry("400x130")
    up_app.attributes('-topmost',True)

    # Cria uma LabelFrame de seção para upload de arquivos.
    lblFrm_upload_section = tk.LabelFrame(master=up_app, text="PESQUISA", font=("Arial", 12, "bold"))
    lblFrm_upload_section.grid(column=1, row=0)

    # Label de orientação para o usuário.
    lbl_upload_text = tk.Label(master=lblFrm_upload_section, text="SELECIONE UM ARQUIVO PARA UPLOAD")
    lbl_upload_text.grid(column=0, row=0)

    # Método que abre o explorador de arquivos para selecionar um arquivo e atualiza o label com o nome do arquivo.
    def getFile(path):
        if len(path) == 1:
            path.pop(0)
        up_app.attributes('-topmost',False)
        path.append(askopenfilename())
        up_app.attributes('-topmost',True)
        lbl_file_name["text"] = path[0]  # Atualiza o label com o caminho do arquivo selecionado

    path = []
    # Botão para selecionar o arquivo a ser carregado e chama a função getFile.
    btn_upload_select = tk.Button(
        master=lblFrm_upload_section, 
        text="ESCOLHA UM ARQUIVO", 
        command=lambda: getFile(path)
    )
    btn_upload_select.grid(column=1, row=0, sticky=tk.N, padx=10)

    def upload():
        # Pergunta ao usuário o nome do arquivo a ser carregado
        nome_arquivo = simpledialog.askstring(title="NAME", prompt="QUAL O NOME DO ARQUIVO")

        # Lê o arquivo selecionado e guarda seu conteúdo
        with open(path[0], 'r') as file:
            data = file.read()

        # Manda as informações para serem salvas
        gen.upload(nome_arquivo, data)

        # Deleta todos os itens de "consulta" e os recarrega
        for i in tv_consult.get_children():
            tv_consult.delete(i)
        for arq in gen.get_arquivos():
            tv_consult.insert("", "end", values=(arq))

        # Avisa ao usuário que o upload foi feito
        messagebox.showinfo("showinfo", f"UPLOAD DE {nome_arquivo} FEITO COM SUCESSO")

    # Botão para confirmar o carregamento do arquivo selecionado
    btn_upload = tk.Button(
        master=lblFrm_upload_section, 
        text="CONFIRMAR UPLOAD", 
        command=lambda: upload()
    )
    btn_upload.grid(column=0, row=2, sticky=tk.N, padx=10, columnspan=2)

    # Label que exibe o nome do arquivo selecionado para upload.
    lbl_file_name = tk.Label(master=lblFrm_upload_section, text="NOME DO ARQUIVO")
    lbl_file_name.grid(column=0, row=1, columnspan=2)

    up_app.mainloop()

btn_upload_area = tk.Button(
    master=lblFrm_consult_section, 
    text="UPLOAD", 
    background="#4d4dff",
    foreground="white",
    font=("Arial", 12, "bold"), 
    command= upload_area)
btn_upload_area.grid(column=1, row=1, sticky="EW", padx=5, pady=5)


"""SEÇÃO: INTERESSES"""
# Cria uma seção para exibir os interesses do usuário.
lblFrm_interest_section = tk.LabelFrame(master=app, text="INTERESSES", font=("Arial", 12, "bold"), bg=background)
lblFrm_interest_section.grid(column=1, row=0, padx=5)

# TreeView que mostra os interesses do usuário.
tv_interest = ttk.Treeview(lblFrm_interest_section, columns=('interesses', 'existe'), show='headings', height=5)
tv_interest.column('interesses', minwidth=10, width=100)
tv_interest.column('existe', minwidth=10, width=10)
tv_interest.heading('interesses', text='INTERESSE')
tv_interest.heading('existe', text='EXISTE')
tv_interest.grid(column=0, row=0, ipadx=50, sticky='NS')

# Leitura do arquivo de interesses no servidor
for arq in gen.get_interreses():
    tv_interest.insert("", "end", values=(arq[2], arq[3]))

# Criação de uma Scrollbar vertical para a TreeView de interesses.
scrollbar_interest = ttk.Scrollbar(lblFrm_interest_section, orient="vertical", command=tv_interest.yview)
# Configura a TreeView para usar a Scrollbar.
tv_interest.configure(yscrollcommand=scrollbar_interest.set)
# Coloca a Scrollbar ao lado direito da TreeView.
scrollbar_interest.grid(column=1, row=0, sticky='NS')

# Função que adiciona um interesse
def new_interest():
    # Pergunta ao usuário o nome do novo interesse
    nome_arquivo = simpledialog.askstring(title="NAME", prompt="QUAL O NOME DO ARQUIVO DE INTERESSE")

    # Manda o nome do arquivo para ser salvo
    gen.set_novo_interesse(nome_arquivo)

    # Deleta todos os itens de "interesses" e os recarrega
    for i in tv_interest.get_children():
        tv_interest.delete(i)
    for arq in gen.get_interreses():
        tv_interest.insert("", "end", values=(arq[2], arq[3]))

# Botão para adicionar um novo interesse (ação precisa ser implementada).
btn_new = tk.Button(
    master=lblFrm_interest_section,
    background="#494454",
    foreground="white",
    font=("Arial", 9, "bold"), 
    text="NOVO INTERESSE",
    command=lambda: new_interest()
)
btn_new.grid(column=0, row=1, sticky="EW", columnspan=2, padx=2.5, pady=2.5)

# Função para cancelar interesse
def drop_interest():
    # Pega as informações do treeView e faz deleta o item
    id_item = tv_interest.focus()
    json_dados = tv_interest.item(id_item)
    nome_arquivo = json_dados["values"][0]

    # Chama a função que exclui
    gen.drop_interesse(nome_arquivo)

    # Deleta o item selecionado
    tv_interest.delete(id_item)

    # Avisa ao usuário que o interesse foi exvluido
    messagebox.showinfo("showinfo", f"EXCLUSÃO DE {nome_arquivo} FEITA COM SUCESSO")

# Botão para cancelar um interesse (ação precisa ser implementada).
btn_new = tk.Button(
    master=lblFrm_interest_section,
    background="#494454",
    foreground="white",
    font=("Arial", 9, "bold"), 
    text="CANCELAR INTERESSE",
    command=lambda: drop_interest() 
)
btn_new.grid(column=0, row=2, columnspan=2, sticky="EW", padx=2.5, pady=2.5)

# Inicia o loop principal da aplicação, que mantém a janela aberta.
app.mainloop()
