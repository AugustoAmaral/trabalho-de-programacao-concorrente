# Jogo Zumbis vs Humanos - Programação Concorrente

## Descrição

Jogo de tabuleiro concorrente onde humanos tentam atravessar o tabuleiro enquanto zumbis tentam impedi-los. Cada entidade é executada em sua própria thread, demonstrando conceitos de programação concorrente.

## Requisitos

- Python 3.7+
- Sem dependências externas

## Como Executar

### Execução Básica
```bash
python3 main.py
```

### Execução com Parâmetros Personalizados
```bash
python3 main.py --board-size 30 --humans 40 --zombies 15 --zombie-strategy PERSEGUICAO
```

## Parâmetros Disponíveis

| Parâmetro | Descrição | Padrão | Limites |
|-----------|-----------|---------|---------|
| `--board-size` | Tamanho do tabuleiro NxN | 50 | 10-100 |
| `--humans` | Quantidade inicial de humanos | 50 | 1-N |
| `--zombies` | Quantidade inicial de zumbis | 10 | 1-N |
| `--cooldown-min` | Tempo mínimo entre movimentos (s) | 0.5 | ≥0.1 |
| `--cooldown-max` | Tempo máximo entre movimentos (s) | 2.0 | ≤5.0 |
| `--game-timeout` | Tempo limite do jogo (s), 0=sem limite | 300 | ≥0 |
| `--position-wait-timeout` | Tempo máximo de espera por posição (s) | 5.0 | >0 |
| `--human-bias` | Probabilidade de humanos moverem à direita | 0.6 | 0.0-1.0 |
| `--no-human-bias` | Desabilita movimento preferencial | False | - |
| `--zombie-strategy` | Estratégia de movimento dos zumbis | ALEATORIO | ALEATORIO, PERSEGUICAO, BLOQUEIO |
| `--zombie-range` | Alcance para perseguição de zumbis | 3 | >0 |
| `--display-rate` | Taxa de atualização da tela (s) | 0.5 | >0 |

## Regras do Jogo

1. **Objetivo dos Humanos**: Atravessar o tabuleiro da esquerda para a direita
2. **Objetivo dos Zumbis**: Transformar todos os humanos em zumbis
3. **Transformação**: Quando um zumbi fica adjacente a um humano, o humano se transforma em zumbi
4. **Movimento**: Cada entidade move 1 casa por vez (horizontal ou vertical)
5. **Vitória**: 
   - Humanos vencem se pelo menos um chegar ao lado direito
   - Zumbis vencem se não houver mais humanos
   - Empate se o tempo limite for atingido

## Estratégias dos Zumbis

- **ALEATORIO**: Movimento completamente aleatório
- **PERSEGUICAO**: Move em direção ao humano mais próximo dentro do alcance
- **BLOQUEIO**: Tenta se posicionar entre humanos e o objetivo

## Símbolos do Tabuleiro

- 🧑 : Humano
- 🧟 : Zumbi
- ⬜ : Espaço vazio

## Exemplos de Uso

### Jogo Rápido (tabuleiro pequeno)
```bash
python3 main.py --board-size 20 --humans 15 --zombies 5 --cooldown-max 1.0
```

### Jogo Ultra Rápido (Tabuleiro pequeno)
```bash
python3 main.py --board-size 20 --humans 10 --zombies 5 --cooldown-min 0.1 --cooldown-max 0.5 --display-rate 0.1 --human-bias 0.3 --position-wait-timeout 2
```

### Jogo Estratégico (zumbis perseguidores)
```bash
python3 main.py --zombie-strategy PERSEGUICAO --zombie-range 5 --no-human-bias
```

### Jogo Longo (sem timeout)
```bash
python3 main.py --game-timeout 0 --board-size 100 --humans 100 --zombies 20
```

## Interrupção do Jogo

Pressione `Ctrl+C` a qualquer momento para interromper o jogo de forma segura. Todas as threads serão finalizadas corretamente.

## Logs

O jogo gera automaticamente um arquivo de log com timestamp contendo todos os eventos do jogo, incluindo:
- Movimentações de cada entidade
- Transformações
- Escapes
- Colisões e esperas

## Arquivos do Projeto

- `main.py` - Ponto de entrada do programa
- `args_parser.py` - Parsing e validação de argumentos da linha de comando
- `game_board.py` - Lógica principal do jogo (Singleton)
- `entity.py` - Classe abstrata para entidades
- `human.py` - Implementação dos humanos
- `zombie.py` - Implementação dos zumbis
- `game_display.py` - Interface de exibição (Observer)
- `game_statistics.py` - Coleta de estatísticas
- `game_logger.py` - Sistema de log thread-safe