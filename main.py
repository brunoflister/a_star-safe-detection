import pygame
import numpy as np
import random
from queue import PriorityQueue
import Node

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
B_RATE = 0.10
c_state = 0
pygame.display.set_caption("A* Path Finding Algorithm")
    
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, start, current, draw):
    global c_state
    # Check if all predefined colors have been used
    if c_state < len(Node.colors):
        color = Node.colors[c_state]
        c_state += 1
    else:
        color = list(np.random.choice(range(50, 200), size=3))
    
    while current in came_from:
        current = came_from[current]
        current.weight_increase()
        if(current != start):        
            current.make_path(color)
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:
            reconstruct_path(came_from, start, end, draw)
            end.make_end()
            return True        
        for neighbor in current.neighbors:
            if neighbor != start:
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) + current.weight
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
        draw()
        if current != start and current.color == Node.WHITE:
            current.make_close()    
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node.Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Node.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Node.GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(Node.WHITE)
    for row in grid:
        for node in row:
            node.draw(win)    
    draw_grid(win, rows, width)
    pygame.display.update()

def heatmap(win, grid, rows, width, start, end):
    win.fill(Node.WHITE)
    for row in grid:
        for node in row:
            if node.is_barrier() or node == start or node == end:
                node.draw(win)
            else:
                node.draw_heat(win)    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row, col

def random_barrier(grid,rows, width):
    gap = width // rows
    for i in range(int(rows*rows*B_RATE)):
        x = random.randint(0, width-1) // gap
        y = random.randint(0, width-1) // gap
        node = grid[x][y]
        node.make_barrier()

def up_neigh(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)      

#gameloop
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True
    heat = False
    random_barrier(grid, ROWS, width)
    up_neigh(grid)
    while run:
        if heat == True:
            heatmap(win, grid, ROWS, width, start, end)
        else:
            draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
                    up_neigh(grid)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_h:
                    heat = not heat
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    random_barrier(grid, ROWS, width)

    pygame.quit()

main(WIN, WIDTH)