import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import time
import requests

def formatar_cnpj(event=None):
    cnpj = entry_cnpj.get().replace('.', '').replace('/', '').replace('-', '')
    if cnpj == '':
        entry_cnpj.delete(0, tk.END)
    else:
        cnpj_formatado = ''
        for i, digito in enumerate(cnpj):
            if i == 2 or i == 5:
                cnpj_formatado += f'.{digito}'
            elif i == 8:
                cnpj_formatado += f'/{digito}'
            elif i == 12:
                cnpj_formatado += f'-{digito}'
            else:
                cnpj_formatado += digito
        entry_cnpj.delete(0, tk.END)
        entry_cnpj.insert(0, cnpj_formatado)

def consultar_cnpj():
    entry_situacao.delete(0, tk.END)
    entry_tipo.delete(0, tk.END)
    entry_razao_social.delete(0, tk.END)
    entry_nome_fantasia.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_municipio.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_natureza_juridica.delete(0, tk.END)
    entry_atividade_principal.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

    cnpj = entry_cnpj.get()
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    if len(cnpj) != 14 or not cnpj.isdigit():
        messagebox.showerror('Erro', 'Por favor, insira um CNPJ válido.')
        return
    
    url = f'http://127.0.0.1:8080/consulta_cnpj?cnpj={cnpj}'
    response = requests.get(url)
    
    if response.status_code == 200:
        global empresa
        empresa = response.json()
        preencher_campos(empresa)
    else:
        messagebox.showerror('Erro', 'Falha ao consultar CNPJ na Receita Federal.')

def preencher_campos(empresa):
    entry_situacao.delete(0, tk.END)
    entry_situacao.insert(0, empresa['Situacao'])
    
    entry_tipo.delete(0, tk.END)
    entry_tipo.insert(0, empresa['Tipo'])
    
    entry_razao_social.delete(0, tk.END)
    entry_razao_social.insert(0, empresa['Razao Social'])
    
    entry_nome_fantasia.delete(0, tk.END)
    entry_nome_fantasia.insert(0, empresa['Nome Fantasia'])
    
    entry_estado.delete(0, tk.END)
    entry_estado.insert(0, empresa['Estado'])
    
    entry_municipio.delete(0, tk.END)
    entry_municipio.insert(0, empresa['Municipio'])
    
    entry_endereco.delete(0, tk.END)
    entry_endereco.insert(0, empresa['Endereco'])
    
    entry_natureza_juridica.delete(0, tk.END)
    entry_natureza_juridica.insert(0, empresa['Natureza Juridica'])
    
    entry_atividade_principal.delete(0, tk.END)
    entry_atividade_principal.insert(0, empresa['Atividade Principal'])
    
    entry_telefone.delete(0, tk.END)
    entry_telefone.insert(0, empresa['Telefone'])

def cadastrar_empresa():

    if not entry_situacao.get():
        messagebox.showerror('Erro', 'Consulte um CNPJ antes de cadastrar.')
        return
    
    cnpj = entry_cnpj.get()
    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes WHERE CNPJ = ?", (cnpj,))
    result = cursor.fetchone()
    if result:
        messagebox.showerror('Erro', 'Empresa já cadastrada.')
        conn.close()
        return
    
    empresa_info = (
        empresa['CNPJ'],
        empresa['Situacao'],
        empresa['Tipo'],
        empresa['Razao Social'],
        empresa['Nome Fantasia'],
        empresa['Estado'],
        empresa['Municipio'],
        empresa['Endereco'],
        empresa['Natureza Juridica'],
        empresa['Atividade Principal'],
        empresa['Telefone'],
        entry_num_funcionarios.get(),
        entry_faturamento_anual.get(),
        entry_vendedor_responsavel.get()
    )
    try:
        cursor.execute("INSERT INTO Clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", empresa_info)
        conn.commit()
        messagebox.showinfo('Sucesso', 'Empresa cadastrada com sucesso.')
    except sqlite3.IntegrityError:
        messagebox.showerror('Erro', 'O CNPJ já está cadastrado no banco de dados.')
    finally:
        conn.close()

