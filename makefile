.PHONY: run clean test-small test-medium test-large test-strategies help

help:
	@echo "Comandos disponíveis:"
	@echo "  make run         - Executa o jogo com configurações padrão"
	@echo "  make test-small  - Testa em tabuleiro pequeno (20x20)"
	@echo "  make test-medium - Testa em tabuleiro médio (50x50)"
	@echo "  make test-large  - Testa em tabuleiro grande (80x80)"
	@echo "  make test-strategies - Testa todas as estratégias"
	@echo "  make clean       - Remove arquivos temporários e logs"

run:
	python main.py

test-small:
	python main.py --board-size 20 --humans 15 --zombies 5 --cooldown-max 1.0 --game-timeout 60

test-medium:
	python main.py --board-size 50 --humans 50 --zombies 10 --game-timeout 120

test-large:
	python main.py --board-size 80 --humans 100 --zombies 25 --game-timeout 180

test-strategies:
	@echo "Testando estratégia ALEATORIO..."
	python main.py --board-size 30 --zombie-strategy ALEATORIO --game-timeout 60
	@echo "\nTestando estratégia PERSEGUICAO..."
	python main.py --board-size 30 --zombie-strategy PERSEGUICAO --zombie-range 5 --game-timeout 60
	@echo "\nTestando estratégia BLOQUEIO..."
	python main.py --board-size 30 --zombie-strategy BLOQUEIO --game-timeout 60

clean:
	rm -rf __pycache__
	rm -f *.pyc
	rm -f game_log*.txt
	rm -f *.log
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true