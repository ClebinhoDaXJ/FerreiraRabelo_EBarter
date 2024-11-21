import tkinter as tk
from tkinter import messagebox
import time
import socket
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dicionário para armazenar sociedades
sociedades = {}

# Variável global para armazenar o widget do gráfico
grafico_canvas = None

def enviar_mensagem(comando):
    host = '127.0.0.1'  # Endereço do servidor (localhost)
    porta = 12345        # Porta do servidor

    try:
        # Criação do socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((host, porta))  # Conecta ao servidor
            cliente.sendall(comando.encode('utf-8'))  # Envia o comando
            print(f"Mensagem enviada: {comando}")
    except ConnectionRefusedError:
        print("Não foi possível conectar ao servidor. Certifique-se de que ele está em execução.")


def processar_arquivo(nome_arquivo):
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(nome_arquivo):
            raise FileNotFoundError(f"O arquivo {nome_arquivo} não foi encontrado.")
        
        # Abre e lê o conteúdo do arquivo
        with open(nome_arquivo, 'r') as arquivo:
            conteudo = arquivo.read().strip()  # Remove espaços e quebras de linha
            print(f"Conteúdo do arquivo: {conteudo}")
        
        # Converte o conteúdo em uma lista de floats
        lista_floats = [float(valor) for valor in conteudo.split(';')]
        print(f"Lista de floats: {lista_floats}")
        
        # Exclui o arquivo
        os.remove(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' excluído com sucesso.")
        
        return lista_floats
    except FileNotFoundError as e:
        print(e)
        return []
    except ValueError as e:
        print(f"Erro ao converter valores do arquivo em floats: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

def atualizar_variavel_y_em_cpp(valor):
    enviar_mensagem(f"y={valor}")

def atualizar_variavel_x_em_cpp():
    enviar_mensagem("x=1")

def criar_grafico(lista_floats, nome_moeda):
    """
    Cria e exibe um gráfico usando matplotlib com base na lista de floats.
    O título do gráfico incluirá o nome da moeda.
    """
    # Verifica se há valores na lista
    if not lista_floats:
        messagebox.showwarning("Aviso", "A lista de valores está vazia. Não foi possível gerar o gráfico.")
        return

    # Configura o gráfico
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(len(lista_floats)), lista_floats, marker='o', linestyle='-', color='blue')
    ax.set_title(f"Evolução da moeda {nome_moeda}")
    ax.set_xlabel("Transações")
    ax.set_ylabel("Valores")
    ax.grid()

    # Integrar o gráfico no Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)  # 'root' é a janela principal
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=850, y=375)  # Ajusta a posição ao lado do frame_moedas
    
    return canvas_widget  # Retorna o widget do gráfico para futuras remoções

# Função para fechar o aplicativo
def sair():
    root.destroy()

# Função para exibir a janela "Nova Simulação" (2ª janela)
def nova_simulacao():
    frame_new_sim.place(x=20, y=150)
    sim_name_entry.delete(0, tk.END)

# Função para criar a simulação e abrir a 3ª janela com detalhes
def criar_simulacao():
    sim_name = sim_name_entry.get()
    if sim_name.strip():
        simulations.append(sim_name)
        frame_new_sim.place_forget()
        mostrar_detalhes_simulacao(sim_name)
        construtor()
    
        # Atualiza a variável no arquivo temporário
        atualizar_variavel_x_em_cpp()
    else:
        messagebox.showwarning("Erro", "O nome da simulação não pode estar vazio!")


# Função para exibir a 3ª janela com os detalhes da simulação criada
def mostrar_detalhes_simulacao(sim_name):
    label_sim_name.config(text=f"Simulação: {sim_name}")
    frame_sim_details.place(x=220, y=150)
    
    # Atualizar o título das janelas "sociedades" e "moedas"
    label_sociedades.config(text=f"Sociedades - {sim_name}")
    label_moedas.config(text=f"Moedas - {sim_name}")
    
    # Posicionar e redimensionar as janelas "sociedades" e "moedas"
    frame_sociedades.place(x=600, y=80, width=800, height=325)
    frame_moedas.place(x=600, y=450, width=800, height=325)

