#!/bin/bash

echo "==================================="
echo "Exemplos de Execução - Zumbis vs Humanos"
echo "==================================="

echo -e "\n1. Jogo Padrão (50x50, 50 humanos, 10 zumbis)"
echo "Comando: python main.py"
echo "Pressione ENTER para executar..."
read
python main.py

echo -e "\n2. Jogo Rápido (20x20, movimento rápido)"
echo "Comando: python main.py --board-size 20 --humans 15 --zombies 5 --cooldown-max 0.5"
echo "Pressione ENTER para executar..."
read
python main.py --board-size 20 --humans 15 --zombies 5 --cooldown-max 0.5

echo -e "\n3. Estratégia de Perseguição"
echo "Comando: python main.py --board-size 30 --zombie-strategy PERSEGUICAO --zombie-range 5"
echo "Pressione ENTER para executar..."
read
python main.py --board-size 30 --zombie-strategy PERSEGUICAO --zombie-range 5

echo -e "\n4. Sem Bias Humano (movimento aleatório)"
echo "Comando: python main.py --no-human-bias --board-size 25"
echo "Pressione ENTER para executar..."
read
python main.py --no-human-bias --board-size 25

echo -e "\n5. Jogo Grande com Estratégia de Bloqueio"
echo "Comando: python main.py --board-size 70 --humans 80 --zombies 20 --zombie-strategy BLOQUEIO"
echo "Pressione ENTER para executar..."
read
python main.py --board-size 70 --humans 80 --zombies 20 --zombie-strategy BLOQUEIO