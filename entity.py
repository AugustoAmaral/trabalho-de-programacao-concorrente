import threading
import time
import random
from abc import ABC, abstractmethod
from enum import Enum

class EntityType(Enum):
    HUMAN = "HUMAN"
    ZOMBIE = "ZOMBIE"

class EntityState(Enum):
    MOVING = "MOVING"
    WAITING = "WAITING"
    TRANSFORMING = "TRANSFORMING"
    ESCAPED = "ESCAPED"
    DEAD = "DEAD"

class Entity(ABC, threading.Thread):
    _id_counter = 0
    _id_lock = threading.Lock()
    
    def __init__(self, position_x, position_y, entity_type):
        super().__init__()
        with Entity._id_lock:
            self.id = Entity._id_counter
            Entity._id_counter += 1
        
        self.position_x = position_x
        self.position_y = position_y
        self.type = entity_type
        self.is_alive = True
        self.actual_state = EntityState.MOVING
        self.game_board = None
        self.daemon = True
        
    def set_game_board(self, game_board):
        self.game_board = game_board
    
    def run(self):
        from game_logger import GameLogger, LogEvent
        logger = GameLogger()
        
        while self.is_alive and not self.game_board.game_ended:
            try:
                if self.actual_state == EntityState.DEAD or self.actual_state == EntityState.ESCAPED:
                    break
                
                cooldown = random.uniform(
                    self.game_board.cooldown_min,
                    self.game_board.cooldown_max
                )
                time.sleep(cooldown)
                
                if not self.is_alive or self.game_board.game_ended:
                    break
                
                next_x, next_y = self.calculate_next_movement()
                
                if next_x is not None and next_y is not None:
                    self.move(next_x, next_y)
                
            except Exception as e:
                logger.log(LogEvent.ERROR, f"Error in entity thread: {e}", self.id, self.type.value)
                break
    
    @abstractmethod
    def calculate_next_movement(self):
        pass
    
    def move(self, new_x, new_y):
        from game_logger import GameLogger, LogEvent
        logger = GameLogger()
        
        if not self.game_board.is_valid_position(new_x, new_y):
            logger.log(
                LogEvent.MOVE_DISCARDED,
                f"Movement out of bounds: ({self.position_x},{self.position_y}) -> ({new_x},{new_y})",
                self.id,
                self.type.value
            )
            return False
        
        success = self.game_board.move_entity(self, new_x, new_y)
        
        if success:
            logger.log(
                LogEvent.MOVE_EXECUTED,
                f"Movement executed: ({self.position_x},{self.position_y}) -> ({new_x},{new_y})",
                self.id,
                self.type.value
            )
            self.position_x = new_x
            self.position_y = new_y
            
            if self.type == EntityType.HUMAN and new_x == self.game_board.board_size - 1:
                self.escape()
        
        return success
    
    def zombify(self):
        from game_logger import GameLogger, LogEvent
        logger = GameLogger()
        
        self.actual_state = EntityState.TRANSFORMING
        logger.log(
            LogEvent.TRANSFORMATION,
            f"Human transformed at position ({self.position_x},{self.position_y})",
            self.id,
            "HUMAN->ZOMBIE"
        )
        self.type = EntityType.ZOMBIE
        self.actual_state = EntityState.MOVING
    
    def escape(self):
        from game_logger import GameLogger, LogEvent
        logger = GameLogger()
        
        self.actual_state = EntityState.ESCAPED
        logger.log(
            LogEvent.ESCAPE,
            f"Human escaped at position ({self.position_x},{self.position_y})",
            self.id,
            self.type.value
        )
        self.kill()
        self.game_board.register_escape()
    
    def kill(self):
        self.is_alive = False
        self.actual_state = EntityState.DEAD
    
    def get_position(self):
        return (self.position_x, self.position_y)