# Função para exibir simulações arquivadas
def mostrar_arquivadas():
    frame_arquivadas.place(x=20, y=150)
    arquivadas_listbox.delete(0, tk.END)
    for sim in simulations:
        arquivadas_listbox.insert(tk.END, sim)

# Função para carregar uma simulação a partir das arquivadas
def carregar_simulacao(event):
    try:
        selecionada = arquivadas_listbox.get(arquivadas_listbox.curselection())
        frame_arquivadas.place_forget()
        mostrar_detalhes_simulacao(selecionada)
    except IndexError:
        pass

# Função para sair da simulação e fechar todas as janelas relacionadas
def sair_simulacao():
    global grafico_canvas

    frame_sim_details.place_forget()
    frame_sociedades.place_forget()  # Fechar a janela "Sociedades"
    frame_moedas.place_forget()      # Fechar a janela "Moedas"

    # Remover o gráfico, se estiver presente
    if grafico_canvas:
        grafico_canvas.place_forget()
        grafico_canvas = None  # Limpar a referência

# Função para abrir a janela "Adicionar Sociedade"
def abrir_janela_sociedade():
    frame_add_soc.place(x=220, y=150)  # Exibe a janela para adicionar sociedade
    for entry in [entry_nome_soc, entry_qtd_moeda, entry_nome_moeda, entry_qtd_bens, entry_dific_bens, entry_necess_bens]:
        entry.delete(0, tk.END)  # Limpa os campos de entrada

