import random
import math
from entity import Entity, EntityType, EntityState

class Zombie(Entity):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y, EntityType.ZOMBIE)
        
    def calculate_next_movement(self):
        if self.actual_state != EntityState.MOVING or not self.is_alive:
            return None, None
        
        strategy = self.game_board.zombie_movement_strategy
        
        if strategy == "ALEATORIO":
            return self._random_movement()
        elif strategy == "PERSEGUICAO":
            return self._persecution_movement()
        elif strategy == "BLOQUEIO":
            return self._blocking_movement()
        else:
            return self._random_movement()
    
    def _random_movement(self):
        directions = []
        
        if self.position_x > 0:
            directions.append((self.position_x - 1, self.position_y))
        if self.position_x < self.game_board.board_size - 1:
            directions.append((self.position_x + 1, self.position_y))
        if self.position_y > 0:
            directions.append((self.position_x, self.position_y - 1))
        if self.position_y < self.game_board.board_size - 1:
            directions.append((self.position_x, self.position_y + 1))
        
        if directions:
            return random.choice(directions)
        
        return None, None
    
    def _persecution_movement(self):
        nearest_human = self._find_nearest_human()
        
        if nearest_human is None:
            return self._random_movement()
        
        human_x, human_y = nearest_human
        dx = human_x - self.position_x
        dy = human_y - self.position_y
        
        moves = []
        
        if dx > 0 and self.position_x < self.game_board.board_size - 1:
            moves.append((self.position_x + 1, self.position_y))
        elif dx < 0 and self.position_x > 0:
            moves.append((self.position_x - 1, self.position_y))
        
        if dy > 0 and self.position_y < self.game_board.board_size - 1:
            moves.append((self.position_x, self.position_y + 1))
        elif dy < 0 and self.position_y > 0:
            moves.append((self.position_x, self.position_y - 1))
        
        if moves:
            return random.choice(moves)
        
        return self._random_movement()
    
    def _blocking_movement(self):
        humans = self._find_humans_in_range()
        
        if not humans:
            return self._random_movement()
        
        best_move = None
        best_score = -1
        
        possible_moves = []
        if self.position_x > 0:
            possible_moves.append((self.position_x - 1, self.position_y))
        if self.position_x < self.game_board.board_size - 1:
            possible_moves.append((self.position_x + 1, self.position_y))
        if self.position_y > 0:
            possible_moves.append((self.position_x, self.position_y - 1))
        if self.position_y < self.game_board.board_size - 1:
            possible_moves.append((self.position_x, self.position_y + 1))
        
        for move in possible_moves:
            score = 0
            for human_x, human_y in humans:
                if move[0] > human_x:
                    score += 1
            if score > best_score:
                best_score = score
                best_move = move
        
        if best_move:
            return best_move
        
        return self._random_movement()
    
    def _find_nearest_human(self):
        min_distance = float('inf')
        nearest = None
        
        for entity in self.game_board.entities:
            if entity.type == EntityType.HUMAN and entity.is_alive:
                distance = abs(entity.position_x - self.position_x) + abs(entity.position_y - self.position_y)
                if distance <= self.game_board.zombie_persecution_range and distance < min_distance:
                    min_distance = distance
                    nearest = (entity.position_x, entity.position_y)
        
        return nearest
    
    def _find_humans_in_range(self):
        humans = []
        
        for entity in self.game_board.entities:
            if entity.type == EntityType.HUMAN and entity.is_alive:
                distance = abs(entity.position_x - self.position_x) + abs(entity.position_y - self.position_y)
                if distance <= self.game_board.zombie_persecution_range:
                    humans.append((entity.position_x, entity.position_y))
        
        return humans