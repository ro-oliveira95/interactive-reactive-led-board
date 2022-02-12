from __future__ import print_function
from __future__ import division
import pygame
import numpy as np
import config
import espControl as led
import random
 
matrixR = np.zeros([8, 32])
matrixG = np.zeros([8, 32])
matrixB = np.zeros([8, 32])

def map8x32to1x256(data):
  output = []
  for j in range(len(data[0])-1, -1, -1):
    if j%2==0:
      rg = range(len(data))
    else:
      rg = range(len(data)-1, -1, -1)

    for i in rg:
      output.append(data[i][j])

  return output

def generateRandomFood():
  foodx = round(random.randrange(0, window_size[0] - block_size) / block_size) * block_size
  foody = round(random.randrange(0, window_size[1] - block_size) / block_size) * block_size
  return [foodx, foody]

def render_snake(snake_list):
  for coord in snake_list:
    pygame.draw.rect(dis, black, [coord[0], coord[1], block_size, block_size])

def getCordinates(pos):
  column = pos[0] // (block_size)
  row = pos[1] // (block_size)
  return [int(row), int(column)]

def resetGrid(grid):
  grid = {'r': np.zeros((8,32)),\
          'g': np.zeros((8,32)),\
          'b': np.zeros((8,32))}
  return grid

def updateLeds(grid):
  matrixR = np.interp(grid['r'], [0,1], [0,120])
  matrixG = np.interp(grid['g'], [0,1], [0,120])
  matrixB = np.interp(grid['b'], [0,1], [0,120])
  led.pixels = [map8x32to1x256(matrixR), map8x32to1x256(matrixG), map8x32to1x256(matrixB)]
  led.update()

def initGameVariables():
  global x1, y1, x1_change, y1_change, direction, snake_List, len_snake
  x1 = x1_init
  y1 = y1_init
  x1_change = 0       
  y1_change = 0
  direction = 'none'
  snake_List = []
  len_snake = 1

grid = {'r': np.zeros((8,32)),\
        'g': np.zeros((8,32)),\
        'b': np.zeros((8,32))}

pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0,255, 0)
 
block_size = 30
fps = 20

x1_init = 15*block_size
y1_init = 4*block_size
 

board_grid = (32, 8) # x, y
window_size = (board_grid[0]*block_size, board_grid[1]*block_size)

dis = pygame.display.set_mode(window_size)
pygame.display.set_caption('LED Snake Game')
 
game_over = False
game_close = False


clock = pygame.time.Clock()

initGameVariables()

food_pos = generateRandomFood()

while not game_over:

  while game_close: 
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          initGameVariables()
          grid = resetGrid(grid)
          render_snake([(x1, y1)])
          game_close = False

    pygame.display.update()


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        game_over = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT and direction != 'right':
            x1_change = -block_size
            y1_change = 0
            direction = 'left'
        elif event.key == pygame.K_RIGHT and direction != 'left':
            x1_change = block_size
            y1_change = 0
            direction = 'right'
        elif event.key == pygame.K_UP and direction != 'down':
            y1_change = -block_size
            x1_change = 0
            direction = 'up'
        elif event.key == pygame.K_DOWN and direction != 'up':
            y1_change = block_size
            x1_change = 0
            direction = 'down'

  grid = resetGrid(grid)


  x1 += x1_change
  y1 += y1_change

  if (x1 < 0 and direction == 'left'):
    x1 = window_size[0] - block_size
  elif (x1 >= window_size[0] and direction == 'right'):
    x1 = 0

  if (y1 < 0 and direction == 'up'):
    y1 = window_size[1] - block_size
  elif (y1 >= window_size[1] and direction == 'down'):
    y1 = 0

  dis.fill(white)
  pygame.draw.rect(dis, green, [food_pos[0], food_pos[1], block_size, block_size])
  
  # toggle food positions in grid
  food_coord = getCordinates(food_pos)
  grid['g'][food_coord[0]][food_coord[1]] = 1
  #print(food_pos)
  snake_Head = []
  snake_Head.append(x1)
  snake_Head.append(y1)
  snake_List.append(snake_Head)
  if len(snake_List) > len_snake:
    del snake_List[0]
  render_snake(snake_List)

  for i, part in enumerate(snake_List):
    # toggle snake positions in grid
    coord = getCordinates(part)
    grid['r'][coord[0]][coord[1]] = 1

    if (i < len(snake_List)-1 and (x1 == part[0] and y1 == part[1])):
      game_close = True
      print('hit?')
      grid['b'][coord[0]][coord[1]] = 1
      updateLeds(grid)
      continue

  if (x1 == food_pos[0] and y1 == food_pos[1]):
    # grid
    food_pos = generateRandomFood()
    len_snake += 1
    # board
    # food_coord = getCordinates(food_pos)

  
  # pygame.draw.rect(dis, black, [x1, y1, block_size, block_size])
  pygame.display.update()

  updateLeds(grid)

  clock.tick(fps)
 
pygame.quit()
quit()