def abrir_janela_simular():
    # Limpa o frame antes de reconfigurá-lo
    frame_simular.place_forget()  # Remove o frame da interface, caso já esteja aberto
    for widget in frame_simular.winfo_children():
        widget.destroy()  # Remove widgets anteriores do frame

    # Configurar o frame para seguir o estilo desejado
    frame_simular.config(bg="white", highlightbackground="black", highlightthickness=2, bd=5)
    frame_simular.place(x=220, y=350)

    # Título no topo do frame
    titulo = tk.Label(
        frame_simular,
        text="Simulação de Transações",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="black",
        anchor="center"
    )
    titulo.pack(fill="x", pady=(5, 10))

    # Rótulo e campo para quantidade de transações
    label_qtd = tk.Label(
        frame_simular,
        text="Quantidade de Transações:",
        font=("Arial", 10),
        bg="white",
        fg="black",
        anchor="w"
    )
    label_qtd.pack(fill="x", padx=10, pady=(5, 0))

    entry_qtd_transa = tk.Entry(frame_simular, font=("Arial", 10), bd=2, relief="groove")
    entry_qtd_transa.pack(fill="x", padx=10, pady=5)

    # Rótulo para moeda a ser analisada
    label_moeda = tk.Label(
        frame_simular,
        text="Moeda a ser Analisada:",
        font=("Arial", 10),
        bg="white",
        fg="black",
        anchor="w"
    )
    label_moeda.pack(fill="x", padx=10, pady=(10, 0))

    # Dropdown para seleção de moeda
    moedas = listbox_moedas.get(0, tk.END)  # Obtém as moedas da listbox existente
    moeda_selecionada = tk.StringVar(frame_simular)
    dropdown_moedas = tk.OptionMenu(frame_simular, moeda_selecionada, *moedas)
    dropdown_moedas.config(font=("Arial", 10), bg="white", bd=1, relief="solid", highlightthickness=0)
    dropdown_moedas.pack(fill="x", padx=10, pady=5)

    # Botão para executar simulação
    btn_simular_confirmar = tk.Button(
        frame_simular,
        text="Executar Simulação",
        font=("Arial", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#45A049",
        bd=2,
        relief="raised",
        command=lambda: executar_simulacao(entry_qtd_transa, moeda_selecionada.get(), moedas)
    )
    btn_simular_confirmar.pack(fill="x", padx=10, pady=10)

    # Botão de voltar
    btn_voltar_simu = tk.Button(
        frame_simular,
        text="Voltar",
        font=("Arial", 10, "bold"),
        bg="#f44336",
        fg="white",
        activebackground="#d32f2f",
        bd=2,
        relief="raised",
        command=frame_simular.place_forget
    )
    btn_voltar_simu.pack(fill="x", padx=10, pady=(0, 10))


def executar_simulacao(entry_qtd_transa, moeda_selecionada, moedas):
    qtd_transacoes = entry_qtd_transa.get().strip()

    # Validações
    if not qtd_transacoes.isdigit():
        messagebox.showerror("Erro", "A quantidade de transações deve ser um número válido!")
        return
    if moeda_selecionada not in moedas:
        messagebox.showerror("Erro", "Por favor, selecione uma moeda válida!")
        return

    indice_moeda = moedas.index(moeda_selecionada)

    # Exibe os dados e inicia a simulação
    messagebox.showinfo(
        "Simulação",
        f"Simulação iniciada com:\n- Transações: {qtd_transacoes}\n- Índice Moeda: {indice_moeda}"
    )
    
    # Fechar a janela de simulação
    frame_simular.place_forget()

    # Atualizar variáveis no backend
    atualizar_variavel_y_em_cpp(5)

    time.sleep(3)

    # Enviar mensagem ao backend
    enviar_mensagem(f"numero_op={qtd_transacoes}|z={indice_moeda}")

    time.sleep(5)

    lista = processar_arquivo("simulacao.txt")

    global grafico_canvas
    grafico_canvas = criar_grafico(lista, moeda_selecionada)


# Função para remover uma sociedade
def remover_sociedade():
    try:
        # Obtém a sociedade selecionada na lista
        selecionada = listbox_sociedades.get(listbox_sociedades.curselection())
        indice_selecionado = listbox_sociedades.curselection()[0]
        nome_sociedade = listbox_sociedades.get(indice_selecionado)
        
        # Confirmação antes de remover
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover a sociedade '{selecionada}'?"):
            # Remove do dicionário e da lista
            del sociedades[selecionada]
            listbox_sociedades.delete(listbox_sociedades.curselection())
            listbox_moedas.delete(indice_selecionado)
            

            # Fecha a janela de detalhes, se estiver aberta
            frame_detalhes_soc.place_forget()
            messagebox.showinfo("Sucesso", f"Sociedade '{selecionada}' removida com sucesso!")

            atualizar_variavel_y_em_cpp(3)

            time.sleep(1)

            # Montar mensagem estruturada e enviar para o backend C++
            mensagem = (
                f"snametormv={nome_sociedade}"
            )
            enviar_mensagem(mensagem)
    except IndexError:
        messagebox.showwarning("Erro", "Nenhuma sociedade selecionada para remover.")

# Função para criar uma nova sociedade
def criar_sociedade():
    nome = entry_nome_soc.get().strip()
    qtd_moeda = entry_qtd_moeda.get().strip()
    moeda = entry_nome_moeda.get().strip()
    bens = entry_qtd_bens.get().strip()
    dificuldade = entry_dific_bens.get().strip()
    necessidade = entry_necess_bens.get().strip()

    if not nome or not qtd_moeda or not moeda or not bens or not dificuldade or not necessidade:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    try:
        # Converte os bens para uma lista de inteiros
        bens_list = list(map(int, bens.split(";")))
        dificuldade_list = list(map(int, dificuldade.split(";")))
        necessidade_list = list(map(int, necessidade.split(";")))

        # Salvar sociedade no dicionário
        sociedades[nome] = {
            "quantidade_inicial": qtd_moeda,
            "moeda": moeda,
            "bens": bens_list,
            "dificuldade": dificuldade_list,
            "necessidade": necessidade_list,
        }

        # Adicionar nome à lista de sociedades
        listbox_sociedades.insert(tk.END, nome)
        listbox_moedas.insert(tk.END, moeda)

        # Fechar a janela de criação
        frame_add_soc.place_forget()

        atualizar_variavel_y_em_cpp(1)

        time.sleep(1)

        # Montar mensagem estruturada e enviar para o backend C++
        mensagem = (
            f"sname={nome}|cname={moeda}|"
            f"qtds={bens}|difcs={dificuldade}|necs={necessidade}|initialQtd={qtd_moeda}"
        )
        enviar_mensagem(mensagem)

    except ValueError:
        messagebox.showwarning("Erro", "Quantidade de bens deve ser uma lista de inteiros separados por ';'!")


# Função para exibir os detalhes da sociedade selecionada
def exibir_detalhes_sociedade(event):
    try:
        selecionada = listbox_sociedades.get(listbox_sociedades.curselection())
        detalhes = sociedades[selecionada]

        # Exibe janela de detalhes
        frame_detalhes_soc.place(x=1100, y=150) 
        label_nome_soc.config(text=f"Sociedade: {selecionada}")
        label_moeda.config(text=f"Nome da Moeda: {detalhes['moeda']}")
        label_bens.config(text=f"Quantidade de Bens: {detalhes['bens']}")
        label_dificuldade.config(text=f"Dificuldade dos Bens: {detalhes['dificuldade']}")
        label_necessidade.config(text=f"Necessidade dos Bens: {detalhes['necessidade']}")
    except IndexError:
        pass

# Função para exibir os detalhes do bem selecionado
def exibir_detalhes_bens(event):
    try:
        # Obtém o índice do bem selecionado
        indice_selecionado = listbox_bens.curselection()[0]
        bem = listbox_bens.get(indice_selecionado)
        
        quantidade = 0
        for sociedade in sociedades.values():
            bens = sociedade["bens"] 
            quantidade += bens[indice_selecionado]

        # Posiciona o frame de detalhes
        frame_detalhes_bens.place(x=180, y=450)

        # Exibe a mensagem no frame de detalhes
        mensagem = f"A quantidade do bem {bem} é: {quantidade}"
        label_quantidade_bens.config(text = mensagem)

    
    except IndexError:
        # Caso nenhum item esteja selecionado, nada acontece
        pass

# Função para abrir a janela "Add Bem"
def abrir_janela_add_bem():
    frame_add_bem.place(x=220, y=400)  # Posiciona o frame para adicionar bens
    entry_nome_bem.delete(0, tk.END)  # Limpa o campo de entrada

# Função para adicionar um novo bem
def adicionar_bem():
    nome_bem = entry_nome_bem.get().strip()
    vqtd_bens = entry_vqtd_bens.get().strip()
    vdif_bens = entry_vdif_bens.get().strip()
    vnec_bens = entry_vnec_bens.get().strip()

    if not nome_bem:
        messagebox.showwarning("Erro", "O vetor nome deve ser preenchido")
        return

    # Obter a simulação atual
    sim_name = label_sim_name["text"].split(": ")[1]

    # Adicionar o bem à lista correspondente
    if sim_name not in bens_por_simulacao:
        bens_por_simulacao[sim_name] = []
    bens_por_simulacao[sim_name].append(nome_bem)

    # Atualizar a exibição da lista de bens
    atualizar_lista_bens(sim_name)

    if vqtd_bens:
        vqtd_bens_list = list(map(int, vqtd_bens.split(";")))
        for sociedade, valor in zip(sociedades.values(), vqtd_bens_list):
            sociedade["bens"].append(valor)
        vdif_bens_list = list(map(int, vdif_bens.split(";")))
        for sociedade, valor in zip(sociedades.values(), vdif_bens_list):
            sociedade["dificuldade"].append(valor)
        vnec_bens_list = list(map(int, vnec_bens.split(";")))
        for sociedade, valor in zip(sociedades.values(), vnec_bens_list):
            sociedade["necessidade"].append(valor)

    # Fechar o frame de adição
    frame_add_bem.place_forget()

    atualizar_variavel_y_em_cpp(2)

    time.sleep(1)

    # Montar mensagem estruturada e enviar para o backend C++
    mensagem = (
        f"gname={nome_bem}|qtds={vqtd_bens}|"
        f"difcs={vdif_bens}|necs={vnec_bens}"
    )
    enviar_mensagem(mensagem)


# Função para atualizar a lista de bens no frame
def atualizar_lista_bens(sim_name):
    listbox_bens.delete(0, tk.END)  # Limpa a lista
    for bem in bens_por_simulacao.get(sim_name, []):
        listbox_bens.insert(tk.END, bem)

# Função para remover um bem selecionado
def remover_bem():
    try:
        selecionado = listbox_bens.get(listbox_bens.curselection())
        indice_selecionado = listbox_bens.curselection()[0]
        nome_bem = listbox_bens.get(indice_selecionado)

        for sociedade in sociedades.values():
            bens = sociedade["bens"] 
            del bens[indice_selecionado]
            necs = sociedade["necessidade"]
            del necs[indice_selecionado]
            difs = sociedade["dificuldade"]
            del difs[indice_selecionado]

        sim_name = label_sim_name["text"].split(": ")[1]

        # Remove o bem da lista correspondente
        bens_por_simulacao[sim_name].remove(selecionado)

        # Atualizar a exibição da lista de bens
        atualizar_lista_bens(sim_name)

        atualizar_variavel_y_em_cpp(4)

        time.sleep(1)

        # Montar mensagem estruturada e enviar para o backend C++
        mensagem = (
            f"gnametormv={nome_bem}"
        )
        enviar_mensagem(mensagem)

    except (IndexError, KeyError):
        messagebox.showwarning("Erro", "Selecione um bem para remover!")

# Função para exibir o frame "Lista de Bens"
def abrir_lista_bens():
    frame_lista_bens.place(x=170, y=450, width=300, height=325)  # Posiciona o frame abaixo de "Simulação Detalhes"
    sim_name = label_sim_name["text"].split(": ")[1]  # Obtém o nome da simulação atual
    atualizar_lista_bens(sim_name)  # Atualiza a exibição dos bens no frame

# Função para fechar o frame "Lista de Bens"
def fechar_lista_bens():
    frame_lista_bens.place_forget()  # Esconde o frame


def construtor():
    nome_bem = "Pão"

    # Obter a simulação atual
    sim_name = label_sim_name["text"].split(": ")[1]

    # Adicionar o bem à lista correspondente
    if sim_name not in bens_por_simulacao:
        bens_por_simulacao[sim_name] = []
    bens_por_simulacao[sim_name].append(nome_bem)

    # Atualizar a exibição da lista de bens
    atualizar_lista_bens(sim_name)

    nome = "Ferreira"
    qtd_moeda = 100
    moeda = "Kwanza"
    bens = "12"
    dificuldade = "7"
    necessidade = "5"

    if not nome or not qtd_moeda or not moeda or not bens or not dificuldade or not necessidade:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    # Converte os bens para uma lista de inteiros
    bens_list = list(map(int, bens.split(";")))
    dificuldade_list = list(map(int, dificuldade.split(";")))
    necessidade_list = list(map(int, necessidade.split(";")))

    # Salvar sociedade no dicionário
    sociedades[nome] = {
        "quantidade_inicial": qtd_moeda,
        "moeda": moeda,
        "bens": bens_list,
        "dificuldade": dificuldade_list,
        "necessidade": necessidade_list,
    }

    # Adicionar nome à lista de sociedades
    listbox_sociedades.insert(tk.END, nome)
    listbox_moedas.insert(tk.END, moeda)

    nome = "Rabelo"
    qtd_moeda = 150
    moeda = "USD"
    bens = "7"
    dificuldade = "4"
    necessidade = "1"

    if not nome or not qtd_moeda or not moeda or not bens or not dificuldade or not necessidade:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    # Converte os bens para uma lista de inteiros
    bens_list = list(map(int, bens.split(";")))
    dificuldade_list = list(map(int, dificuldade.split(";")))
    necessidade_list = list(map(int, necessidade.split(";")))

    # Salvar sociedade no dicionário
    sociedades[nome] = {
        "quantidade_inicial": qtd_moeda,
        "moeda": moeda,
        "bens": bens_list,
        "dificuldade": dificuldade_list,
        "necessidade": necessidade_list,
    }

    # Adicionar nome à lista de sociedades
    listbox_sociedades.insert(tk.END, nome)
    listbox_moedas.insert(tk.END, moeda)


# Configurações principais
root = tk.Tk()
root.title("E-Barter")
root.geometry("800x600")
root.configure(bg="#E3E9F2")
simulations = []

# Estilo global
font_title = ("Arial", 16, "bold")
font_text = ("Arial", 12)
bg_color = "#F7F9FC"
button_color = "#D9E3F0"
button_active_color = "#C3D4E6"

# Título principal
title_label = tk.Label(root, text="E-Barter", font=("Arial", 20, "bold"), bg="#305496", fg="white")
title_label.pack(fill="x", pady=5)

# Frame principal - Menu
frame_menu = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
frame_menu.pack(side="left", fill="y", padx=5, pady=5)

# Botões do menu principal
btn_nova_sim = tk.Button(frame_menu, text="Nova Simulação", font=font_text, bg=button_color,
                         activebackground=button_active_color, command=nova_simulacao)
btn_nova_sim.pack(fill="x", pady=5)

btn_arquivadas = tk.Button(frame_menu, text="Sim. Arquivadas", font=font_text, bg=button_color,
                           activebackground=button_active_color, command=mostrar_arquivadas)
btn_arquivadas.pack(fill="x", pady=5)

btn_sair = tk.Button(frame_menu, text="Sair", font=font_text, bg=button_color,
                     activebackground=button_active_color, command=sair)
btn_sair.pack(fill="x", pady=5)

# Frame "Nova Simulação" (2ª janela)
frame_new_sim = tk.Frame(root, bg=bg_color, bd=2, relief="groove")

tk.Label(frame_new_sim, text="Nova Simulação", font=font_title, bg=bg_color).pack(pady=5)
tk.Label(frame_new_sim, text="Nome da Simulação", font=font_text, bg=bg_color).pack(pady=5)
sim_name_entry = tk.Entry(frame_new_sim, font=font_text)
sim_name_entry.pack(pady=5)

btn_criar_sim = tk.Button(frame_new_sim, text="Criar Simulação", font=font_text, bg=button_color,
                          activebackground=button_active_color, command=criar_simulacao)
btn_criar_sim.pack(pady=5)

btn_voltar_sim = tk.Button(frame_new_sim, text="Voltar", font=font_text, bg=button_color,
                           activebackground=button_active_color, command=lambda: frame_new_sim.place_forget())
btn_voltar_sim.pack(pady=5)

# Frame "Simulações Arquivadas"
frame_arquivadas = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_arquivadas, text="Simulações Arquivadas", font=font_title, bg=bg_color).pack(pady=5)
arquivadas_listbox = tk.Listbox(frame_arquivadas, font=font_text, bg="#FFFFFF", height=10)
arquivadas_listbox.pack(fill="both", expand=True, padx=10, pady=5)
arquivadas_listbox.bind("<<ListboxSelect>>", carregar_simulacao)

