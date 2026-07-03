import tkinter as tk
from tkinter import messagebox

# --- CONFIGURAÇÃO DE CORES (Verde e Amarelo) ---
COR_FUNDO = "#006400"        # Verde Bandeira (DarkGreen)
COR_TEXTO = "#FFD700"        # Amarelo Ouro (Gold)
COR_BOTAO_FUNDO = "#FFD700"  # Fundo do botão amarelo
COR_BOTAO_TEXTO = "#006400"  # Texto do botão verde
COR_ENTRY_FUNDO = "#E0F8E0"  # Verde bem claro para as caixas de texto
COR_DESTAQUE = "#32CD32"     # Verde Limão para destaques

class ProcessadorInterface:
    def __init__(self):
        self.resetar()

    def resetar(self):
        self.memoria = ["0"] * 32
        self.regs = [0, 0, 0, 0]
        self.pc = 0
        self.ir = ""
        self.flag_zero = False
        self.flag_negativo = False
        self.halted = False

    def extrair_reg(self, reg_str):
        return int(reg_str.replace('R', ''))

    def step(self):
        if self.halted or self.pc >= 32:
            return False

        # FETCH
        self.ir = self.memoria[self.pc].strip()
        if not self.ir or self.ir == "0":
            return False

        self.pc += 1

        # DECODE & EXECUTE
        partes = self.ir.split()
        cmd = partes[0].upper()

        try:
            if cmd == "HALT":
                self.halted = True
                
            elif cmd == "LOAD":
                reg = self.extrair_reg(partes[1])
                end_mem = int(partes[2])
                self.regs[reg] = int(self.memoria[end_mem])
                
            elif cmd == "STORE":
                end_mem = int(partes[1])
                reg = self.extrair_reg(partes[2])
                self.memoria[end_mem] = str(self.regs[reg])
                
            elif cmd == "MOVE":
                reg_dest = self.extrair_reg(partes[1])
                reg_src = self.extrair_reg(partes[2])
                self.regs[reg_dest] = self.regs[reg_src]
                
            elif cmd in ["ADD", "SUB", "AND", "OR"]:
                reg_dest = self.extrair_reg(partes[1])
                r_src1 = self.regs[self.extrair_reg(partes[2])]
                r_src2 = self.regs[self.extrair_reg(partes[3])]
                
                if cmd == "ADD": resultado = r_src1 + r_src2
                elif cmd == "SUB": resultado = r_src1 - r_src2
                elif cmd == "AND": resultado = r_src1 & r_src2
                elif cmd == "OR": resultado = r_src1 | r_src2
                
                self.regs[reg_dest] = resultado
                self.flag_zero = (resultado == 0)
                self.flag_negativo = (resultado < 0)
                
            elif cmd == "BRANCH":
                self.pc = int(partes[1])
                
            elif cmd == "BZERO":
                if self.flag_zero: self.pc = int(partes[1])
                    
            elif cmd == "BNEG":
                if self.flag_negativo: self.pc = int(partes[1])
                
            return True
        except Exception as e:
            print(f"Erro de Execução: {e}")
            self.halted = True
            return False

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador K&S - Edição Verde e Amarelo")
        self.root.configure(bg=COR_FUNDO)
        self.root.geometry("750x600")
        
        self.cpu = ProcessadorInterface()
        self.rodando = False
        
        self.criar_widgets()
        self.atualizar_interface()

    def criar_widgets(self):
        # Frame da CPU (Esquerda)
        frame_cpu = tk.Frame(self.root, bg=COR_FUNDO, padx=20, pady=20)
        frame_cpu.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_cpu, text="CPU / CONTROLE", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))

        # PC e IR
        frame_pc_ir = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_pc_ir.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_pc_ir, text="PC:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="e")
        self.ent_pc = tk.Entry(frame_pc_ir, width=5, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
        self.ent_pc.grid(row=0, column=1, padx=5)

        tk.Label(frame_pc_ir, text="IR:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5)
        self.ent_ir = tk.Entry(frame_pc_ir, width=15, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
        self.ent_ir.grid(row=1, column=1, padx=5)

        # Registradores
        frame_regs = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_regs.pack(fill=tk.X, pady=15)
        tk.Label(frame_regs, text="Registradores:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
        
        self.ent_regs = []
        for i in range(4):
            tk.Label(frame_regs, text=f"R{i}:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12)).grid(row=i+1, column=0, sticky="e")
            ent = tk.Entry(frame_regs, width=10, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
            ent.grid(row=i+1, column=1, pady=2, padx=5)
            self.ent_regs.append(ent)

        # Flags da ALU
        frame_flags = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_flags.pack(fill=tk.X, pady=10)
        tk.Label(frame_flags, text="Flags ALU:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
        
        self.lbl_zero = tk.Label(frame_flags, text="ZERO: Falso", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10))
        self.lbl_zero.grid(row=1, column=0, padx=10)
        self.lbl_neg = tk.Label(frame_flags, text="NEG: Falso", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10))
        self.lbl_neg.grid(row=1, column=1, padx=10)

        # Botões de Controle
        frame_botoes = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_botoes.pack(fill=tk.X, pady=20)
        
        botoes = [
            ("Step (Passo)", self.step),
            ("Run (Rodar)", self.run),
            ("Stop (Parar)", self.stop),
            ("Reset CPU", self.reset_cpu),
            ("Limpar Memória", self.limpar_memoria)
        ]
        
        for texto, comando in botoes:
            btn = tk.Button(frame_botoes, text=texto, command=comando, bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_TEXTO, font=("Arial", 10, "bold"), width=15)
            btn.pack(pady=3)

        # Frame da Memória RAM (Direita)
        frame_mem = tk.Frame(self.root, bg=COR_FUNDO, padx=20, pady=20)
        frame_mem.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(frame_mem, text="MEMÓRIA RAM", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 10))

        # Grid da Memória (2 colunas de 16 para caber na tela)
        frame_mem_grid = tk.Frame(frame_mem, bg=COR_FUNDO)
        frame_mem_grid.pack()

        self.ent_mems = []
        for i in range(32):
            linha = i % 16
            coluna = (i // 16) * 2
            
            tk.Label(frame_mem_grid, text=f"{i:02d}:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Courier", 10)).grid(row=linha, column=coluna, sticky="e", padx=(10, 2))
            ent = tk.Entry(frame_mem_grid, width=12, bg=COR_ENTRY_FUNDO, font=("Courier", 10))
            ent.insert(0, "0")
            ent.grid(row=linha, column=coluna+1, pady=2)
            self.ent_mems.append(ent)

    def ler_memoria_da_interface(self):
        """Puxa o texto digitado nas caixas da interface para a lista de memória da CPU."""
        for i in range(32):
            val = self.ent_mems[i].get().strip()
            self.cpu.memoria[i] = val if val else "0"

    def atualizar_interface(self):
        """Atualiza a interface gráfica com os dados atuais da CPU."""
        self.ent_pc.delete(0, tk.END)
        self.ent_pc.insert(0, str(self.cpu.pc))
        
        self.ent_ir.delete(0, tk.END)
        self.ent_ir.insert(0, self.cpu.ir)

        for i in range(4):
            self.ent_regs[i].delete(0, tk.END)
            self.ent_regs[i].insert(0, str(self.cpu.regs[i]))

        self.lbl_zero.config(text=f"ZERO: {'Verdadeiro' if self.cpu.flag_zero else 'Falso'}")
        self.lbl_neg.config(text=f"NEG: {'Verdadeiro' if self.cpu.flag_negativo else 'Falso'}")

        for i in range(32):
            self.ent_mems[i].delete(0, tk.END)
            self.ent_mems[i].insert(0, self.cpu.memoria[i])
            self.ent_mems[i].config(bg=COR_ENTRY_FUNDO) # Reseta cor de fundo
            
        # Destaca a próxima instrução na memória
        if self.cpu.pc < 32 and not self.cpu.halted:
            self.ent_mems[self.cpu.pc].config(bg=COR_DESTAQUE)

    def step(self):
        self.ler_memoria_da_interface()
        if not self.cpu.halted:
            sucesso = self.cpu.step()
            self.atualizar_interface()
            if not sucesso and not self.cpu.halted:
                messagebox.showinfo("Fim", "Fim da execução do programa.")
                self.cpu.halted = True

    def run(self):
        self.ler_memoria_da_interface()
        self.rodando = True
        self.ciclo_run()

    def ciclo_run(self):
        """Executa instruções continuamente até parar ou dar HALT (evita travar a interface)."""
        if self.rodando and not self.cpu.halted:
            self.cpu.step()
            self.atualizar_interface()
            # Chama o próximo passo após 200 milissegundos (efeito visual do programa rodando)
            self.root.after(200, self.ciclo_run)

    def stop(self):
        self.rodando = False

    def reset_cpu(self):
        self.stop()
        self.cpu.resetar()
        self.atualizar_interface()

    def limpar_memoria(self):
        self.stop()
        self.cpu.resetar()
        for ent in self.ent_mems:
            ent.delete(0, tk.END)
            ent.insert(0, "0")
        self.ler_memoria_da_interface()
        self.atualizar_interface()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()