def atualizar_informacoes():
    cnpj = entry_cnpj.get()
    if not cnpj:
        messagebox.showerror('Erro', 'Consulte um CNPJ antes de atualizar as informações.')
        return

    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()

    num_funcionarios = entry_num_funcionarios.get()
    faturamento_anual = entry_faturamento_anual.get()
    vendedor_responsavel = entry_vendedor_responsavel.get()

    if not (num_funcionarios or faturamento_anual or vendedor_responsavel):
        messagebox.showerror('Erro', 'Preencha pelo menos um dos três últimos campos para atualização.')
        return

    if num_funcionarios:
        cursor.execute("UPDATE Clientes SET NumeroFuncionarios = ? WHERE CNPJ = ?", (num_funcionarios, cnpj))

    if faturamento_anual:
        cursor.execute("UPDATE Clientes SET FaturamentoAnualEstimado = ? WHERE CNPJ = ?", (faturamento_anual, cnpj))

    if vendedor_responsavel:
        cursor.execute("UPDATE Clientes SET VendedorResponsavel = ? WHERE CNPJ = ?", (vendedor_responsavel, cnpj))

    conn.commit()
    conn.close()
    messagebox.showinfo('Sucesso', 'Informações atualizadas com sucesso.')

def consultar_clientes():

    clientes_window = tk.Toplevel(root)
    clientes_window.title('Clientes')

    canvas = tk.Canvas(clientes_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    y_scrollbar = tk.Scrollbar(clientes_window, orient=tk.VERTICAL, command=canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = tk.Scrollbar(clientes_window, orient=tk.HORIZONTAL, command=canvas.xview)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.configure(xscrollcommand=x_scrollbar.set)

    clientes_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=clientes_frame, anchor=tk.NW)

    conn = sqlite3.connect('empresas.db')
    cursor = conn.cursor()

    if entry_vendedor_responsavel.get():
        cursor.execute("SELECT * FROM Clientes WHERE VendedorResponsavel LIKE ?", ('%' + entry_vendedor_responsavel.get() + '%',))
    else:
        cursor.execute("SELECT * FROM Clientes")

    clientes = cursor.fetchall()

    headers = ["CNPJ", "Situação", "Tipo", "Razão Social", "Nome Fantasia", "Estado", "Município", "Endereço", "Natureza Jurídica", "Atividade Principal", "Telefone", "Número de Funcionários", "Faturamento Anual Estimado", "Vendedor Responsável"]
    for i, header in enumerate(headers):
        lbl = tk.Label(clientes_frame, text=header, bg='lightgrey', relief=tk.RIDGE)
        lbl.grid(row=0, column=i, sticky='ew')

    for i, cliente in enumerate(clientes):
        for j, valor in enumerate(cliente):
            lbl = tk.Label(clientes_frame, text=valor, padx=5, pady=2)
            lbl.grid(row=i+1, column=j, sticky='nsew')

    clientes_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    conn.close()

root = tk.Tk()
root.title('Cadastro de Empresa')

label_cnpj = tk.Label(root, text='*CNPJ:')
label_cnpj.grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_cnpj = tk.Entry(root)
entry_cnpj.grid(row=0, column=1, padx=5, pady=5)
entry_cnpj.bind('<KeyRelease>', formatar_cnpj)
entry_cnpj.bind('<Control-v>', formatar_cnpj)

label_situacao = tk.Label(root, text='Situação:')
label_situacao.grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_situacao = tk.Entry(root)
entry_situacao.grid(row=1, column=1, padx=5, pady=5)

label_tipo = tk.Label(root, text='Tipo:')
label_tipo.grid(row=2, column=0, padx=5, pady=5, sticky='w')
entry_tipo = tk.Entry(root)
entry_tipo.grid(row=2, column=1, padx=5, pady=5)
label_razao_social = tk.Label(root, text='Razão Social:')
label_razao_social.grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_razao_social = tk.Entry(root)
entry_razao_social.grid(row=3, column=1, padx=5, pady=5)

label_nome_fantasia = tk.Label(root, text='Nome Fantasia:')
label_nome_fantasia.grid(row=4, column=0, padx=5, pady=5, sticky='w')
entry_nome_fantasia = tk.Entry(root)
entry_nome_fantasia.grid(row=4, column=1, padx=5, pady=5)

label_estado = tk.Label(root, text='Estado:')
label_estado.grid(row=5, column=0, padx=5, pady=5, sticky='w')
entry_estado = tk.Entry(root)
entry_estado.grid(row=5,column=1, padx=5, pady=5)

label_municipio = tk.Label(root, text='Município:')
label_municipio.grid(row=6, column=0, padx=5, pady=5, sticky='w')
entry_municipio = tk.Entry(root)
entry_municipio.grid(row=6, column=1, padx=5, pady=5)

label_endereco = tk.Label(root, text='Endereço:')
label_endereco.grid(row=7, column=0, padx=5, pady=5, sticky='w')
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=7, column=1, padx=5, pady=5)

