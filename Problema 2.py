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
            currentNode = pila.pop()  # Cambiado de pop(0) a pop() para DFS
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
                movements = [[0, -1], [-1, 0], [1, 0], [0, 1]]
                for movement in movements:
                    newPosition = [currentNode.position[0] + movement[0], currentNode.position[1] + movement[1]]
                    if (0 <= newPosition[0] < mapaRows and 0 <= newPosition[1] < mapaCols and
                        mapa[newPosition[0]][newPosition[1]] != 0 and tuple(newPosition) not in visited):
                        adjacentNode = MapaNode(newPosition, currentNode)
                        stack.append((adjacentNode, depth + 1))
                        visited.add(tuple(newPosition))

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

# Colores
BLACK = pg.Color('black')
WHITE = pg.Color('white')
GREEN = pg.Color(0, 200, 0)  # Verde más brillante
RED = pg.Color(200, 0, 0)    # Rojo más brillante
BLUE = pg.Color(0, 100, 255) # Azul más brillante
GRAY = pg.Color(200, 200, 200)
DARK_GRAY = pg.Color(100, 100, 100)

# Fuentes
pg.font.init()
font = pg.font.Font(None, 30)

# Configuración de la pantalla
TILE_SIZE = 12
TOP_PADDING = 50
SCREEN_WIDTH = width * TILE_SIZE
SCREEN_HEIGHT = height * TILE_SIZE + TOP_PADDING
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Laberinto con Algoritmos de Búsqueda")

# Posiciones iniciales
start = [20, 2]
goal = [40, 45]

# Inicialización de algoritmos
searchDFS = deepSearch()
searchBFS = breadthSearch()
searchIDDFS = iterativeDeepeningSearch()

def draw_map():
    for y in range(height):
        for x in range(width):
            rect = pg.Rect(x * TILE_SIZE, y * TILE_SIZE + TOP_PADDING, TILE_SIZE, TILE_SIZE)
            if mapaAlg[y, x] == 0:
                pg.draw.rect(screen, BLACK, rect)
            else:
                pg.draw.rect(screen, WHITE, rect)
            # Dibuja un borde gris para cada celda
            pg.draw.rect(screen, GRAY, rect, 1)

    # Dibujar inicio y fin con formas más atractivas
    start_center = ((start[1] + 0.5) * TILE_SIZE, (start[0] + 0.5) * TILE_SIZE + TOP_PADDING)
    goal_center = ((goal[1] + 0.5) * TILE_SIZE, (goal[0] + 0.5) * TILE_SIZE + TOP_PADDING)
    pg.draw.circle(screen, GREEN, start_center, TILE_SIZE // 2)
    pg.draw.polygon(screen, RED, [
        (goal_center[0], goal_center[1] - TILE_SIZE // 2),
        (goal_center[0] - TILE_SIZE // 2, goal_center[1] + TILE_SIZE // 2),
        (goal_center[0] + TILE_SIZE // 2, goal_center[1] + TILE_SIZE // 2)
    ])

def draw_path(path):
    if path:
        # Dibuja un camino más suave y atractivo
        points = [(p[1] * TILE_SIZE + TILE_SIZE // 2, p[0] * TILE_SIZE + TILE_SIZE // 2 + TOP_PADDING) for p in path]
        pg.draw.lines(screen, BLUE, False, points, 4)
        
        # Dibuja círculos en los puntos de giro para un efecto más suave
        for point in points:
            pg.draw.circle(screen, BLUE, point, 3)

def draw_button(text, x, y, w, h, color, text_color):
    button_rect = pg.Rect(x, y, w, h)
    pg.draw.rect(screen, color, button_rect)
    pg.draw.rect(screen, BLACK, button_rect, 2)  # Borde del botón
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def main():
    clock = pg.time.Clock()
    running = True
    current_path = []

    while running:
        screen.fill(WHITE)
        
        # Dibujar botones
        dfs_button = draw_button("DFS", 10, 10, 100, 30, DARK_GRAY, WHITE)
        bfs_button = draw_button("BFS", 120, 10, 100, 30, DARK_GRAY, WHITE)
        iddfs_button = draw_button("IDDFS", 230, 10, 100, 30, DARK_GRAY, WHITE)
        reset_button = draw_button("Reset", 340, 10, 100, 30, DARK_GRAY, WHITE)

        draw_map()
        draw_path(current_path)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if dfs_button.collidepoint(mouse_pos):
                    current_path, _ = searchDFS.run(mapaAlg, start, goal)
                elif bfs_button.collidepoint(mouse_pos):
                    current_path, _ = searchBFS.run(mapaAlg, start, goal)
                elif iddfs_button.collidepoint(mouse_pos):
                    current_path, _ = searchIDDFS.run(mapaAlg, start, goal)
                elif reset_button.collidepoint(mouse_pos):
                    current_path = []

        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == "__main__":
    main()