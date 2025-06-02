import threading
import time
import random
import signal
import sys
from entity import EntityType, EntityState
from human import Human
from zombie import Zombie
from game_logger import GameLogger, LogEvent
from game_statistics import GameStatistics
from game_display import GameDisplay

class GameBoard:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.board_size = 50
            self.humans_amount = 50
            self.zombies_amount = 10
            self.cooldown_min = 0.5
            self.cooldown_max = 2.0
            self.game_timeout = 300
            self.position_wait_timeout = 5.0
            self.human_movement_bias_enabled = True
            self.human_movement_bias = 0.6
            self.zombie_movement_strategy = "ALEATORIO"
            self.zombie_persecution_range = 3
            self.display_update_rate = 0.5
            
            self.entities = []
            self.board_lock = threading.Lock()
            self.position_locks = {}
            self.position_conditions = {}
            self.game_ended = False
            self.winner = None
            self.start_time = None
            
            self.logger = GameLogger()
            self.statistics = GameStatistics()
            self.display = None
            
            self.initialized = True
    
    def configure(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def initialize_positions(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.position_locks[(x, y)] = threading.Lock()
                self.position_conditions[(x, y)] = threading.Condition(self.position_locks[(x, y)])
    
    def start_game(self):
        self.logger.initialize(f"game_log_{int(time.time())}.txt")
        self.logger.log(LogEvent.GAME_START, f"Game started with {self.humans_amount} humans and {self.zombies_amount} zombies")
        
        self.initialize_positions()
        self._place_entities()
        
        self.statistics.set_initial_counts(self.humans_amount, self.zombies_amount)
        
        self.display = GameDisplay(self, self.display_update_rate)
        self.display.start()
        
        self.start_time = time.time()
        
        for entity in self.entities:
            entity.set_game_board(self)
            entity.start()
        
        signal.signal(signal.SIGINT, self._signal_handler)
        
        if self.game_timeout > 0:
            timeout_thread = threading.Thread(target=self._timeout_checker, daemon=True)
            timeout_thread.start()
        
        game_thread = threading.Thread(target=self._game_loop)
        game_thread.start()
        
        return game_thread
    
    def _place_entities(self):
        available_human_positions = [(0, y) for y in range(self.board_size)]
        available_zombie_positions = [(self.board_size - 1, y) for y in range(self.board_size)]
        
        random.shuffle(available_human_positions)
        random.shuffle(available_zombie_positions)
        
        for i in range(min(self.humans_amount, len(available_human_positions))):
            x, y = available_human_positions[i]
            human = Human(x, y)
            self.entities.append(human)
        
        for i in range(min(self.zombies_amount, len(available_zombie_positions))):
            x, y = available_zombie_positions[i]
            zombie = Zombie(x, y)
            self.entities.append(zombie)
    
    def _game_loop(self):
        while not self.game_ended:
            time.sleep(0.1)
            self.check_win_condition()
    
    def _timeout_checker(self):
        time.sleep(self.game_timeout)
        if not self.game_ended:
            self.end_game("TIMEOUT")
    
    def _signal_handler(self, signum, frame):
        print("\n\nInterrupção recebida. Finalizando o jogo...")
        self.end_game("INTERRUPTED")
        sys.exit(0)
    
    def is_valid_position(self, x, y):
        return 0 <= x < self.board_size and 0 <= y < self.board_size
    
    def is_position_busy(self, x, y):
        with self.board_lock:
            for entity in self.entities:
                if entity.is_alive and entity.position_x == x and entity.position_y == y:
                    return True
        return False
    
    def move_entity(self, entity, new_x, new_y):
        if not self.is_valid_position(new_x, new_y):
            return False
        
        old_x, old_y = entity.position_x, entity.position_y
        
        with self.position_conditions[(new_x, new_y)]:
            wait_start = time.time()
            while self.is_position_busy(new_x, new_y):
                if time.time() - wait_start > self.position_wait_timeout:
                    self.statistics.record_collision()
                    self.logger.log(
                        LogEvent.MOVE_WAITING,
                        f"Movement timeout waiting for position ({new_x},{new_y})",
                        entity.id,
                        entity.type.value
                    )
                    return False
                
                self.logger.log(
                    LogEvent.MOVE_WAITING,
                    f"Waiting for position ({new_x},{new_y}) to be free",
                    entity.id,
                    entity.type.value
                )
                
                if not self.position_conditions[(new_x, new_y)].wait(timeout=0.5):
                    if self.game_ended or not entity.is_alive:
                        return False
            
            with self.board_lock:
                entity.position_x = new_x
                entity.position_y = new_y
            
            self.statistics.record_move(entity.type.value, (new_x, new_y))
        
        with self.position_conditions[(old_x, old_y)]:
            self.position_conditions[(old_x, old_y)].notify_all()
        
        self.check_transformations(new_x, new_y)
        
        return True
    
    def check_transformations(self, x, y):
        with self.board_lock:
            entity_at_pos = None
            for entity in self.entities:
                if entity.is_alive and entity.position_x == x and entity.position_y == y:
                    entity_at_pos = entity
                    break
            
            if entity_at_pos and entity_at_pos.type == EntityType.ZOMBIE:
                adjacent_positions = [
                    (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                ]
                
                for adj_x, adj_y in adjacent_positions:
                    if self.is_valid_position(adj_x, adj_y):
                        for entity in self.entities:
                            if (entity.is_alive and 
                                entity.type == EntityType.HUMAN and 
                                entity.position_x == adj_x and 
                                entity.position_y == adj_y):
                                entity.zombify()
                                self.statistics.record_transformation()
                                self.check_transformations(adj_x, adj_y)
    
    def get_nearby_entities(self, x, y):
        nearby = []
        with self.board_lock:
            for entity in self.entities:
                if entity.is_alive:
                    distance = abs(entity.position_x - x) + abs(entity.position_y - y)
                    if distance == 1:
                        nearby.append(entity)
        return nearby
    
    def register_escape(self):
        self.statistics.record_escape()
        self.check_win_condition()
    
    def check_win_condition(self):
        with self.board_lock:
            humans_alive = sum(1 for e in self.entities if e.is_alive and e.type == EntityType.HUMAN)
            zombies_alive = sum(1 for e in self.entities if e.is_alive and e.type == EntityType.ZOMBIE)
            
            if self.statistics.escapes > 0:
                self.end_game("HUMANS")
            elif humans_alive == 0:
                self.end_game("ZOMBIES")
    
    def end_game(self, winner):
        if self.game_ended:
            return
        
        self.game_ended = True
        self.winner = winner
        
        humans_alive = sum(1 for e in self.entities if e.is_alive and e.type == EntityType.HUMAN)
        zombies_alive = sum(1 for e in self.entities if e.is_alive and e.type == EntityType.ZOMBIE)
        
        self.statistics.set_final_counts(humans_alive, zombies_alive)
        
        self.logger.log(LogEvent.GAME_END, f"Game ended. Winner: {winner}")
        
        for entity in self.entities:
            entity.kill()
        
        if self.display:
            self.display.stop()
        
        time.sleep(0.5)
        
        if self.display:
            self.display.show()
            self.display.show_final_statistics()
        
        self.logger.close()
        
        for entity in self.entities:
            entity.join(timeout=1)
        
        for condition in self.position_conditions.values():
            with condition:
                condition.notify_all()