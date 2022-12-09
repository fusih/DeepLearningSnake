import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN1 = (0, 138, 0)
GREEN2 = (0, 100, 0)
LGREEN = (124,250,0)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 15

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
           
    def reset(self):
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
       
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward=0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward,game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward,game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(LGREEN)
        i=0
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            if i==0:
                pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x+6, pt.y+6, 4, 4))
                pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x+6, pt.y+12, 4, 4))
            i=i+1
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.food.x+6,self.food.y-2, 4 ,7))
        pygame.draw.rect(self.display, GREEN2, pygame.Rect(self.food.x+6,self.food.y-5, 7 ,4))

        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        # [stright,right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir = clock_wise[idx]       # no change 
        if np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1 )%4
            new_dir = clock_wise[next_idx]       # right turn 
        else:  #[0,0,1]
            next_idx = (idx-1)%4
            new_dir = clock_wise[next_idx]
        
        self.direction = new_dir


        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            
