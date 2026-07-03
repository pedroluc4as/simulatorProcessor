import os

class ProcessadorSimples:
    def __init__(self):
        self.memoria = ["0"] * 32  
        self.regs = [0, 0, 0, 0]   
        self.pc = 0                
        self.ir = ""               
        
        self.flag_zero = False
        self.flag_negativo = False
        
        self.executando = True

    def carregar_programa(self, arquivo_entrada):
        try:
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    if i < 32: 
                        self.memoria[i] = linha.strip()
            print(f"Programa '{arquivo_entrada}' carregado na memória com sucesso.")
        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
            self.executando = False

    def atualizar_flags(self, resultado):
        self.flag_zero = (resultado == 0)
        self.flag_negativo = (resultado < 0)

    def extrair_reg(self, reg_str):
        return int(reg_str.replace('R', ''))

    def ciclo_instrucao(self):
        if self.executando and self.pc < 32:
            self.ir = self.memoria[self.pc]
            
            if not self.ir or self.ir == "0":
                self.executando = False
                return
                
            self.pc += 1
            
            partes = self.ir.split()
            cmd = partes[0]
            
            try:
                if cmd == "HALT":
                    self.executando = False
                    
                elif cmd == "NOP":
                    pass 

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
                    
                elif cmd == "ADD":
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 + r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "SUB":
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 - r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "AND":
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 & r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "OR":
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 | r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "BRANCH":
                    self.pc = int(partes[1])
                    
                elif cmd == "BZERO":
                    if self.flag_zero:
                        self.pc = int(partes[1])
                        
                elif cmd == "BNEG":
                    if self.flag_negativo:
                        self.pc = int(partes[1])
            except Exception as e:
                print(f"Erro ao executar a instrução '{self.ir}' na linha {self.pc-1}: {e}")
                self.executando = False

    def gerar_arquivos_saida(self):
        with open("unidade_controle.txt", "w") as f:
            f.write(f"{self.pc}\n")
            f.write(f"{self.ir}\n")
            
        with open("banco_registradores.txt", "w") as f:
            for reg in self.regs:
                f.write(f"{reg}\n")
                
        with open("memoria_ram.txt", "w") as f:
            for item in self.memoria:
                f.write(f"{item}\n")
                
        print("Execução finalizada. Arquivos de saída gerados com sucesso!")

if __name__ == "__main__":
    simulador = ProcessadorSimples()
    
    simulador.carregar_programa("entrada.txt")
    
    if simulador.executando:
        simulador.ciclo_instrucao()
        simulador.gerar_arquivos_saida()