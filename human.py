import random
from entity import Entity, EntityType, EntityState

class Human(Entity):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y, EntityType.HUMAN)
        
    def calculate_next_movement(self):
        if self.actual_state != EntityState.MOVING or not self.is_alive:
            return None, None
        
        directions = []
        
        if self.game_board.human_movement_bias_enabled:
            bias = self.game_board.human_movement_bias
            if random.random() < bias:
                if self.position_x < self.game_board.board_size - 1:
                    return self.position_x + 1, self.position_y
        
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