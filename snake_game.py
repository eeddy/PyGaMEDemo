import pygame
from pygame.locals import *
import random

class SnakeGame:
    def __init__(self):
        random.seed(0)
        self.width = 500
        self.height = 500
        
        # Pygame Setup:
        pygame.init()
        self.window = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('Pygame (Snake) EMG Demo')
        self.clock = pygame.time.Clock()

        # Game Variables:
        self.running = True 
        self.score = 0
        self.movement = 20
        self.snake_head = [40,40]
        self.snake_body = []
        self.target = [None, None]
        self.generate_target()
        self.previous_key_presses = []

        # Colors
        self.snake_green = (5, 255, 0)
        self.head_blue = (0, 133, 255)
        self.red = (255, 0, 0)
    
    def generate_target(self):
        x = random.randrange(20, self.width-20) 
        y = random.randrange(20, self.height-20) 
        self.target[0] = x - x % self.movement
        self.target[1] = y - y % self.movement
    
    def handle_movement(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            
            # Listen for key presses:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.previous_key_presses.append("left")
                elif event.key == pygame.K_RIGHT:
                    self.previous_key_presses.append("right")
                elif event.key == pygame.K_UP:
                    self.previous_key_presses.append("up")
                elif event.key == pygame.K_DOWN:
                    self.previous_key_presses.append("down")
                else:
                    return 
                
                # Move head 
                self.move(self.previous_key_presses[-1], self.snake_head)

                # Move the snake body 
                for i in range(0, len(self.snake_body)):
                    self.move(self.previous_key_presses[-(2+i)], self.snake_body[i])

    def move(self, direction, block):
        if direction == "left":
            block[0] -= self.movement
        elif direction == "right":
            block[0] += self.movement
        elif direction == "up":
            block[1] -= 20
        elif direction == "down":
            block[1] += 20

    def grow_snake(self):
        x = self.snake_head[0]
        y = self.snake_head[1]
        idx = -1

        if len(self.snake_body) > 0:
            x = self.snake_body[-1][0]
            y = self.snake_body[-1][1]
            idx = -(1 + len(self.snake_body))

        if self.previous_key_presses[idx] == "left":
            x += self.movement
        elif self.previous_key_presses[idx] == "right":
            x -= self.movement
        elif self.previous_key_presses[idx] == "up":
            y += 20
        elif self.previous_key_presses[idx] == "down":
            y -= 20
        self.snake_body.append([x,y])

    def run_game(self):
        while self.running:
            # Check for collision between snake and head
            snake = Rect(self.snake_head[0], self.snake_head[1], 20, 20)
            target = Rect(self.target[0], self.target[1], 20, 20)
            if pygame.Rect.colliderect(snake, target):
                self.generate_target()
                self.grow_snake()
                self.score += 1
            
            # Fill the background with black
            self.window.fill((233, 233, 233))

            # Listen for movement events
            self.handle_movement()

            # Draw Snake
            pygame.draw.rect(self.window, self.head_blue, snake, border_radius=2)
            for b in self.snake_body:
                pygame.draw.rect(self.window, self.snake_green, [b[0], b[1], 20, 20],  border_radius=2)

            # Draw Target 
            pygame.draw.rect(self.window, self.red, target)

            # Score label
            myfont = pygame.font.SysFont("arial bold", 30)
            label = myfont.render("Score: " + str(self.score), 1, (0,0,0))
            self.window.blit(label, (self.width - 100, 10))

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    sg = SnakeGame()
    sg.run_game()