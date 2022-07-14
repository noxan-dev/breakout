import pygame
from sys import exit
import random

r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect(midbottom=(400, 550))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3

    def update(self):
        self.input()


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.circle(self.image, color, (int(width // 2), int(height // 2)), 5)
        self.rect = self.image.get_rect(midbottom=(400, 525))

    def update(self):
        pass


class Bricks(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect(midbottom=(random.randint(10, 790), random.randint(25, 300)))

    def update(self):
        pass


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()

background = pygame.Color('black')

player = pygame.sprite.GroupSingle()
player.add(Player(color=(20, 0, 255), width=55, height=10))

ball = pygame.sprite.GroupSingle()
ball.add(Ball(color=(255, 0, 0), width=20, height=20))

bricks = pygame.sprite.Group()
for i in range(5):
    for j in range(5):
        bricks.add(Bricks(color=(r, g, b), width=50, height=20))
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        bricks.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(background)

    ball.draw(screen)
    ball.update()

    player.draw(screen)
    player.update()

    bricks.draw(screen)
    bricks.update()

    pygame.display.update()
    clock.tick(60)