btn_voltar_arquivadas = tk.Button(frame_arquivadas, text="Voltar", font=font_text, bg=button_color,
                                  activebackground=button_active_color, command=lambda: frame_arquivadas.place_forget())
btn_voltar_arquivadas.pack(pady=5)

# Frame "Detalhes da Simulação" (3ª janela)
frame_sim_details = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
label_sim_name = tk.Label(frame_sim_details, text="Simulação: ", font=font_title, bg=bg_color)
label_sim_name.pack(pady=5)

btn_add_soc = tk.Button(frame_sim_details, text="Add Sociedade", font=font_text, bg=button_color,
                        activebackground=button_active_color)
btn_add_soc.pack(pady=5)

btn_simular = tk.Button(frame_sim_details, text="Simular", font=font_text, bg=button_color,
                        activebackground=button_active_color)
btn_simular.pack(pady=5)

btn_sair_sim = tk.Button(frame_sim_details, text="Sair", font=font_text, bg=button_color,
                         activebackground=button_active_color, command=sair_simulacao)
btn_sair_sim.pack(pady=5)

# Frame "Sociedades" (janela superior direita)
frame_sociedades = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
label_sociedades = tk.Label(frame_sociedades, text="Sociedades", font=font_title, bg=bg_color)
label_sociedades.pack(anchor="n", pady=5)
listbox_sociedades = tk.Listbox(frame_sociedades, font=font_text, bg="#FFFFFF", height=12)
listbox_sociedades.pack(fill="both", expand=True, padx=5, pady=5)

