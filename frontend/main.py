import tkinter as tk
from tkinter import messagebox
from backend.simulator import ProcessadorSimples

COR_FUNDO = "#006400"
COR_TEXTO = "#FFD700"
COR_BOTAO_FUNDO = "#FFD700"
COR_BOTAO_TEXTO = "#006400"
COR_ENTRY_FUNDO = "#E0F8E0"
COR_DESTAQUE = "#32CD32"

class FrontendProcessador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Processador")
        self.root.configure(bg=COR_FUNDO)
        self.root.geometry("750x600")
        
        self.cpu = ProcessadorSimples()
        self.rodando = False
        
        self.criar_widgets()
        self.atualizar_interface()

    def criar_widgets(self):
        frame_cpu = tk.Frame(self.root, bg=COR_FUNDO, padx=20, pady=20)
        frame_cpu.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_cpu, text="CPU / CONTROLE", font=("Arial", 14, "bold"), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=(0, 20))

        frame_pc_ir = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_pc_ir.pack(fill=tk.X, pady=5)
        
        tk.Label(frame_pc_ir, text="PC:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="e")
        self.ent_pc = tk.Entry(frame_pc_ir, width=5, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
        self.ent_pc.grid(row=0, column=1, padx=5)

        tk.Label(frame_pc_ir, text="IR:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="e", pady=5)
        self.ent_ir = tk.Entry(frame_pc_ir, width=15, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
        self.ent_ir.grid(row=1, column=1, padx=5)

        frame_regs = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_regs.pack(fill=tk.X, pady=15)
        tk.Label(frame_regs, text="Registradores:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
        
        self.ent_regs = []
        for i in range(4):
            tk.Label(frame_regs, text=f"R{i}:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12)).grid(row=i+1, column=0, sticky="e")
            ent = tk.Entry(frame_regs, width=10, bg=COR_ENTRY_FUNDO, font=("Arial", 12))
            ent.grid(row=i+1, column=1, pady=2, padx=5)
            self.ent_regs.append(ent)

        frame_flags = tk.Frame(frame_cpu, bg=COR_FUNDO)
        frame_flags.pack(fill=tk.X, pady=10)
        tk.Label(frame_flags, text="Flags ALU:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)
        
        self.lbl_zero = tk.Label(frame_flags, text="ZERO: Falso", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10))
        self.lbl_zero.grid(row=1, column=0, padx=10)
        self.lbl_neg = tk.Label(frame_flags, text="NEG: Falso", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 10))
        self.lbl_neg.grid(row=1, column=1, padx=10)

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
        for i in range(32):
            val = self.ent_mems[i].get().strip()
            self.cpu.memoria[i] = val if val else "0"

    def atualizar_interface(self):
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
            self.ent_mems[i].config(bg=COR_ENTRY_FUNDO)
            
        if self.cpu.pc < 32 and self.cpu.executando:
            self.ent_mems[self.cpu.pc].config(bg=COR_DESTAQUE)

    def step(self):
        self.ler_memoria_da_interface()
        if self.cpu.executando and self.cpu.pc < 32:
            self.cpu.ciclo_instrucao() # Chama o seu backend!
            self.atualizar_interface()
            
            if not self.cpu.executando or self.cpu.pc >= 32:
                messagebox.showinfo("Fim", "Fim da execução do programa.")

    def run(self):
        self.ler_memoria_da_interface()
        self.rodando = True
        self.ciclo_run()

    def ciclo_run(self):
        if self.rodando and self.cpu.executando and self.cpu.pc < 32:
            self.cpu.ciclo_instrucao()
            self.atualizar_interface()
            self.root.after(200, self.ciclo_run)

    def stop(self):
        self.rodando = False

    def reset_cpu(self):
        self.stop()
        self.cpu = ProcessadorSimples()
        self.atualizar_interface()

    def limpar_memoria(self):
        self.stop()
        self.cpu = ProcessadorSimples()
        for ent in self.ent_mems:
            ent.delete(0, tk.END)
            ent.insert(0, "0")
        self.ler_memoria_da_interface()
        self.atualizar_interface()

if __name__ == "__main__":
    root = tk.Tk()
    app = FrontendProcessador(root)
    root.mainloop()