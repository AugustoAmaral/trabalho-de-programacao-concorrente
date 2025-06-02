import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Jogo de Zumbis vs Humanos - Programação Concorrente')
    parser.add_argument('--board-size', type=int, default=50,
                       help='Tamanho do tabuleiro NxN (padrão: 50, min: 10, max: 100)')
    parser.add_argument('--humans', type=int, default=50,
                       help='Quantidade inicial de humanos (padrão: 50)')
    parser.add_argument('--zombies', type=int, default=10,
                       help='Quantidade inicial de zumbis (padrão: 10)')
    parser.add_argument('--cooldown-min', type=float, default=0.5,
                       help='Tempo mínimo de cooldown em segundos (padrão: 0.5, min: 0.1)')
    parser.add_argument('--cooldown-max', type=float, default=2.0,
                       help='Tempo máximo de cooldown em segundos (padrão: 2.0, max: 5.0)')
    parser.add_argument('--game-timeout', type=float, default=300,
                       help='Tempo limite do jogo em segundos, 0 = sem limite (padrão: 300)')
    parser.add_argument('--position-wait-timeout', type=float, default=10.0,
                       help='Tempo máximo de espera por posição livre (padrão: 10.0)')
    parser.add_argument('--human-bias', type=float, default=0.6,
                       help='Fator de bias para movimento dos humanos (padrão: 0.6, entre 0.0 e 1.0)')
    parser.add_argument('--no-human-bias', action='store_true',
                       help='Desabilita movimento preferencial dos humanos')
    parser.add_argument('--zombie-strategy', type=str, default='ALEATORIO',
                       choices=['ALEATORIO', 'PERSEGUICAO', 'BLOQUEIO'],
                       help='Estratégia de movimento dos zumbis (padrão: ALEATORIO)')
    parser.add_argument('--zombie-range', type=int, default=3,
                       help='Distância máxima para perseguição dos zumbis (padrão: 3)')
    parser.add_argument('--display-rate', type=float, default=0.5,
                       help='Taxa de atualização da tela em segundos (padrão: 0.5)')
    parser.add_argument('--enable-realtime-logger', action='store_true',
                       help='Habilita exibição de logs em tempo real durante a execução (padrão: desabilitado)')
    
    args = parser.parse_args()
    validate_args(args)
    return args

def validate_args(args):
    if args.board_size < 10 or args.board_size > 100:
        print("Erro: Tamanho do tabuleiro deve estar entre 10 e 100")
        sys.exit(1)
    
    if args.humans < 1 or args.humans > args.board_size:
        print(f"Erro: Quantidade de humanos deve estar entre 1 e {args.board_size}")
        sys.exit(1)
    
    if args.zombies < 1 or args.zombies > args.board_size:
        print(f"Erro: Quantidade de zumbis deve estar entre 1 e {args.board_size}")
        sys.exit(1)
    
    if args.cooldown_min < 0.1:
        print("Erro: Cooldown mínimo deve ser pelo menos 0.1 segundos")
        sys.exit(1)
    
    if args.cooldown_max > 5.0 or args.cooldown_max < args.cooldown_min:
        print("Erro: Cooldown máximo deve ser no máximo 5.0 segundos e maior que o mínimo")
        sys.exit(1)
    
    if args.human_bias < 0.0 or args.human_bias > 1.0:
        print("Erro: Bias humano deve estar entre 0.0 e 1.0")
        sys.exit(1)
    
    if args.game_timeout < 0:
        print("Erro: Timeout do jogo não pode ser negativo")
        sys.exit(1)
