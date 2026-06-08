import os

class ProcessadorSimples:
    def __init__(self):
        # Inicializando os componentes de hardware
        self.memoria = ["0"] * 32  # Memória principal com 32 posições
        self.regs = [0, 0, 0, 0]   # Banco de registradores: R0, R1, R2, R3
        self.pc = 0                # Program Counter
        self.ir = ""               # Instruction Register
        
        # Flags da ALU
        self.flag_zero = False
        self.flag_negativo = False
        
        self.executando = True

    def carregar_programa(self, arquivo_entrada):
        """Lê o arquivo entrada.txt e carrega na memória RAM."""
        try:
            with open(arquivo_entrada, 'r') as f:
                linhas = f.readlines()
                for i, linha in enumerate(linhas):
                    if i < 32: # Máximo de 32 linhas conforme especificação
                        self.memoria[i] = linha.strip()
            print(f"Programa '{arquivo_entrada}' carregado na memória com sucesso.")
        except FileNotFoundError:
            print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
            self.executando = False

    def atualizar_flags(self, resultado):
        """Atualiza as flags da ALU após operações aritméticas/lógicas."""
        self.flag_zero = (resultado == 0)
        self.flag_negativo = (resultado < 0)

    def extrair_reg(self, reg_str):
        """Converte a string 'R0', 'R1', etc. para o índice inteiro 0, 1..."""
        return int(reg_str.replace('R', ''))

    def ciclo_instrucao(self):
        """Ciclo principal: Busca (Fetch), Decodifica (Decode) e Executa (Execute)."""
        while self.executando and self.pc < 32:
            # 1. FETCH (Busca)
            self.ir = self.memoria[self.pc]
            
            # Se a memória estiver vazia ou com "0" e não for uma instrução válida, encerra
            if not self.ir or self.ir == "0":
                break
                
            self.pc += 1 # Incrementa o PC para apontar para a próxima instrução
            
            # 2. DECODE (Decodifica)
            partes = self.ir.split()
            cmd = partes[0]
            
            # 3. EXECUTE (Executa)
            try:
                if cmd == "HALT":
                    self.executando = False
                    
                elif cmd == "NOP":
                    pass # Não faz nada
                    
                elif cmd == "LOAD":
                    # Ex: LOAD R2 13
                    reg = self.extrair_reg(partes[1])
                    end_mem = int(partes[2])
                    self.regs[reg] = int(self.memoria[end_mem])
                    
                elif cmd == "STORE":
                    # Ex: STORE 8 R3
                    end_mem = int(partes[1])
                    reg = self.extrair_reg(partes[2])
                    self.memoria[end_mem] = str(self.regs[reg])
                    
                elif cmd == "MOVE":
                    # Ex: MOVE R2 R0  (Copia R0 para R2)
                    reg_dest = self.extrair_reg(partes[1])
                    reg_src = self.extrair_reg(partes[2])
                    self.regs[reg_dest] = self.regs[reg_src]
                    
                elif cmd == "ADD":
                    # Ex: ADD R3 R2 R1  (R3 = R2 + R1)
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 + r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "SUB":
                    # Ex: SUB R3 R1 R0  (R3 = R1 - R0)
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 - r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "AND":
                    # Ex: AND R0 R3 R1
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 & r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "OR":
                    # Ex: OR R2 R2 R3
                    reg_dest = self.extrair_reg(partes[1])
                    r_src1 = self.regs[self.extrair_reg(partes[2])]
                    r_src2 = self.regs[self.extrair_reg(partes[3])]
                    resultado = r_src1 | r_src2
                    self.regs[reg_dest] = resultado
                    self.atualizar_flags(resultado)
                    
                elif cmd == "BRANCH":
                    # Ex: BRANCH 10
                    self.pc = int(partes[1])
                    
                elif cmd == "BZERO":
                    # Ex: BZERO 2
                    if self.flag_zero:
                        self.pc = int(partes[1])
                        
                elif cmd == "BNEG":
                    # Ex: BNEG 7
                    if self.flag_negativo:
                        self.pc = int(partes[1])
            except Exception as e:
                print(f"Erro ao executar a instrução '{self.ir}' na linha {self.pc-1}: {e}")
                self.executando = False

    def gerar_arquivos_saida(self):
        """Gera os três arquivos de saída com o estado FINAL da execução."""
        # 1. Unidade de Controle
        with open("unidade_controle.txt", "w") as f:
            f.write(f"{self.pc}\n")
            f.write(f"{self.ir}\n")
            
        # 2. Banco de Registradores
        with open("banco_registradores.txt", "w") as f:
            for reg in self.regs:
                f.write(f"{reg}\n")
                
        # 3. Memória RAM
        with open("memoria_ram.txt", "w") as f:
            for item in self.memoria:
                f.write(f"{item}\n")
                
        print("Execução finalizada. Arquivos de saída gerados com sucesso!")

# Execução do programa
if __name__ == "__main__":
    simulador = ProcessadorSimples()
    
    # "entrada.txt" no mesmo diretório
    simulador.carregar_programa("entrada.txt")
    
    if simulador.executando:
        simulador.ciclo_instrucao()
        simulador.gerar_arquivos_saida()