import pygame as pg
import numpy as np

class MapaNode:
    def __init__(self, position, parent=None):
        self.parent = parent
        self.position = position
    
    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

class deepSearch(object):
    def run(self, mapa, start, end):
        mapa = mapa.astype(float)
        startNode = MapaNode(start)
        endNode = MapaNode(end)
        path = []
        pila = [startNode]
        mapaRows, mapaCols = np.shape(mapa)
        visited = np.zeros(mapa.shape)
        while len(pila) != 0:
            currentNode = pila.pop(0)
            if currentNode == endNode:
                break
            
            movements = [
                [0, -1],
                [-1, 0],
                [1, 0],
                [0, 1]
            ]
            
            for movement in movements:
                newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
                if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[1] >= mapaCols or newPosition[0] >= mapaRows:
                    continue
                elif visited[newPosition[0]][newPosition[1]] == 1:
                    continue
                elif mapa[newPosition[0]][newPosition[1]] == 0:
                    continue
                else:
                    adjacentNode = MapaNode(newPosition, currentNode)
                    pila.append(adjacentNode)
                    visited[newPosition[0]][newPosition[1]] = 1
        
        while currentNode is not None:
            path.append(currentNode.position)
            currentNode = currentNode.parent
        return path[::-1], visited

class breadthSearch(object):
    def run(self, mapa, start, end):
        mapa = mapa.astype(float)
        startNode = MapaNode(start)
        endNode = MapaNode(end)
        path = []
        queue = [startNode]
        mapaRows, mapaCols = np.shape(mapa)
        visited = np.zeros(mapa.shape)
        visited[startNode.position[0]][startNode.position[1]] = 1
        while len(queue) != 0:
            currentNode = queue.pop(0)
            if currentNode == endNode:
                break
            
            movements = [
                [0, -1],
                [-1, 0],
                [1, 0],
                [0, 1]
            ]
            
            for movement in movements:
                newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
                if newPosition[0] < 0 or newPosition[1] < 0 or newPosition[1] >= mapaCols or newPosition[0] >= mapaRows:
                    continue
                elif visited[newPosition[0]][newPosition[1]] == 1:
                    continue
                elif mapa[newPosition[0]][newPosition[1]] == 0:
                    continue
                else:
                    adjacentNode = MapaNode(newPosition, currentNode)
                    queue.append(adjacentNode)
                    visited[newPosition[0]][newPosition[1]] = 1
        
        while currentNode is not None:
            path.append(currentNode.position)
            currentNode = currentNode.parent
        return path[::-1], visited

class iterativeDeepeningSearch(object):
    def dfs_with_depth_limit(self, mapa, start, end, depth_limit):
        startNode = MapaNode(start)
        endNode = MapaNode(end)
        stack = [(startNode, 0)]
        visited = set()
        mapaRows, mapaCols = np.shape(mapa)

        while stack:
            currentNode, depth = stack.pop()
            if currentNode == endNode:
                path = []
                while currentNode:
                    path.append(currentNode.position)
                    currentNode = currentNode.parent
                return path[::-1], visited

            if depth < depth_limit:
                if tuple(currentNode.position) not in visited:
                    visited.add(tuple(currentNode.position))
                    movements = [[0, -1], [-1, 0], [1, 0], [0, 1]]
                    for movement in movements:
                        newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
                        if (0 <= newPosition[0] < mapaRows and 0 <= newPosition[1] < mapaCols and
                            mapa[newPosition[0]][newPosition[1]] != 0):
                            adjacentNode = MapaNode(newPosition, currentNode)
                            stack.append((adjacentNode, depth + 1))

        return None, visited

    def run(self, mapa, start, end):
        mapa = mapa.astype(float)
        max_depth = max(mapa.shape)
        for depth in range(max_depth):
            path, visited = self.dfs_with_depth_limit(mapa, start, end, depth)
            if path:
                return path, visited
        return [], set()  # Path not found

pg.init()
mapaAlg = np.load('mapaProfundidad.npy')
width, height = mapaAlg.shape