label_natureza_juridica = tk.Label(root, text='Natureza Jurídica:')
label_natureza_juridica.grid(row=8, column=0, padx=5, pady=5, sticky='w')
entry_natureza_juridica = tk.Entry(root)
entry_natureza_juridica.grid(row=8, column=1, padx=5, pady=5)

label_atividade_principal = tk.Label(root, text='Atividade Principal:')
label_atividade_principal.grid(row=9, column=0, padx=5, pady=5, sticky='w')
entry_atividade_principal = tk.Entry(root)
entry_atividade_principal.grid(row=9, column=1, padx=5, pady=5)

label_telefone = tk.Label(root, text='Telefone:')
label_telefone.grid(row=10, column=0, padx=5, pady=5, sticky='w')
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=10, column=1, padx=5, pady=5)

label_num_funcionarios = tk.Label(root, text='Número de Funcionários:')
label_num_funcionarios.grid(row=11, column=0, padx=5, pady=5, sticky='w')
entry_num_funcionarios = tk.Entry(root)
entry_num_funcionarios.grid(row=11, column=1, padx=5, pady=5)

label_faturamento_anual = tk.Label(root, text='Faturamento Anual Estimado:')
label_faturamento_anual.grid(row=12, column=0, padx=5, pady=5, sticky='w')
entry_faturamento_anual = tk.Entry(root)
entry_faturamento_anual.grid(row=12, column=1, padx=5, pady=5)

label_vendedor_responsavel = tk.Label(root, text='Vendedor Responsável:')
label_vendedor_responsavel.grid(row=13, column=0, padx=5, pady=5, sticky='w')
entry_vendedor_responsavel = tk.Entry(root)
entry_vendedor_responsavel.grid(row=13, column=1, padx=5, pady=5)

button_cadastrar = tk.Button(root, text='Cadastrar Empresa', command=cadastrar_empresa)
button_cadastrar.grid(row=15, column=0, padx=(10, 10), pady=5)

button_atualizar = tk.Button(root, text='Atualizar Informações', command=atualizar_informacoes)
button_atualizar.grid(row=15, column=1, padx=(15, 10), pady=5)

button_consultar = tk.Button(root, text='Consultar CNPJ', command=consultar_cnpj)
button_consultar.grid(row=15, column=2, padx=(10, 10), pady=5)

button_consultar_clientes = tk.Button(root, text='Consultar Clientes', command=consultar_clientes)
button_consultar_clientes.grid(row=15, column=3, padx=(10, 10), pady=5)

api_process = subprocess.Popen(['python', 'api.py'])

time.sleep(3)

root.mainloop()

api_process.wait()
