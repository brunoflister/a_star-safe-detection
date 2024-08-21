import Node
import random
import numpy as np

B_RATE = 0.05
N_COEF = 5

def g(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

class Grid:
    def __init__(self, row, width):
        self.row = row
        self.width = width
        self.gap = width // row
        self.obstacles = []
        self.danger = []
        self.grid = self.make_grid()
        
    def make_grid(self):
        grid = []
        for i in range(self.row):
            grid.append([])
            for j in range(self.row):
                node = Node.Node(i, j, self.gap, self.row)
                grid[i].append(node)
        return grid
    
    def random_barrier(self):
        for i in range(int(self.row*self.row*B_RATE)):
            x = random.randint(0, self.row - 1)
            y = random.randint(0, self.row - 1)
            node = self.grid[x][y]
            self.obstacles.append(node)
            node.make_barrier()
    
    def update_danger_deg(self):
        for row in self.grid:
            for node in row:
                node.deg = 0
                list = []
                for obs in self.obstacles:
                    if node != obs:
                        list.append(round(1 /(N_COEF*g(node.get_pos(), obs.get_pos()) + 1) * 100, 2))
                if list:
                    node.deg = max(list)
                node.color_heat()
    
    def reset_node(self, node):
        if node.is_barrier():
            self.obstacles.remove(node)
            self.update_danger_deg()
        node.reset()

    def reset_grid(self):
        self.grid = self.make_grid()
        self.obstacles.clear()
        self.danger.clear()