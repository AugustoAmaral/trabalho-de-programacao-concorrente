# Jogo Zombie - Programação Concorrente

Este projeto implementa um jogo de tabuleiro onde elementos azuis tentam chegar à direita do tabuleiro enquanto zombies tentam infectá-los.

## 📋 Descrição do Projeto

- **Tabuleiro**: Array 2D de 50x50 posições
- **Elementos**: 
  - 🔵 **Azuis**: Tentam chegar à direita do tabuleiro
  - 🧟 **Zombies**: Infectam elementos azuis adjacentes
- **Movimento**: Todos os elementos se movem aleatoriamente (horizontal/vertical)
- **Infecção**: Zombies convertem azuis adjacentes em zombies
- **Condições de Fim**:
  - Todos os elementos viram zombies (derrota)
  - Um elemento azul chega à direita (vitória)

## 🗂️ Estrutura dos Módulos

### 1. `tabuleiro_display.py`
Módulo responsável pela exibição do jogo no terminal (CLI):
- Exibe o tabuleiro com símbolos visuais
- Atualiza a tela em tempo real
- Mostra informações da rodada
- Exibe resultado final

### 2. `jogo_logica.py`
Contém a lógica principal do jogo:
- Inicialização do tabuleiro
- Movimentação dos elementos
- Sistema de infecção
- Verificação das condições de fim
- Controle de rodadas

### 3. `main_programa.py`
Programa principal que executa o jogo:
- Interface de configuração
- Loop principal do jogo
- Tratamento de exceções
- Controle de execução

### 4. `elemento_concorrente.py`
Implementação da programação concorrente:
- Cada elemento roda em sua própria thread
- Sincronização com locks
- Gerenciamento de threads
- Movimentação assíncrona

## 🚀 Como Executar

### Versão Simples (Sequencial)
```bash
python3 main_programa.py
```

### Versão Concorrente
```python
from elemento_concorrente import JogoZombieConcorrente
from tabuleiro_display import TabuleiroCLI

# Criar instâncias
jogo = JogoZombieConcorrente()
display = TabuleiroCLI()

# Inicializar e executar
jogo.inicializar_jogo(10, 5)  # 10 azuis, 5 zombies

# Loop do jogo
try:
    while True:
        display.exibir_tabuleiro(jogo.tabuleiro, jogo.rodada)
        
        fim, motivo = jogo.verificar_condicoes_fim()
        if fim:
            display.exibir_resultado(motivo, jogo.rodada)
            break
            
        display.pausar(0.5)
        jogo.rodada += 1

finally:
    jogo.finalizar()  # Para todas as threads
```

## ⚙️ Configurações

### Parâmetros Personalizáveis
- **Tamanho do tabuleiro**: Padrão 50x50
- **Número de elementos azuis**: Padrão 10 (máximo recomendado: 20)
- **Número de zombies**: Padrão 5 (máximo recomendado: 10)
- **Velocidade de atualização**: Configurável no display

### Modificar Configurações
```python
# No main_programa.py ou ao criar as instâncias
jogo = JogoZombie(tamanho=30)  # Tabuleiro 30x30
jogo.inicializar_jogo(num_azuis=15, num_zombies=3)
```

## 🎮 Controles

- **Enter**: Avançar configuração
- **Ctrl+C**: Interromper jogo
- **s/n**: Escolhas de configuração

## 🔧 Recursos Implementados

### ✅ Funcionalidades Básicas
- [x] Tabuleiro 50x50
- [x] Elementos azuis e zombies
- [x] Movimento aleatório
- [x] Sistema de infecção
- [x] Condições de vitória/derrota
- [x] Interface CLI com símbolos visuais

### ✅ Programação Concorrente
- [x] Threads individuais para cada elemento
- [x] Sincronização com locks
- [x] Movimento assíncrono
- [x] Gerenciamento seguro de threads

### ✅ Recursos Adicionais
- [x] Configuração personalizada
- [x] Estatísticas em tempo real
- [x] Tratamento de erros
- [x] Interface amigável
- [x] Documentação completa

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐
│  main_programa  │───▶│  jogo_logica     │
└─────────────────┘    └──────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│tabuleiro_display│    │elemento_concorren│
└─────────────────┘    └──────────────────┘
```

### Fluxo de Execução
1. **Inicialização**: Configuração e criação do tabuleiro
2. **Loop Principal**: Atualização e exibição contínua
3. **Movimentação**: Elementos se movem independentemente
4. **Verificação**: Checagem das condições de fim
5. **Finalização**: Limpeza e exibição do resultado

## 🐛 Tratamento de Erros

- **Posições inválidas**: Verificação de limites do tabuleiro
- **Concorrência**: Locks para evitar condições de corrida
- **Interrupção**: Graceful shutdown com Ctrl+C
- **Threads**: Timeout e cleanup automático
- **Entrada inválida**: Valores padrão em caso de erro

## 📊 Exemplo de Execução

```
=== JOGO ZOMBIE - RODADA 15 ===
🔵 = Elemento Azul | 🧟 = Zombie | ⬜ = Vazio
Objetivo: Elementos azuis devem chegar à direita do tabuleiro!
------------------------------------------------------------
    0         10        20        30        40        
 0 ⬜⬜🔵⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
 1 ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
 2 ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🧟⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
...
------------------------------------------------------------
Pressione Ctrl+C para parar o jogo
```

## 🤝 Contribuições

Para modificar ou estender o projeto:

1. **Adicionar novos tipos de elementos**: Modificar `jogo_logica.py`
2. **Melhorar interface**: Atualizar `tabuleiro_display.py`
3. **Otimizar concorrência**: Ajustar `elemento_concorrente.py`
4. **Novas regras**: Implementar em `jogo_logica.py`

## 📝 Observações Técnicas

- **Python 3.7+** requerido para threading
- **Cross-platform**: Funciona em Windows, Linux e macOS
- **Performance**: Otimizado para tabuleiros até 100x100
- **Memória**: Uso eficiente com cleanup automático
- **Segurança**: Thread-safe com proper locking

## 🎯 Próximas Melhorias Sugeridas

- [ ] Interface gráfica com Pygame ou Tkinter
- [ ] Salvamento e carregamento de jogos
- [ ] Diferentes tipos de zombies
- [ ] Power-ups para elementos azuis
- [ ] Multiplayer em rede
- [ ] Análise de performance com profiling
- [ ] Logs detalhados de execução