BLACK = pg.Color('black')
WHITE = pg.Color('white')
GREEN = pg.Color('green')
RED = pg.Color('red')
BLUE = pg.Color('blue')

color_light = (170,170,170)
color_dark = (100,100,100)
smallfont = pg.font.SysFont('comicsans', 30)
textDFS = smallfont.render('DFS' , True , RED)
textBFS = smallfont.render('BFS' , True , RED)
textIDDFS = smallfont.render('IDDFS' , True , RED)
textReset = smallfont.render('Reset' , True , RED)

tile_size = 10
start = [20, 2]
goal = [40, 45]
topPadding = 50

searchDFS = deepSearch()
searchBFS = breadthSearch()
searchIDDFS = iterativeDeepeningSearch()

screen = pg.display.set_mode((width*tile_size, height*tile_size+topPadding))
clock = pg.time.Clock()

background = pg.Surface((width*tile_size, height*tile_size))
buttons = pg.Surface((width*tile_size, 50))

def draw_map():
    for y in range(0, height):
        for x in range(0, width):
            rect = (x*tile_size, y*tile_size, tile_size, tile_size)
            if mapaAlg[y, x] == 0:
                color = BLACK
            else:
                color = WHITE
            if x == start[1] and y == start[0]:
                color = GREEN
            if x == goal[1] and y == goal[0]:
                color = RED
            pg.draw.rect(background, color, rect)

def draw_path(path):
    for i in range(len(path) - 1):
        start_pos = (path[i][1] * tile_size + tile_size // 2, path[i][0] * tile_size + tile_size // 2)
        end_pos = (path[i+1][1] * tile_size + tile_size // 2, path[i+1][0] * tile_size + tile_size // 2)
        pg.draw.line(background, BLUE, start_pos, end_pos, 2)

draw_map()

game_exit = False
selected_algorithm = None

while not game_exit:
    mouse = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_exit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40:
                selected_algorithm = 'DFS'
            if 160 <= mouse[0] <= 300 and 10 <= mouse[1] <= 40:
                selected_algorithm = 'BFS'
            if 310 <= mouse[0] <= 450 and 10 <= mouse[1] <= 40:
                selected_algorithm = 'IDDFS'
            if 460 <= mouse[0] <= 600 and 10 <= mouse[1] <= 40:
                draw_map()
                selected_algorithm = None
            
            if selected_algorithm:
                draw_map()  # Reset the map before drawing new path
                if selected_algorithm == 'DFS':
                    camino, mapavisited = searchDFS.run(mapaAlg, start, goal)
                elif selected_algorithm == 'BFS':
                    camino, mapavisited = searchBFS.run(mapaAlg, start, goal)
                elif selected_algorithm == 'IDDFS':
                    camino, mapavisited = searchIDDFS.run(mapaAlg, start, goal)
                
                if camino:
                    draw_path(camino)
    
    # Update button colors
    pg.draw.rect(buttons, color_light if 10 <= mouse[0] <= 150 and 10 <= mouse[1] <= 40 else color_dark, [10, 10, 140, 30])
    pg.draw.rect(buttons, color_light if 160 <= mouse[0] <= 300 and 10 <= mouse[1] <= 40 else color_dark, [160, 10, 140, 30])
    pg.draw.rect(buttons, color_light if 310 <= mouse[0] <= 450 and 10 <= mouse[1] <= 40 else color_dark, [310, 10, 140, 30])
    pg.draw.rect(buttons, color_light if 460 <= mouse[0] <= 600 and 10 <= mouse[1] <= 40 else color_dark, [460, 10, 140, 30])

    screen.fill((0, 0, 0))
    screen.blit(buttons, (0, 0))
    screen.blit(background, (0, 50))
    screen.blit(textDFS, (10, 10))
    screen.blit(textBFS, (160, 10))
    screen.blit(textIDDFS, (310, 10))
    screen.blit(textReset, (460, 10))
    pg.display.flip()
    clock.tick(30)

pg.display.quit()