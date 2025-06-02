import threading
import time
import os
from entity import EntityType

class GameDisplay:
    def __init__(self, game_board, update_rate=0.5):
        self.game_board = game_board
        self.update_rate = update_rate
        self.running = False
        self.display_thread = None
        self.lock = threading.Lock()
        
    def start(self):
        self.running = True
        self.display_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.display_thread.start()
    
    def stop(self):
        self.running = False
        if self.display_thread:
            self.display_thread.join(timeout=1)
    
    def _update_loop(self):
        while self.running and not self.game_board.game_ended:
            self.show()
            time.sleep(self.update_rate)
    
    def show(self):
        with self.lock:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            board = [[' ' for _ in range(self.game_board.board_size)] for _ in range(self.game_board.board_size)]
            
            human_count = 0
            zombie_count = 0
            
            for entity in self.game_board.entities:
                if entity.is_alive:
                    x, y = entity.position_x, entity.position_y
                    if 0 <= x < self.game_board.board_size and 0 <= y < self.game_board.board_size:
                        if entity.type == EntityType.HUMAN:
                            board[y][x] = 'H'
                            human_count += 1
                        else:
                            board[y][x] = 'Z'
                            zombie_count += 1
            
            print("\n" + "="*60)
            print("ZUMBIS VS HUMANOS")
            print("="*60)
            
            print("\n   ", end="")
            for i in range(self.game_board.board_size):
                print(f"{i%10}", end="")
            print()
            
            print("  +" + "-"*self.game_board.board_size + "+")
            
            for y in range(self.game_board.board_size):
                print(f"{y:2}|", end="")
                for x in range(self.game_board.board_size):
                    if board[y][x] == 'H':
                        print("🧑", end="")
                    elif board[y][x] == 'Z':
                        print("🧟", end="")
                    else:
                        print("⬜", end="")
                print("|")
            
            print("  +" + "-"*self.game_board.board_size + "+")
            
            stats = self.game_board.statistics.get_statistics()
            
            print(f"\nHumanos: {human_count} | Zumbis: {zombie_count}")
            print(f"Escaparam: {stats['escapes']} | Transformações: {stats['transformations']}")
            print(f"Tempo: {stats['total_time']:.1f}s")
            
            status = "EM ANDAMENTO"
            if self.game_board.game_ended:
                if self.game_board.winner == "HUMANS":
                    status = "VITÓRIA DOS HUMANOS!"
                elif self.game_board.winner == "ZOMBIES":
                    status = "VITÓRIA DOS ZUMBIS!"
                else:
                    status = "EMPATE!"
            
            print(f"\nStatus: {status}")
            print("\nPressione Ctrl+C para interromper o jogo.")
    
    def show_final_statistics(self):
        stats = self.game_board.statistics.get_statistics()
        
        print("\n" + "="*60)
        print("ESTATÍSTICAS FINAIS")
        print("="*60)
        
        print(f"\nResultado: {self.game_board.winner}")
        print(f"Tempo total: {stats['total_time']:.2f} segundos")
        
        print(f"\nContagem inicial: {stats['initial_humans']} humanos, {stats['initial_zombies']} zumbis")
        print(f"Contagem final: {stats['final_humans']} humanos, {stats['final_zombies']} zumbis")
        
        print(f"\nHumanos que escaparam: {stats['escapes']}")
        print(f"Transformações: {stats['transformations']}")
        print(f"Colisões: {stats['collisions']}")
        
        print(f"\nMovimentos totais:")
        for entity_type, count in stats['total_moves'].items():
            print(f"  {entity_type}: {count}")
        
        print(f"\nTempo médio de sobrevivência humana: {stats['avg_human_survival']:.2f}s")
        print(f"Tempo médio por movimento: {stats['avg_move_time']:.4f}s")
        
        if stats['most_used_positions']:
            print(f"\nPosições mais ocupadas:")
            for pos, count in stats['most_used_positions'][:5]:
                print(f"  {pos}: {count} vezes")