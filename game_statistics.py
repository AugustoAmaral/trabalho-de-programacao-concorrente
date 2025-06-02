import threading
import time
from collections import defaultdict

class GameStatistics:
    def __init__(self):
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.end_time = None
        
        self.total_moves = defaultdict(int)
        self.transformations = 0
        self.escapes = 0
        self.collisions = 0
        self.position_usage = defaultdict(int)
        self.human_survival_times = []
        self.move_times = []
        
        self.initial_humans = 0
        self.initial_zombies = 0
        self.final_humans = 0
        self.final_zombies = 0
        
    def record_move(self, entity_type, position):
        with self.lock:
            self.total_moves[entity_type] += 1
            self.position_usage[position] += 1
    
    def record_transformation(self):
        with self.lock:
            self.transformations += 1
    
    def record_escape(self):
        with self.lock:
            self.escapes += 1
    
    def record_collision(self):
        with self.lock:
            self.collisions += 1
    
    def record_human_death(self, survival_time):
        with self.lock:
            self.human_survival_times.append(survival_time)
    
    def record_move_time(self, move_time):
        with self.lock:
            self.move_times.append(move_time)
    
    def set_initial_counts(self, humans, zombies):
        with self.lock:
            self.initial_humans = humans
            self.initial_zombies = zombies
    
    def set_final_counts(self, humans, zombies):
        with self.lock:
            self.final_humans = humans
            self.final_zombies = zombies
            self.end_time = time.time()
    
    def get_statistics(self):
        with self.lock:
            total_time = (self.end_time or time.time()) - self.start_time
            avg_survival = sum(self.human_survival_times) / len(self.human_survival_times) if self.human_survival_times else 0
            avg_move_time = sum(self.move_times) / len(self.move_times) if self.move_times else 0
            
            most_used_positions = sorted(
                self.position_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            return {
                'total_time': total_time,
                'initial_humans': self.initial_humans,
                'initial_zombies': self.initial_zombies,
                'final_humans': self.final_humans,
                'final_zombies': self.final_zombies,
                'escapes': self.escapes,
                'transformations': self.transformations,
                'total_moves': dict(self.total_moves),
                'collisions': self.collisions,
                'avg_human_survival': avg_survival,
                'avg_move_time': avg_move_time,
                'most_used_positions': most_used_positions
            }