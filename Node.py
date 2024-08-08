import pygame
import numpy as np

RED = (255, 0, 110)
GREEN = (94, 232, 126)
BLUE = (58, 134, 255)
LIGHT_BLUE = (173, 232, 244)
YELLOW = (255, 190, 11)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (131, 56, 236)
ORANGE = (251, 86, 7)
GREY = (214, 214, 214)
TURQUOISE = (6, 214, 160)

colors = [RED, GREEN, BLUE, LIGHT_BLUE, YELLOW, PURPLE]

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.heat = LIGHT_BLUE
        self.neighbors = []
        self.width = width
        self.weight = 0
        self.total_rows = total_rows
        self.full = False
        self.path_count = 0
    
    def get_pos(self):
        return self.row, self.col
    
    def is_close(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_full(self):
        return self.full
    
    def reset(self):
        if self.color == BLACK:
            for n in self.neighbors:
                n.weight_decrease()
            self.weight = 0        
        self.color = WHITE

    def make_close(self):
        self.color = GREY
    
    def make_barrier(self):
        self.weight = 100
        self.color = BLACK
    
    def make_full(self):
        self.full = True
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self, color):
        self.color = color
        self.path_count += 1
        if(self.path_count > 2):
            self.make_full()
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y, self.width, self.width))
    
    def draw_heat(self, win):
        pygame.draw.rect(win, self.heat, (self.x,self.y, self.width, self.width))

    def obstacle_propagation(self):
        for n in self.neighbors:
            for i in range(2):
                n.weight_increase()
            for m in n.neighbors:
                m.weight_increase()
    
    def update_neighbors(self, grid):
        self.neighbors = []
        init_weight = self.weight
        
        #bellow
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier() and not grid[self.row + 1][self.col].is_full():
            self.neighbors.append(grid[self.row + 1][self.col])
        elif self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_barrier() and init_weight < 10:
            self.weight_increase()
        
        #above
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier() and not grid[self.row-1][self.col].is_full():
            self.neighbors.append(grid[self.row-1][self.col])
        elif self.row > 0 and grid[self.row-1][self.col].is_barrier() and init_weight < 10:
            self.weight_increase()

        #right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier() and not grid[self.row][self.col + 1].is_full():
            self.neighbors.append(grid[self.row][self.col + 1])
        elif self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_barrier() and init_weight < 10:
            self.weight_increase()

        #left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier() and not grid[self.row][self.col - 1].is_full():
            self.neighbors.append(grid[self.row][self.col - 1])
        elif self.col > 0 and grid[self.row][self.col - 1].is_barrier() and init_weight < 10:
            self.weight_increase()

    def weight_increase(self):
        self.weight += 15
        if self.weight >= 100:
            self.weight = 100
        f = 1 - self.weight/100
        
        base_color = np.array([173, 232, 244]) 
        scaled_color = base_color * f

        self.heat = tuple(scaled_color.astype(int))
    
    def weight_decrease(self):
        self.weight -= 15
        if self.weight <= 0 :
            self.weight = 0
        f = 1 - self.weight/100
        
        base_color = np.array([173, 232, 244]) 
        scaled_color = base_color * f

        self.heat = tuple(scaled_color.astype(int))

    def __lt__(self, other):
        return False