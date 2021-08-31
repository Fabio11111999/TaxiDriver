import pygame
import constants
import numpy as np
import ast 


def load_map(map_path):
    with open(map_path) as f:
        city = f.readlines()
    for i in range(len(city) - 1):
        city[i] = city[i][0 : -1]
    return city

def show_city(city, moves):
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    rows, cols = len(city), len(city[0])
    block_width, block_height = round(constants.SCREEN_WIDTH / cols) - 1, round(constants.SCREEN_HEIGHT / rows) - 1
    row = [pygame.Rect(1, 1, 1, 1) for i in range(cols)]
    mat = [list(row) for i in range(rows)]
    t_x, t_y, a_x, a_y, b_x, b_y = 0, 0, 0, 0, 0, 0
    for i in range(rows):
        for j in range(cols):
            x, y = i * (block_height + 1), j * (block_width + 1)
            mat[i][j] = pygame.Rect(x, y, block_width, block_height)
            if city[i][j] == '.':
                color = constants.WHITE
            if city[i][j] == '#':
                color = constants.GREY
            if city[i][j] == 'A':
                color = constants.GREEN
                a_x, a_y = i, j
            if city[i][j] == 'B':
                color = constants.RED
                b_x, b_y = i, j
            if city[i][j] == 'T':
                color = constants.BLUE
                t_x, t_y = i, j
            pygame.draw.rect(surface = screen, color = color, rect = mat[i][j])
    pygame.display.flip()
    pygame.time.wait(1000)
    for move in moves:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.draw.rect(surface = screen, color = constants.SKYBLUE, rect = mat[t_x][t_y])
        t_x, t_y = move[0], move[1]
        pygame.draw.rect(surface = screen, color = constants.BLUE, rect = mat[t_x][t_y])
        pygame.time.wait(10)
        pygame.display.update()
    
    
def main():
    map_path = 'maps/map3/'
    city = load_map(map_path + 'map.txt')
    with open(map_path + 'moves.txt') as f:
        moves = ast.literal_eval(f.read()) 
    with open(map_path + 'best.txt') as f:
        best, index = [int(x) for x in next(f).split()]
    show_city(city, moves[100])

    
if __name__ == '__main__':
    main()
