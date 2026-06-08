# 🟣 Codificador e Decodificador de Hamming 🟡

Projeto desenvolvido para a disciplina de Arquitetura de Computadores. Esta aplicação implementa o Algoritmo de Hamming para codificação e decodificação de mensagens binárias de até 8 bits, permitindo a detecção e correção de erros de 1 bit.

## 🛠️ Tecnologias Utilizadas

* **Python 3:** Lógica backend e manipulação de bits (bitwise operations e XOR).
* **Tkinter:** Interface gráfica nativa customizada.

## ⚙️ Funcionalidades

* **Codificação:** Calcula os bits de paridade dinamicamente e os intercala na mensagem original (exibindo-os entre colchetes).
* **Decodificação:** Recebe uma mensagem codificada, recalcula a paridade de cada grupo e, caso haja erro de transmissão, detecta a posição exata, corrige o bit invertido e extrai a mensagem original.
* **Validação de Entrada:** Bloqueio de caracteres não-binários e limite estrito de 8 bits para a mensagem original.

## 💻 Como executar no Linux

Certifique-se de ter o pacote do Tkinter instalado:

```bash
sudo apt update && sudo apt install python3-tk
```

Execute o arquivo principal:

```bash
python3 hamming.py
```
