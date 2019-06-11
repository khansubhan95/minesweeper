# Beginner version of minesweeper with 9x9 cells and 10 mines

import pygame, sys, random, time

pygame.init()
pygame.font.init()

SIZE = 9
MINES = 10
DIMENSION = 40

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 129, 0)
BLUE = (55, 0, 253)
BACKGROUND_COLOR = (115, 115, 115)
CELL_COLOR = (164, 164, 164)

ROWS = SIZE
COLUMNS = SIZE
WIDTH = DIMENSION
HEIGHT = DIMENSION

CELL_SIZE = [WIDTH, HEIGHT]
WINDOW_SIZE= [COLUMNS * WIDTH, (ROWS * HEIGHT) + DIMENSION]

class Cell:
    def __init__(self):
        self.value = 0
        self.state = False
        self.visibility = False
        self.flag = False
        self.image_name = 'images/facing_down.png'

    def __str__(self):
        return self.value

    def set_value(self, v):
        self.value = v

    def get_value(self):
        return self.value

    def set_state(self, s):
        self.state = s

    def get_state(self):
        return self.state

    def set_visibility(self, v):
        self.visibility = v

    def get_visibility(self):
        return self.visibility

    def set_flag(self, f):
        self.flag = f

    def get_flag(self):
        return self.flag

    def set_image_name(self, i):
        self.image_name = i

    def get_image_name(self):
        return self.image_name

    def has_mine(self):
        return self.value == -1

def print_array(arr):
    for element in arr:
        print(element)

def find_valid_indices(i, j):
    temp = []
    temp.extend([[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1], [i - 1, j - 1], [i - 1, j + 1], [i + 1, j - 1], [i + 1, j + 1]])
    valid = []
    for t in temp:
        if -1 in t:
            continue
        elif COLUMNS in t:
            continue
        else:
            valid.append(t)
    return valid

def find_adjacent(cells, i, j):
    if cells[i][j].has_mine():
        return -1

    valid_indices = find_valid_indices(i, j)
    count = 0

    for index in valid_indices:
        count += (cells[index[0]][index[1]].has_mine())
    return count

def find_image_name_by_value(i):
    if i == -1:
        return 'images/mine.png'
    else:
        return 'images/' + str(i) + '.png'

def find_neighbours(cells, i, j):
    temp = []
    answer = []
    temp.append([i, j])
    while len(temp) != 0:
        element = temp[0]
        if cells[element[0]][element[1]].get_value() == 0:
            valid_indices = find_valid_indices(element[0], element[1])
            for index in valid_indices:
                if index not in temp and index not in answer:
                    temp.append(index)
        head = temp.pop(0)
        if head not in answer:
            answer.append(head)
    return answer

# Load the surface
# surface = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

mine_positions = []
cells = [[Cell() for i in range(COLUMNS)] for j in range(ROWS)]

mines_left = MINES
mines_detected = []

game_over = False

font = pygame.font.SysFont('Arial', 30)
text_surface = font.render(str(mines_left), False, BLACK)

while len(mine_positions) < MINES:
    x_coord = random.randint(0, COLUMNS - 1)
    y_coord = random.randint(0, ROWS - 1)
    if [x_coord, y_coord] not in mine_positions:
        mine_positions.append([x_coord, y_coord])       
        cells[x_coord][y_coord].set_value(-1)

# print(mine_positions)

for i in range(ROWS):
    for j in range(COLUMNS):
        cells[i][j].set_value(find_adjacent(cells, i, j))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    surface.fill(WHITE)

    if pygame.mouse.get_pressed()[0]:
        x_coord, y_coord = int(pygame.mouse.get_pos()[1] / DIMENSION), int(pygame.mouse.get_pos()[0] / DIMENSION)
        if y_coord==0 and x_coord * DIMENSION == ROWS*HEIGHT:
            sys.exit()
        if x_coord * DIMENSION < ROWS * HEIGHT: 
            cells[x_coord][y_coord].set_visibility(True)
            cells[x_coord][y_coord].set_image_name(find_image_name_by_value(cells[x_coord][y_coord].get_value()))

            if(cells[x_coord][y_coord].has_mine()):
                text_surface = font.render('You Lost :(', False, BLACK)
                game_over = True
                for i in range(ROWS):
                    for j in range(COLUMNS):
                        cells[i][j].set_visibility(True)
                        cells[i][j].set_image_name(find_image_name_by_value(cells[i][j].get_value()))               


            if(cells[x_coord][y_coord].get_value() == 0):
                neighbours = find_neighbours(cells, x_coord, y_coord)
                for neighbour in neighbours:
                    cells[neighbour[0]][neighbour[1]].set_visibility(True)
                    cells[neighbour[0]][neighbour[1]].set_image_name(find_image_name_by_value(cells[neighbour[0]][neighbour[1]].get_value()))

    if pygame.mouse.get_pressed()[2]:
        x_coord, y_coord = int((pygame.mouse.get_pos()[1]) / DIMENSION), int(pygame.mouse.get_pos()[0] / DIMENSION)
        time.sleep(0.1)
        if cells[x_coord][y_coord].get_flag():
            cells[x_coord][y_coord].set_flag(False)
            cells[x_coord][y_coord].set_image_name('images/facing_down.png')
        else:
            cells[x_coord][y_coord].set_flag(True)
            cells[x_coord][y_coord].set_image_name('images/flag.png')

    if not game_over:
        for i in range(ROWS):
            for j in range(COLUMNS):
                    if cells[i][j].get_flag():
                        if [i, j] not in mines_detected:
                            mines_detected.append([i, j])
                            mines_left = MINES - len(mines_detected)
                    else:
                        if [i, j] in mines_detected:
                            mines_detected.remove([i, j])
                            mines_left += 1
                    text_surface = font.render(str(mines_left), False, BLACK)

    if mines_left == 0:
        mine_positions.sort(key = lambda x: (x[0], x[1]))
        mines_detected.sort(key = lambda x: (x[0], x[1]))
        message = ''
        if mine_positions == mines_detected:
            message = 'You Won :)'
            for i in range(ROWS):
                for j in range(COLUMNS):
                    if not cells[i][j].get_flag():
                            cells[i][j].set_visibility(True)
                            cells[i][j].set_image_name(find_image_name_by_value(cells[i][j].get_value()))
        else:
            message = 'You Lost :('
        game_over = True
        text_surface = font.render(message, False, BLACK)

    for i in range(ROWS):
        for j in range(COLUMNS):
            cell_down = pygame.transform.scale(pygame.image.load(cells[i][j].get_image_name()), CELL_SIZE)
            cell_down_rect = cell_down.get_rect()
            cell_down_rect.x = j * WIDTH
            cell_down_rect.y = i * HEIGHT
            surface.blit(cell_down, cell_down_rect)

            text_surface_rect = text_surface.get_rect()
            text_surface_rect.center = (COLUMNS*WIDTH/2, ROWS*HEIGHT + (HEIGHT/2))
            surface.blit(text_surface, text_surface_rect)

            exit_sign = font.render('X', False, RED)
            exit_sign_rect = exit_sign.get_rect()
            exit_sign_rect.center = (WIDTH/2, ROWS*HEIGHT + (HEIGHT/2))
            surface.blit(exit_sign, exit_sign_rect)

    pygame.display.update()
