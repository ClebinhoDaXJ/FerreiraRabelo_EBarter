import tkinter as tk
from tkinter import messagebox

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
    frame_sim_details.place_forget()
    frame_sociedades.place_forget()  # Fechar a janela "Sociedades"
    frame_moedas.place_forget()      # Fechar a janela "Moedas"

# Função para abrir a janela "Adicionar Sociedade"
def abrir_janela_sociedade():
    frame_add_soc.place(x=220, y=150)  # Exibe a janela para adicionar sociedade
    for entry in [entry_nome_soc, entry_qtd_moeda, entry_lista_bens, entry_dific_bens, entry_necess_bens]:
        entry.delete(0, tk.END)  # Limpa os campos de entrada

# Função para criar uma nova sociedade
def criar_sociedade():
    nome = entry_nome_soc.get().strip()
    moeda = entry_qtd_moeda.get().strip()
    bens = entry_lista_bens.get().strip()
    dificuldade = entry_dific_bens.get().strip()
    necessidade = entry_necess_bens.get().strip()

    if not nome or not moeda or not bens or not dificuldade or not necessidade:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return

    # Salvar sociedade no dicionário
    sociedades[nome] = {
        "moeda": moeda,
        "bens": bens,
        "dificuldade": dificuldade,
        "necessidade": necessidade,
    }

    # Adicionar nome à lista de sociedades
    listbox_sociedades.insert(tk.END, nome)

    # Fechar a janela de criação
    frame_add_soc.place_forget()

# Função para exibir os detalhes da sociedade selecionada
def exibir_detalhes_sociedade(event):
    try:
        selecionada = listbox_sociedades.get(listbox_sociedades.curselection())
        detalhes = sociedades[selecionada]

        # Exibe janela de detalhes
        frame_detalhes_soc.place(x=1100, y=150)
        label_nome_soc.config(text=f"Sociedade: {selecionada}")
        label_moeda.config(text=f"Quantidade de Moeda: {detalhes['moeda']}")
        label_bens.config(text=f"Lista de Bens: {detalhes['bens']}")
        label_dificuldade.config(text=f"Dificuldade dos Bens: {detalhes['dificuldade']}")
        label_necessidade.config(text=f"Necessidade dos Bens: {detalhes['necessidade']}")
    except IndexError:
        pass

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

# Dicionário para armazenar sociedades
sociedades = {}

# Janela para adicionar nova sociedade
frame_add_soc = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
tk.Label(frame_add_soc, text="Adicionar Sociedade", font=font_title, bg=bg_color).pack(pady=5)

tk.Label(frame_add_soc, text="Nome da Sociedade:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_nome_soc = tk.Entry(frame_add_soc, font=font_text)
entry_nome_soc.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Quantidade de Moeda:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_qtd_moeda = tk.Entry(frame_add_soc, font=font_text)
entry_qtd_moeda.pack(fill="x", padx=10, pady=2)

tk.Label(frame_add_soc, text="Lista dos Bens:", font=font_text, bg=bg_color).pack(anchor="w", padx=10, pady=2)
entry_lista_bens = tk.Entry(frame_add_soc, font=font_text)
entry_lista_bens.pack(fill="x", padx=10, pady=2)

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

label_moeda = tk.Label(frame_detalhes_soc, text="Quantidade de Moeda:", font=font_text, bg=bg_color)
label_moeda.pack(anchor="w", padx=10, pady=2)

label_bens = tk.Label(frame_detalhes_soc, text="Lista de Bens:", font=font_text, bg=bg_color)
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

# Configurar o evento de clique na lista de sociedades
listbox_sociedades.bind("<<ListboxSelect>>", exibir_detalhes_sociedade)

# Iniciar a interface
root.mainloop()
