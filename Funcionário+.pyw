import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from collections import OrderedDict

class SistemaFuncionarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Funcionários")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.funcionarios = []
        self.arquivo_dados = "funcionarios.json"
        self.arquivo_idioma = "idioma_config.json"
        self.idioma_atual = "pt_BR"
        
        # Configuração de idiomas
        self.idiomas = {
            "pt_BR": {
                "titulo": "Gestão de Funcionários",
                "cadastrar": "Cadastrar Novo Funcionário",
                "nome": "Nome completo:",
                "salario": "Salário (R$):",
                "btn_cadastrar": "Cadastrar Funcionário",
                "ajustes": "Ajustes Salariais",
                "porcentagem": "Porcentagem (%):",
                "aumentar": "Aplicar Aumento",
                "diminuir": "Aplicar Redução",
                "remover": "Remover Selecionado",
                "lista": "Funcionários Cadastrados",
                "atualizar": "↻ Atualizar Lista",
                "salvar": "💾 Salvar Dados",
                "nenhum_funcionario": "Nenhum funcionário cadastrado",
                "sucesso_cadastro": "Funcionário {} cadastrado com sucesso!",
                "erro_valor": "Por favor, insira um valor numérico válido."
            },
            "en_US": {
                "titulo": "Employee Management",
                "cadastrar": "Register New Employee",
                "nome": "Full name:",
                "salario": "Salary ($):",
                "btn_cadastrar": "Register Employee",
                "ajustes": "Salary Adjustments",
                "porcentagem": "Percentage (%):",
                "aumentar": "Apply Increase",
                "diminuir": "Apply Decrease",
                "remover": "Remove Selected",
                "lista": "Registered Employees",
                "atualizar": "↻ Refresh List",
                "salvar": "💾 Save Data",
                "nenhum_funcionario": "No employees registered",
                "sucesso_cadastro": "Employee {} registered successfully!",
                "erro_valor": "Please enter a valid numeric value."
            },
            "es_ES": {
                "titulo": "Gestión de Empleados",
                "cadastrar": "Registrar Nuevo Empleado",
                "nome": "Nombre completo:",
                "salario": "Salario ($):",
                "btn_cadastrar": "Registrar Empleado",
                "ajustes": "Ajustes Salariales",
                "porcentagem": "Porcentaje (%):",
                "aumentar": "Aplicar Aumento",
                "diminuir": "Aplicar Reducción",
                "remover": "Eliminar Seleccionado",
                "lista": "Empleados Registrados",
                "atualizar": "↻ Actualizar Lista",
                "salvar": "💾 Guardar Datos",
                "nenhum_funcionario": "Ningún empleado registrado",
                "sucesso_cadastro": "¡Empleado {} registrado con éxito!",
                "erro_valor": "Por favor ingrese un valor numérico válido."
            }
        }

        # Verificar se é a primeira execução
        if not os.path.exists(self.arquivo_idioma):
            self.mostrar_seletor_idioma()
        else:
            self.carregar_idioma()
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 9), padding=6)
        self.style.configure('TEntry', padding=5)
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#333333')
        
        # Carregar dados
        self.carregar_dados()
        
        # Criar interface
        self.criar_interface()
        
        # Configurar salvamento ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)
    
    def mostrar_seletor_idioma(self):
        """Janela para seleção de idioma na primeira execução"""
        popup = tk.Toplevel(self.root)
        popup.title("Selecione o Idioma / Select Language / Seleccione Idioma")
        popup.geometry("350x250")
        popup.resizable(False, False)
        popup.grab_set()
        
        tk.Label(
            popup, 
            text="Por favor, selecione seu idioma\nPlease select your language\nPor favor seleccione su idioma",
            font=('Segoe UI', 10),
            pady=20
        ).pack()
        
        btn_pt = ttk.Button(
            popup,
            text="Português Brasileiro",
            command=lambda: self.definir_idioma("pt_BR")
        )
        btn_pt.pack(pady=5, fill=tk.X, padx=50)
        
        btn_en = ttk.Button(
            popup,
            text="English (US)",
            command=lambda: self.definir_idioma("en_US")
        )
        btn_en.pack(pady=5, fill=tk.X, padx=50)
        
        btn_es = ttk.Button(
            popup,
            text="Español (ES)",
            command=lambda: self.definir_idioma("es_ES")
        )
        btn_es.pack(pady=5, fill=tk.X, padx=50)
    
    def definir_idioma(self, codigo_idioma):
        """Define o idioma selecionado"""
        self.idioma_atual = codigo_idioma
        with open(self.arquivo_idioma, 'w') as f:
            json.dump({"idioma": codigo_idioma}, f)
        self.atualizar_interface()
    
    def carregar_idioma(self):
        """Carrega o idioma salvo"""
        try:
            with open(self.arquivo_idioma, 'r') as f:
                config = json.load(f)
                self.idioma_atual = config.get("idioma", "pt_BR")
        except:
            self.idioma_atual = "pt_BR"
    
    def atualizar_interface(self):
        """Atualiza todos os textos da interface"""
        textos = self.idiomas.get(self.idioma_atual, self.idiomas["pt_BR"])
        
        self.root.title(textos["titulo"])
        self.header.config(text=textos["titulo"])
        self.form_frame.config(text=f" {textos['cadastrar']} ")
        self.ajuste_frame.config(text=f" {textos['ajustes']} ")
        self.lista_frame.config(text=f" {textos['lista']} ")
        
        # Atualizar labels
        self.label_nome.config(text=textos["nome"])
        self.label_salario.config(text=textos["salario"])
        self.label_porcentagem.config(text=textos["porcentagem"])
        
        # Atualizar botões
        self.btn_adicionar.config(text=textos["btn_cadastrar"])
        self.btn_aumentar.config(text=textos["aumentar"])
        self.btn_diminuir.config(text=textos["diminuir"])
        self.btn_remover.config(text=textos["remover"])
        self.btn_atualizar.config(text=textos["atualizar"])
        self.btn_salvar.config(text=textos["salvar"])
        
        # Atualizar lista
        self.listar_funcionarios()
    
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        # Container principal
        self.main_container = ttk.Frame(self.root, padding=(20, 15))
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        self.header = ttk.Label(
            self.main_container, 
            text=self.t("titulo"),
            style='Header.TLabel'
        )
        self.header.pack(pady=(0, 15))
        
        # Formulário de cadastro
        self.form_frame = ttk.LabelFrame(
            self.main_container,
            text=f" {self.t('cadastrar')} ",
            padding=(15, 10)
        )
        self.form_frame.pack(fill=tk.X, pady=5)
        
        # Campos do formulário
        self.label_nome = ttk.Label(self.form_frame, text=self.t("nome"))
        self.label_nome.grid(row=0, column=0, sticky='w', pady=3)
        
        self.entry_nome = ttk.Entry(self.form_frame, width=40)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=3)
        
        self.label_salario = ttk.Label(self.form_frame, text=self.t("salario"))
        self.label_salario.grid(row=1, column=0, sticky='w', pady=3)
        
        self.entry_salario = ttk.Entry(self.form_frame, width=40)
        self.entry_salario.grid(row=1, column=1, padx=5, pady=3)
        
        self.btn_adicionar = ttk.Button(
            self.form_frame,
            text=self.t("btn_cadastrar"),
            command=self.adicionar_funcionario
        )
        self.btn_adicionar.grid(row=2, column=1, pady=10, sticky='e')
        
        # Painel de ajustes
        self.ajuste_frame = ttk.LabelFrame(
            self.main_container,
            text=f" {self.t('ajustes')} ",
            padding=(15, 10)
        )
        self.ajuste_frame.pack(fill=tk.X, pady=5)
        
        self.label_porcentagem = ttk.Label(self.ajuste_frame, text=self.t("porcentagem"))
        self.label_porcentagem.grid(row=0, column=0, sticky='w', pady=3)
        
        self.entry_porcentagem = ttk.Entry(self.ajuste_frame, width=10)
        self.entry_porcentagem.grid(row=0, column=1, padx=5, pady=3, sticky='w')
        
        self.btn_container = ttk.Frame(self.ajuste_frame)
        self.btn_container.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.btn_aumentar = ttk.Button(
            self.btn_container,
            text=self.t("aumentar"),
            command=self.aumentar_salario,
            style='TButton'
        )
        self.btn_aumentar.pack(side=tk.LEFT, padx=5)
        
        self.btn_diminuir = ttk.Button(
            self.btn_container,
            text=self.t("diminuir"),
            command=self.diminuir_salario
        )
        self.btn_diminuir.pack(side=tk.LEFT, padx=5)
        
        self.btn_remover = ttk.Button(
            self.btn_container,
            text=self.t("remover"),
            command=self.remover_funcionario
        )
        self.btn_remover.pack(side=tk.LEFT, padx=5)
        
        # Lista de funcionários
        self.lista_frame = ttk.LabelFrame(
            self.main_container,
            text=f" {self.t('lista')} ",
            padding=(15, 10)
        )
        self.lista_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.lista_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.listbox = tk.Listbox(
            self.lista_frame,
            yscrollcommand=self.scrollbar.set,
            selectbackground='#4a98f7',
            selectforeground='white',
            activestyle='none',
            font=('Segoe UI', 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#cccccc',
            highlightbackground='#cccccc'
        )
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        
        # Rodapé
        self.footer = ttk.Frame(self.main_container)
        self.footer.pack(fill=tk.X, pady=(10, 0))
        
        self.btn_atualizar = ttk.Button(
            self.footer,
            text=self.t("atualizar"),
            command=self.listar_funcionarios
        )
        self.btn_atualizar.pack(side=tk.LEFT, padx=5)
        
        self.btn_salvar = ttk.Button(
            self.footer,
            text=self.t("salvar"),
            command=self.salvar_dados
        )
        self.btn_salvar.pack(side=tk.RIGHT, padx=5)
        
        # Carregar lista inicial
        self.listar_funcionarios()
    
    def t(self, chave):
        """Retorna o texto traduzido"""
        return self.idiomas[self.idioma_atual].get(chave, chave)
    
    # Métodos de funcionalidade
    def adicionar_funcionario(self):
        nome = self.entry_nome.get().strip()
        salario = self.entry_salario.get().strip()
        
        if not nome or not salario:
            messagebox.showwarning(self.t("titulo"), self.t("erro_valor"))
            return
        
        try:
            salario = float(salario)
            if salario <= 0:
                messagebox.showwarning(self.t("titulo"), self.t("erro_valor"))
                return
                
            self.funcionarios.append({"nome": nome, "salario": salario})
            messagebox.showinfo(
                self.t("titulo"),
                self.t("sucesso_cadastro").format(nome)
            )
            self.entry_nome.delete(0, tk.END)
            self.entry_salario.delete(0, tk.END)
            self.listar_funcionarios()
            self.salvar_dados()
        except ValueError:
            messagebox.showerror(self.t("titulo"), self.t("erro_valor"))
    
    def aplicar_ajuste(self, aumento=True):
        if not self.funcionarios:
            messagebox.showwarning(self.t("titulo"), self.t("nenhum_funcionario"))
            return
        
        porcentagem = self.entry_porcentagem.get().strip()
        
        if not porcentagem:
            messagebox.showwarning(self.t("titulo"), self.t("erro_valor"))
            return
        
        try:
            porcentagem = float(porcentagem)
            if porcentagem <= 0:
                messagebox.showwarning(self.t("titulo"), self.t("erro_valor"))
                return
            
            selected = self.listbox.curselection()
            if not selected:
                messagebox.showwarning(self.t("titulo"), "Selecione um funcionário")
                return
            
            index = selected[0]
            funcionario = self.funcionarios[index]
            
            if aumento:
                novo_salario = funcionario["salario"] * (1 + porcentagem/100)
                msg = f"Aumento de {porcentagem}% aplicado.\nNovo salário: {self.formatar_moeda(novo_salario)}"
            else:
                novo_salario = funcionario["salario"] * (1 - porcentagem/100)
                msg = f"Redução de {porcentagem}% aplicada.\nNovo salário: {self.formatar_moeda(novo_salario)}"
            
            funcionario["salario"] = novo_salario
            messagebox.showinfo(self.t("titulo"), msg)
            self.listar_funcionarios()
            self.salvar_dados()
        except ValueError:
            messagebox.showerror(self.t("titulo"), self.t("erro_valor"))
    
    def formatar_moeda(self, valor):
        """Formata o valor conforme o idioma selecionado"""
        if self.idioma_atual == "en_US":
            return f"${valor:.2f}"
        elif self.idioma_atual == "es_ES":
            return f"${valor:.2f}"
        else:  # pt_BR e padrão
            return f"R$ {valor:.2f}"
    
    def aumentar_salario(self):
        self.aplicar_ajuste(aumento=True)
    
    def diminuir_salario(self):
        self.aplicar_ajuste(aumento=False)
    
    def remover_funcionario(self):
        if not self.funcionarios:
            messagebox.showwarning(self.t("titulo"), self.t("nenhum_funcionario"))
            return
        
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning(self.t("titulo"), "Selecione um funcionário")
            return
        
        index = selected[0]
        funcionario = self.funcionarios[index]
        
        confirmacao = messagebox.askyesno(
            "Confirmar Remoção", 
            f"Tem certeza que deseja remover?\n\n{funcionario['nome']} - {self.formatar_moeda(funcionario['salario'])}"
        )
        
        if confirmacao:
            self.funcionarios.pop(index)
            messagebox.showinfo(self.t("titulo"), "Funcionário removido")
            self.listar_funcionarios()
            self.salvar_dados()
    
    def listar_funcionarios(self):
        self.listbox.delete(0, tk.END)
        if not self.funcionarios:
            self.listbox.insert(tk.END, self.t("nenhum_funcionario"))
            return
            
        for func in sorted(self.funcionarios, key=lambda x: x['nome']):
            self.listbox.insert(tk.END, f"{func['nome']} - {self.formatar_moeda(func['salario'])}")
    
    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r') as f:
                    self.funcionarios = json.load(f)
            except:
                self.funcionarios = []
    
    def salvar_dados(self):
        try:
            with open(self.arquivo_dados, 'w') as f:
                json.dump(self.funcionarios, f, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
    
    def ao_fechar(self):
        self.salvar_dados()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaFuncionarios(root)
    root.mainloop()