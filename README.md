# Jogo Zumbis vs Humanos - Programação Concorrente

## Descrição

Jogo de tabuleiro concorrente onde humanos tentam atravessar o tabuleiro enquanto zumbis tentam impedi-los. Cada entidade é executada em sua própria thread, demonstrando conceitos de programação concorrente.

Este projeto implementa um sistema de simulação multi-thread onde cada humano e zumbi opera como uma entidade independente, executando sua própria lógica de comportamento simultaneamente. O jogo serve como uma demonstração prática de vários conceitos de programação concorrente, incluindo:

- **Threads**: Cada entidade (humano ou zumbi) executa em sua própria thread
- **Sincronização**: Utiliza mecanismos para evitar condições de corrida no acesso ao tabuleiro
- **Deadlocks**: Implementa timeouts para prevenir impasses entre entidades
- **Comunicação entre threads**: Coordena interações entre humanos e zumbis
- **Padrão Observer**: Para atualização da interface gráfica sem bloquear a lógica do jogo

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

### Explicação Detalhada dos Parâmetros

- **`--board-size`**: Define as dimensões do tabuleiro quadrado (N×N). Tabuleiros maiores oferecem mais espaço para manobras estratégicas, mas o jogo pode levar mais tempo.

- **`--humans`**: Define o número inicial de humanos no lado esquerdo do tabuleiro. Quanto mais humanos, maiores as chances de vitória para o lado humano, mas também torna o jogo mais complexo computacionalmente.

- **`--zombies`**: Define o número inicial de zumbis distribuídos pelo tabuleiro. Aumentar este valor torna o jogo mais difícil para os humanos.

- **`--cooldown-min` e `--cooldown-max`**: Define o intervalo de tempo aleatório entre movimentos de cada entidade. Valores menores tornam o jogo mais rápido, enquanto valores maiores permitem melhor visualização das estratégias.

- **`--game-timeout`**: Estabelece o tempo máximo de duração do jogo em segundos. Se nenhum lado vencer dentro deste período, o jogo termina em empate. O valor 0 desativa o timeout, permitindo que o jogo continue indefinidamente.

- **`--position-wait-timeout`**: Tempo máximo que uma entidade espera por uma posição livre antes de desistir e tentar novamente. Isso evita que entidades fiquem presas indefinidamente em situações de bloqueio.

- **`--human-bias`**: Controla a tendência dos humanos se moverem para a direita (em direção ao objetivo). Um valor de 0.6 significa que há 60% de chance do humano escolher um movimento que o aproxime do objetivo. Valores mais altos tornam os humanos mais determinados, enquanto valores mais baixos os tornam mais imprevisíveis.

- **`--no-human-bias`**: Quando ativado, desabilita completamente a tendência direcional dos humanos, fazendo com que se movam aleatoriamente como os zumbis no modo ALEATORIO.

- **`--zombie-strategy`**: Define o comportamento dos zumbis:
  - ALEATORIO: Movimento completamente aleatório, sem qualquer inteligência
  - PERSEGUICAO: Zumbis perseguem ativamente os humanos dentro de seu alcance de percepção
  - BLOQUEIO: Zumbis tentam posicionar-se estrategicamente para bloquear a passagem dos humanos

- **`--zombie-range`**: Determina a distância máxima em que um zumbi pode detectar um humano quando está no modo PERSEGUICAO ou BLOQUEIO. Aumentar este valor torna os zumbis mais eficientes na caça.

- **`--display-rate`**: Define o intervalo de tempo entre atualizações da interface gráfica. Valores menores proporcionam uma animação mais suave, mas podem consumir mais recursos do sistema.

## Regras do Jogo

1. **Objetivo dos Humanos**: Atravessar o tabuleiro da esquerda para a direita
2. **Objetivo dos Zumbis**: Transformar todos os humanos em zumbis
3. **Transformação**: Quando um zumbi fica adjacente a um humano, o humano se transforma em zumbi
4. **Movimento**: Cada entidade move 1 casa por vez (horizontal ou vertical)
5. **Vitória**: 
   - Humanos vencem se pelo menos um chegar ao lado direito
   - Zumbis vencem se não houver mais humanos
   - Empate se o tempo limite for atingido

### Mecânica de Jogo Detalhada

- **Posicionamento Inicial**: 
  - Os humanos são posicionados aleatoriamente no lado esquerdo do tabuleiro
  - Os zumbis são distribuídos aleatoriamente no lado direito do tabuleiro

- **Sistema de Turnos**:
  - Não há turnos fixos. Cada entidade move-se independentemente de acordo com seu próprio temporizador em sua propria thread
  - O intervalo entre movimentos é aleatório dentro dos limites definidos (cooldown-min e cooldown-max)