# Frame "Moedas" (janela inferior direita)
frame_moedas = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
label_moedas = tk.Label(frame_moedas, text="Moedas", font=font_title, bg=bg_color)
label_moedas.pack(anchor="n", pady=5)
listbox_moedas = tk.Listbox(frame_moedas, font=font_text, bg="#FFFFFF", height=12)
listbox_moedas.pack(fill="both", expand=True, padx=5, pady=5)

# Janela para adicionar nova sociedade
frame_add_soc = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_add_soc, text="Adicionar Sociedade", font=font_title, bg=bg_color).pack(pady=5)

# Configurações principais para a janela "Adicionar Sociedade"
tk.Label(frame_add_soc, text="Nome da Sociedade:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_nome_soc = tk.Entry(frame_add_soc, font=font_text)
entry_nome_soc.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Quantidade Inicial:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_qtd_moeda = tk.Entry(frame_add_soc, font=font_text)
entry_qtd_moeda.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Nome da Moeda:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_nome_moeda = tk.Entry(frame_add_soc, font=font_text)
entry_nome_moeda.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Quantidade de Bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_qtd_bens = tk.Entry(frame_add_soc, font=font_text)
entry_qtd_bens.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Dificuldade dos Bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_dific_bens = tk.Entry(frame_add_soc, font=font_text)
entry_dific_bens.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Necessidade dos Bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_necess_bens = tk.Entry(frame_add_soc, font=font_text)
entry_necess_bens.pack(fill="x", padx=10, pady=2)

btn_criar_soc = tk.Button(frame_add_soc, text="Criar", font=font_text, bg=button_color,
                          activebackground=button_active_color, command=criar_sociedade)
btn_criar_soc.pack(pady=10)

btn_voltar_add_soc = tk.Button(frame_add_soc, text="Voltar", font=font_text, bg=button_color,
                               activebackground=button_active_color, command=lambda: frame_add_soc.place_forget())
btn_voltar_add_soc.pack()

# Detalhes da sociedade selecionada
frame_detalhes_soc = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
label_nome_soc = tk.Label(frame_detalhes_soc, text="Sociedade:", font=font_title, bg=bg_color)
label_nome_soc.pack(pady=5)

label_moeda = tk.Label(frame_detalhes_soc, text="Nome da Moeda:", font=font_text, bg=bg_color)
label_moeda.pack(anchor="w", padx=10, pady=2)

label_bens = tk.Label(frame_detalhes_soc, text="Quantidade de Bens:", font=font_text, bg=bg_color)
label_bens.pack(anchor="w", padx=10, pady=2)

label_dificuldade = tk.Label(frame_detalhes_soc, text="Dificuldade dos Bens:", font=font_text, bg=bg_color)
label_dificuldade.pack(anchor="w", padx=10, pady=2)

label_necessidade = tk.Label(frame_detalhes_soc, text="Necessidade dos Bens:", font=font_text, bg=bg_color)
label_necessidade.pack(anchor="w", padx=10, pady=2)

btn_voltar_detalhes_soc = tk.Button(frame_detalhes_soc, text="Voltar", font=font_text, bg=button_color,
                                    activebackground=button_active_color, command=lambda: frame_detalhes_soc.place_forget())
btn_voltar_detalhes_soc.pack(pady=10)

# Atualizar o botão "Add Sociedade"
btn_add_soc.config(command=abrir_janela_sociedade)

# Adiciona o botão "Remover Sociedade" na interface principal
btn_remover_soc = tk.Button(frame_sim_details, text="Remover Sociedade", font=font_text, bg=button_color,
                            activebackground=button_active_color, command=remover_sociedade)
btn_remover_soc.pack(pady=5)

# Aumentar a largura do frame "Detalhes da Simulação"
frame_sim_details.configure(width=300)

# Ajustar o botão "Remover Sociedade" para ficar logo abaixo do botão "Add Sociedade"
btn_remover_soc.pack(after=btn_add_soc, pady=5)  # Posiciona logo abaixo do botão "Add Sociedade"

# Dicionário para armazenar bens associados a cada simulação
bens_por_simulacao = {}

# Frame "Adicionar Bem"
frame_add_bem = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_add_bem, text="Adicionar Bem", font=font_title, bg=bg_color).pack(pady=5)

