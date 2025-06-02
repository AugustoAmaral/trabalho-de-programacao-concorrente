import threading
import time
from datetime import datetime
from enum import Enum

class LogEvent(Enum):
    MOVE_EXECUTED = "MOVE_EXECUTED"
    MOVE_DISCARDED = "MOVE_DISCARDED"
    MOVE_WAITING = "MOVE_WAITING"
    TRANSFORMATION = "TRANSFORMATION"
    GAME_START = "GAME_START"
    GAME_END = "GAME_END"
    ESCAPE = "ESCAPE"
    ERROR = "ERROR"

class GameLogger:
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
            self.log_file = None
            self.file_lock = threading.Lock()
            self.initialized = True
    
    def initialize(self, log_file="game_log.txt"):
        with self.file_lock:
            self.log_file = log_file
            with open(self.log_file, 'w') as f:
                f.write(f"Game Log Started: {datetime.now()}\n")
                f.write("="*80 + "\n")
    
    def log(self, event_type, message, entity_id=None, entity_type=None):
        with self.file_lock:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = f"[{timestamp}] [{event_type.value}]"
            
            if entity_id is not None:
                log_entry += f" [Entity:{entity_id}]"
            if entity_type is not None:
                log_entry += f" [{entity_type}]"
            
            log_entry += f" {message}"
            
            if self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry + "\n")
            
            print(log_entry)
    
    def close(self):
        with self.file_lock:
            if self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write("="*80 + "\n")
                    f.write(f"Game Log Ended: {datetime.now()}\n")