- **Colisões**:
  - Duas entidades não podem ocupar a mesma posição simultaneamente
  - Quando uma entidade tenta mover para uma posição ocupada, ela aguarda até que a posição seja liberada ou até que o timeout seja atingido

- **Transformação**:
  - A transformação de humano em zumbi ocorre quando um zumbi se move para uma posição adjacente (horizontal, vertical ou diagonal) a um humano ou quando um humano se move para uma posição adjacente a um zumbi
  - O humano transformado permanece na mesma posição, mas agora como um zumbi
  - O novo zumbi passa a seguir a estratégia de movimento dos outros zumbis

- **Condições de Fim de Jogo**:
  - Se ao menos um humano alcançar a coluna mais à direita do tabuleiro, os humanos vencem imediatamente
  - Se todos os humanos forem transformados em zumbis, os zumbis vencem
  - Se o tempo limite for atingido sem que nenhuma das condições anteriores seja satisfeita, o jogo termina em empate

## Estratégias dos Zumbis

- **ALEATORIO**: Movimento completamente aleatório
  - O zumbi escolhe aleatoriamente uma direção válida (norte, sul, leste ou oeste)
  - Não há qualquer inteligência ou preferência direcional
  - Esta estratégia é a menos eficiente, mas pode surpreender com movimentos imprevisíveis

- **PERSEGUICAO**: Move em direção ao humano mais próximo dentro do alcance
  - O zumbi escaneia sua vizinhança até um raio definido por `--zombie-range`
  - Se detectar um humano dentro do alcance, move-se na direção que o aproxima deste humano
  - Se múltiplos humanos estiverem no alcance, o zumbi escolhe o mais próximo
  - Se nenhum humano estiver no alcance, move-se aleatoriamente como no modo ALEATORIO

- **BLOQUEIO**: Tenta se posicionar entre humanos e o objetivo
  - O zumbi analisa o tabuleiro para até um raio definido por `--zombie-range` para identificar rotas prováveis dos humanos
  - Tenta posicionar-se estrategicamente para formar barreiras que bloqueiam o caminho para o lado direito
  - Esta é a estratégia mais sofisticada, tentando maximizar a cobertura da área com o mínimo de zumbis
  - Zumbis colaboram indiretamente e de forma independente para criar formações de bloqueio

## Símbolos do Tabuleiro

- 🧑 : Humano
- 🧟 : Zumbi
- ⬜ : Espaço vazio

## Exemplos de Uso

### Jogo Rápido (tabuleiro pequeno)
```bash
python3 main.py --board-size 20 --humans 15 --zombies 5 --cooldown-max 1.0
```
Este modo utiliza um tabuleiro menor (20x20) com menos entidades e menor tempo entre movimentos, resultando em partidas rápidas ideais para testes ou demonstrações. Com poucos zumbis e espaço reduzido, os humanos têm uma chance razoável de vitória mesmo com movimentos mais frequentes.

### Jogo Ultra Rápido (Tabuleiro pequeno)
```bash
python3 main.py --board-size 20 --humans 10 --zombies 5 --cooldown-min 0.1 --cooldown-max 0.5 --display-rate 0.1 --human-bias 0.3 --position-wait-timeout 2
```
Esta configuração cria um jogo extremamente dinâmico com movimentos muito rápidos (até 10 movimentos por segundo). O human-bias reduzido (0.3) faz os humanos se moverem menos diretamente em direção ao objetivo, tornando seus movimentos mais imprevisíveis. O display-rate acelerado (0.1s) garante que a tela acompanhe a velocidade do jogo. Ideal para demonstrar a concorrência em alta velocidade.

### Jogo Estratégico (zumbis perseguidores)
```bash
python3 main.py --zombie-strategy PERSEGUICAO --zombie-range 5 --no-human-bias
```
Este modo ativa a inteligência dos zumbis, fazendo-os perseguir ativamente os humanos dentro de um alcance ampliado (5 unidades). Ao mesmo tempo, os humanos perdem sua tendência de mover à direita (--no-human-bias), tornando o jogo um verdadeiro desafio de sobrevivência. Este modo destaca como diferentes comportamentos programados nas threads podem criar dinâmicas emergentes interessantes.

### Jogo Longo (sem timeout)
```bash
python3 main.py --game-timeout 0 --board-size 100 --humans 100 --zombies 20
```
Esta configuração cria uma simulação de longa duração em um tabuleiro enorme (100x100) com muitas entidades. Sem limite de tempo (--game-timeout 0), o jogo continua até que uma condição de vitória seja alcançada. Este modo é excelente para observar padrões emergentes de comportamento ao longo do tempo e testar a estabilidade do sistema concorrente sob cargas prolongadas.

