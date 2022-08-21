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
        self.speed = 5

    def reset(self):
        self.rect.center = (400, 550)

    def input(self):
        keys = pygame.key.get_pressed()
        global game_active
        if not game_active:
            self.reset()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

    def update(self):
        self.input()


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.circle(self.image, color, (int(width // 2), int(height // 2)), 5)
        self.rect = self.image.get_rect(midbottom=(400, 510))
        self.y_speed = -3
        self.x_speed = -3

    def reset(self):
        self.rect.center = (400, 510)
        self.y_speed = -3
        self.x_speed = -3

    def movement(self):
        global game_active
        if self.rect.bottom >= 600:
            self.reset()
            game_active = False

        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if self.rect.x > 800 or self.rect.x < 0:
            self.x_speed = -self.x_speed
        if self.rect.y < 0:
            self.y_speed = -self.y_speed

    def collision(self):
        if pygame.sprite.collide_mask(ball.sprite, player.sprite):
            self.y_speed = -self.y_speed
            self.x_speed = -self.x_speed
        for brick in bricks:
            if pygame.sprite.collide_mask(ball.sprite, brick):
                self.y_speed = -self.y_speed
                brick.kill()

    def update(self):
        self.movement()
        self.collision()


class Bricks(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect(midbottom=(random.randint(10, 790), random.randint(25, 300)))

    def overlap(self):
        for brick in bricks:
            for brick2 in bricks:
                if brick != brick2:
                    if brick.rect.colliderect(brick2.rect):
                        brick2.kill()

    def game_over(self):
        if len(bricks) == 0:
            global game_active
            game_active = False

    def update(self):
        self.overlap()
        self.game_over()


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
game_active = False

font = pygame.font.SysFont('monospace', 24)
background = pygame.Color('black')

player = pygame.sprite.GroupSingle()
player.add(Player(color=(20, 0, 255), width=55, height=10))

ball = pygame.sprite.GroupSingle()
ball.add(Ball(color=(255, 0, 0), width=20, height=20))

bricks = pygame.sprite.Group()
for i in range(75):
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
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    if game_active:
        screen.fill(background)

        ball.draw(screen)
        ball.update()

        player.draw(screen)
        player.update()

        bricks.draw(screen)
        bricks.update()

    else:
        start_message = font.render('Press Space to start', False, (111, 196, 169))
        start_message_rect = start_message.get_rect(center=(400, 300))

        screen.blit(start_message, start_message_rect)

    pygame.display.update()
    clock.tick(60)