tk.Label(frame_add_bem, text="Nome do bem:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_nome_bem = tk.Entry(frame_add_bem, font=font_text)
entry_nome_bem.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_bem, text="Vetor de qtd dos bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_vqtd_bens = tk.Entry(frame_add_bem, font=font_text)
entry_vqtd_bens.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_bem, text="Vetor de dif dos bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_vdif_bens = tk.Entry(frame_add_bem, font=font_text)
entry_vdif_bens.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_bem, text="Vetor de nec dos bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_vnec_bens = tk.Entry(frame_add_bem, font=font_text)
entry_vnec_bens.pack(fill="x", padx=10, pady=2)

btn_confirmar_bem = tk.Button(frame_add_bem, text="Adicionar", font=font_text, bg=button_color,
                              activebackground=button_active_color, command=adicionar_bem)
btn_confirmar_bem.pack(pady=5)

btn_cancelar_bem = tk.Button(frame_add_bem, text="Cancelar", font=font_text, bg=button_color,
                             activebackground=button_active_color, command=lambda: frame_add_bem.place_forget())
btn_cancelar_bem.pack(pady=5)

# Janela para adicionar simular
frame_simular = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_add_soc, text="Simular", font=font_title, bg=bg_color).pack(pady=5)

tk.Label(frame_add_soc, text="Quantidade de transações:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_qtd_transa = tk.Entry(frame_simular, font=font_text)
entry_qtd_transa.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Moeda a ser analisada:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_analise = tk.Entry(frame_simular, font=font_text)
entry_analise.pack(fill="x", padx=10, pady=2)

#btn_rodar_simu = tk.Button(frame_simular, text="Analisar", font=font_text, bg=button_color,
#                          activebackground=button_active_color, command=analisar)
#btn_rodar_simu.pack(pady=10)

btn_voltar_simu = tk.Button(frame_add_soc, text="Voltar", font=font_text, bg=button_color,
                               activebackground=button_active_color, command=lambda: frame_simular.place_forget())
btn_voltar_simu.pack()

# Atualizar o botão "simular"
btn_simular.config(command=abrir_janela_simular)

# Frame "Lista de Bens"
frame_lista_bens = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_lista_bens, text="Lista de Bens", font=font_title, bg=bg_color).pack(anchor="n", pady=5)