### Modo Apocalipse (muitos zumbis, estratégia de bloqueio)
```bash
python3 main.py --board-size 50 --humans 20 --zombies 40 --zombie-strategy BLOQUEIO
```
Um cenário desafiador onde os humanos estão em menor número e enfrentam zumbis usando a estratégia de bloqueio. Neste modo, os zumbis trabalham coletivamente para cortar rotas de fuga, criando um verdadeiro "apocalipse zumbi". É uma excelente demonstração de como entidades independentes podem criar comportamentos coordenados emergentes.

### Modo Equilibrado (chances iguais)
```bash
python3 main.py --board-size 40 --humans 25 --zombies 15 --human-bias 0.7 --zombie-strategy PERSEGUICAO --zombie-range 2
```
Esta configuração busca um equilíbrio entre humanos e zumbis. Os humanos têm um forte bias direcional (0.7), enquanto os zumbis perseguem, mas com alcance limitado (2). Isso cria um jogo competitivo onde ambos os lados têm chances similares de vitória, ideal para observar diferentes estratégias emergentes.

## Interrupção do Jogo

Pressione `Ctrl+C` a qualquer momento para interromper o jogo de forma segura. Todas as threads serão finalizadas corretamente.

O sistema implementa um mecanismo de captura de sinal que:
1. Interrompe a thread principal e o display
2. Sinaliza a todas as threads de entidades para pararem de forma ordenada
3. Aguarda a finalização de todas as threads antes de encerrar o programa
4. Salva os logs e estatísticas finais antes de encerrar

Esta implementação demonstra como gerenciar o encerramento seguro de um sistema multi-thread.

## Logs

O jogo gera automaticamente um arquivo de log com timestamp contendo todos os eventos do jogo, incluindo:
- Movimentações de cada entidade
- Transformações
- Escapes
- Colisões e esperas

Os logs são armazenados na pasta `logs/` com o formato `game_log_[timestamp].txt`. Eles são úteis para:
- Analisar o comportamento das entidades ao longo do tempo
- Depurar problemas de sincronização
- Coletar estatísticas sobre o desempenho do sistema
- Visualizar eventos importantes que podem ocorrer muito rapidamente na tela

O sistema de logging é thread-safe, permitindo que múltiplas entidades registrem eventos simultaneamente sem conflitos.

## Aspectos Técnicos

### Concorrência

Este projeto demonstra diversos aspectos da programação concorrente:

- **Threading**: Cada entidade (humano ou zumbi) executa em sua thread independente, permitindo movimentos verdadeiramente paralelos
- **Sincronização**: Usa locks para evitar condições de corrida no acesso às posições do tabuleiro
- **Comunicação entre threads**: Implementa mecanismos para que entidades detectem e reajam a eventos causados por outras entidades
- **Prevenção de deadlocks**: Utiliza timeouts e estratégias de desistência para evitar impasses permanentes
- **Pattern Observer**: A interface gráfica observa mudanças no estado do jogo sem interferir na lógica concorrente

### Arquitetura

O projeto segue uma arquitetura modular com separação clara de responsabilidades:

- **Modelo**: Classes que representam o estado do jogo (`game_board.py`, `entity.py`, `human.py`, `zombie.py`)
- **Visualização**: Interface para o usuário (`game_display.py`)
- **Controle**: Gerenciamento do jogo e regras (`main.py`, `args_parser.py`)
- **Utilitários**: Funcionalidades de suporte (`game_logger.py`, `game_statistics.py`)

Esta separação facilita a extensão do jogo com novas funcionalidades.

## Arquivos do Projeto

- `main.py` - Ponto de entrada do programa, inicializa e coordena todas as componentes do jogo
- `args_parser.py` - Parsing e validação de argumentos da linha de comando, estabelece os parâmetros de configuração
- `game_board.py` - Lógica principal do jogo (Singleton), gerencia o estado do tabuleiro e coordena as interações entre entidades
- `entity.py` - Classe abstrata para entidades, define o comportamento base para humanos e zumbis
- `human.py` - Implementação dos humanos, incluindo sua lógica de movimento e transformação
- `zombie.py` - Implementação dos zumbis, incluindo as diferentes estratégias de movimento
- `game_display.py` - Interface de exibição (Observer), renderiza o estado do jogo no terminal
- `game_statistics.py` - Coleta de estatísticas sobre o jogo, como taxa de transformações e tempo até vitória
- `game_logger.py` - Sistema de log thread-safe para registrar eventos do jogo