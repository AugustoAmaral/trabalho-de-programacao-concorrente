import sys
from game_board import GameBoard
from args_parser import parse_arguments

def main():
    args = parse_arguments()
    
    print("="*60)
    print("ZUMBIS VS HUMANOS - PROGRAMAÇÃO CONCORRENTE")
    print("="*60)
    print(f"\nConfigurações:")
    print(f"  Tabuleiro: {args.board_size}x{args.board_size}")
    print(f"  Humanos: {args.humans}")
    print(f"  Zumbis: {args.zombies}")
    print(f"  Cooldown: {args.cooldown_min}s - {args.cooldown_max}s")
    print(f"  Timeout: {'Sem limite' if args.game_timeout == 0 else f'{args.game_timeout}s'}")
    print(f"  Estratégia Zumbi: {args.zombie_strategy}")
    print(f"  Bias Humano: {'Desabilitado' if args.no_human_bias else args.human_bias}")
    print("\nIniciando jogo em 3 segundos...")
    
    import time
    time.sleep(3)
    
    game = GameBoard()
    game.configure(
        board_size=args.board_size,
        humans_amount=args.humans,
        zombies_amount=args.zombies,
        cooldown_min=args.cooldown_min,
        cooldown_max=args.cooldown_max,
        game_timeout=args.game_timeout,
        position_wait_timeout=args.position_wait_timeout,
        human_movement_bias_enabled=not args.no_human_bias,
        human_movement_bias=args.human_bias,
        zombie_movement_strategy=args.zombie_strategy,
        zombie_persecution_range=args.zombie_range,
        display_update_rate=args.display_rate
    )
    
    try:
        game_thread = game.start_game()
        game_thread.join()
    except KeyboardInterrupt:
        print("\n\nJogo interrompido pelo usuário")
        game.end_game("INTERRUPTED")
    except Exception as e:
        print(f"\n\nErro durante execução do jogo: {e}")
        game.end_game("ERROR")

if __name__ == "__main__":
    main()