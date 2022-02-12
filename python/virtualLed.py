"""
 Example program to show using an array to back a self.grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
from __future__ import print_function
from __future__ import division
import pygame
from pygame import Color
import numpy as np
import config
import espControl as led
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
RED = (255, 0, 0)
 
# This sets the WIDTH and HEIGHT of each self.grid location
WIDTH = 30
HEIGHT = 30

RADIUS_CIRCLE = WIDTH/2
 
# This sets the margin between each cell
MARGIN = 5
 


class VirtualLedTable(object):
  def __init__(self):
    self.grid = []
    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    for row in range(8):
        # Add an empty array that will hold each cell
        # in this row
        self.grid.append([])
        for column in range(32):
            self.grid[row].append(0)  # Append a cell
    
    
    # Initialize pygame
    pygame.init()
    
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [1130, 290]
    self.screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")
    
    # Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    matrixR = np.zeros([8, 32])
    matrixG = np.zeros([8, 32])
    matrixB = np.zeros([8, 32])

    # -------- Main Program Loop -----------
    # while not done:
    #   for event in pygame.event.get():  # User did something
    #       if event.type == pygame.QUIT:  # If user clicked close
    #           done = True  # Flag that we are done so we exit this loop
    #       elif event.type == pygame.MOUSEBUTTONDOWN:
    #           # User clicks the mouse. Get the position
    #           pos = pygame.mouse.get_pos()
    #           # Change the x/y screen coordinates to self.grid coordinates
    #           column = pos[0] // (WIDTH + MARGIN)
    #           row = pos[1] // (HEIGHT + MARGIN)
    #           # Set that location to one
    #           if (pygame.mouse.get_pressed()[0]):
    #             self.grid[row][column] = 1
    #             # print("Click mouse left ", pos, "Grid coordinates: ", row, column)
    #           elif (pygame.mouse.get_pressed()[2]):
    #             self.grid[row][column] = 0
    #             # print("Click mouse right ", pos, "Grid coordinates: ", row, column)
  
    #   # Set the screen background
    #   screen.fill(BLACK)

    #   drawing_coord_list = []

    #   # Draw the self.grid
    #   for row in range(8):
    #       for column in range(32):
    #           color = WHITE
    #           if self.grid[row][column] == 1:
    #             drawing_coord_list.append((row, column))
    #             color = BLUE
    #           pygame.draw.rect(screen,
    #                           color,
    #                           [(MARGIN + WIDTH) * column + MARGIN,
    #                             (MARGIN + HEIGHT) * row + MARGIN,
    #                             WIDTH,
    #                             HEIGHT])

    #   # print('------------\n',drawing_coord_list,'\n\n')

    #   # print(self.grid,'\n\n')

    #   matrixR = np.interp(self.grid, [0,1], [0,120])
    #   matrixB = np.interp(self.grid, [0,1], [0,120])
      
    #   # led.pixels = [self.map8x32to1x256(matrixR), self.map8x32to1x256(matrixG), self.map8x32to1x256(matrixB)]
    #   # led.update()

    #   # Limit to 60 frames per second
    #   clock.tick(60)
  
    #   # Go ahead and update the screen with what we've drawn.
    #   pygame.display.flip()

  def map8x32to1x256(self, data):
    output = []
    for j in range(len(data[0])-1, -1, -1):
      if j%2==0:
        rg = range(len(data))
      else:
        rg = range(len(data)-1, -1, -1)

      for i in rg:
        output.append(data[i][j])

    return output

  def drawOnTable(self):
    self.screen.fill(BLACK)
    for row in range(8):
      for column in range(32):
        # color = WHITE
        # print(self.grid[0][row][column])
        # print(self.grid[1][row][column])
        # print(self.grid[2][row][column])
        # color = Color(int(self.grid[0][row][column]), int(self.grid[1][row][column]), int(self.grid[2][row][column]))
        r = int(self.grid[0][row][column])
        g = int(self.grid[1][row][column])
        b = int(self.grid[2][row][column])
        color = Color(abs(r),abs(g),abs(b))
        # color = Color(r,120,150) # colormap 1
        pygame.draw.rect(self.screen,
                        color,
                        [(MARGIN + WIDTH) * column + MARGIN,
                          (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH,
                          HEIGHT])
        # pygame.draw.circle(self.screen,
        #                 color,
        #                 [(MARGIN + WIDTH) * column + MARGIN*4,
        #                   (MARGIN + HEIGHT) * row + MARGIN*4,
        #                   ], RADIUS_CIRCLE)

  def updateVirtualLedTable(self, mR, mG, mB):
    self.grid = [mR, mG, mB]
    self.drawOnTable()
    pygame.display.flip()

  def closeGame(self):
    pygame.quit()
# play = VirtualLedTable()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.