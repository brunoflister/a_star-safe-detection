import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (127, 191, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,121,0)
GREY = (158,158,158)
TURQUOISE = (0, 255, 255)

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
    
    def reset(self):
        if self.color == BLACK:
            for n in self.neighbors:
                n.weight_decrease()
            self.weight = 0        
        self.color = WHITE

    def make_close(self):
        self.color = GREY
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.weight = 100
        self.color = BLACK
        #self.obstacle_propagation()        
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self, color):
        self.color = color
    
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
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        elif self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_barrier() and init_weight < 10:
            self.weight_increase()
        
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        elif self.row > 0 and grid[self.row-1][self.col].is_barrier() and init_weight < 10:
            self.weight_increase()

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        elif self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_barrier() and init_weight < 10:
            self.weight_increase()

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        elif self.col > 0 and grid[self.row][self.col - 1].is_barrier() and init_weight < 10:
            self.weight_increase()

    def weight_increase(self):
        self.weight += 10
        if self.weight >= 100:
            self.weight = 100
        f = 1 - self.weight/100
        self.heat = (127 * f, 191 * f, 63 + 192 * f)
    
    def weight_decrease(self):
        self.weight -= 10
        if self.weight <= 0 :
            self.weight = 0
        f = 1 - self.weight/100
        self.heat = (127 * f, 191 * f, 63 + 192 * f)

    def __lt__(self, other):
        return False