listbox_bens = tk.Listbox(frame_lista_bens, font=font_text, bg="#FFFFFF", height=10)
listbox_bens.pack(fill="both", expand=True, padx=10, pady=5)

btn_remover_bem = tk.Button(frame_lista_bens, text="Remover Bem", font=font_text, bg=button_color,
                            activebackground=button_active_color, command=remover_bem)
btn_remover_bem.pack(pady=5)

btn_fechar_lista = tk.Button(frame_lista_bens, text="Fechar", font=font_text, bg=button_color,
                             activebackground=button_active_color, command=fechar_lista_bens)
btn_fechar_lista.pack(pady=5)

# Botão para abrir a lista de bens na janela de detalhes
btn_abrir_lista_bens = tk.Button(frame_sim_details, text="Lista de Bens", font=font_text, bg=button_color,
                                 activebackground=button_active_color, command=abrir_lista_bens)
btn_abrir_lista_bens.pack(pady=5)

# Botões na janela de detalhes da simulação
btn_add_bem = tk.Button(frame_sim_details, text="Add Bem", font=font_text, bg=button_color,
                        activebackground=button_active_color, command=abrir_janela_add_bem)
btn_add_bem.pack(pady=5)

# Configurar o evento de clique na lista de sociedades
listbox_sociedades.bind("<<ListboxSelect>>", exibir_detalhes_sociedade)

# Detalhes dos bens selecionados
frame_detalhes_bens = tk.Frame(root, bg=bg_color, bd=2, relief="groove")

label_quantidade_bens = tk.Label(frame_detalhes_bens, text="Quantidade:", font=font_title, bg=bg_color)
label_quantidade_bens.pack(pady=5)


btn_voltar_detalhes_bens = tk.Button(frame_detalhes_bens, text="Voltar", font=font_text, bg=button_color,
                                    activebackground=button_active_color, command=lambda: frame_detalhes_bens.place_forget())
btn_voltar_detalhes_bens.pack(pady=10)


# Configurar o evento de clique na lista de bens
listbox_bens.bind("<<ListboxSelect>>", exibir_detalhes_bens)


# Iniciar a interface
root.mainloop()