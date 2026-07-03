# Define as variáveis
PYTHON = python3
FRONTEND = frontend/main.py

.PHONY: run clean

run:
	@echo "Iniciando o Simulador..."
	@PYTHONPATH=. $(PYTHON) $(FRONTEND)

clean:
	@echo "Limpando arquivos temporários..."
	@rm -rf backend/__pycache__ frontend/__pycache__
	@rm -f *.txt backend/*.txt frontend/*.txt