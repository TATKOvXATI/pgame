import pygame
import random
import time

window = pygame.display.set_mode((800,800))

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource (works for PyInstaller onefile mode) """
    if getattr(sys, 'frozen', False):  # If running as an executable
        base_path = sys._MEIPASS  # Temporary folder where PyInstaller unpacks files
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

image1_path = resource_path("pixil-frame-0 (2).png")
image2_path = resource_path("218071 (1).png")

colorlist = ((255,0,0), (0,255,0), (0,0,255))

BLACK = (0,0,0)
WHITE = (255,255,255)

deliveryimage = pygame.image.load("pixil-frame-0 (2).png")

def carcolor():
    carimage = pygame.image.load("218071 (1).png").convert_alpha()
    cararray = pygame.PixelArray(carimage)
    randcolor = random.choice(colorlist)

    cararray.replace((74, 94, 149), randcolor)
    cararray.replace((58,78,128), randcolor)
    cararray.replace((52,60,84), randcolor)
    cararray.replace((100,110,158), randcolor)
    cararray.replace((27,39,63), randcolor)
    cararray.replace((52, 60, 84), randcolor)
    return carimage

class Text(pygame.sprite.Sprite):
    def __init__(self, text, x, y, size, color):
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, text, x, y, color):
        self.image = self.font.render(self.text, True, color)

class Deliveryman(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((70, 100))
        self.image = deliveryimage

        self.rect = self.image.get_rect()
        self.rect.x = 330
        self.rect.y = 600

    def turn(self, coords):
        self.rect.x += coords

class Cars(pygame.sprite.Sprite):
    def __init__(self, color, speed, x, isflipped=False):
        super().__init__()
        self.image = pygame.Surface((70, 100))
        carimage = carcolor()
        self.image = pygame.transform.flip(carimage, False, isflipped)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = x
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 799:
            self.kill()

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 70)
        self.text = "GAME OVER,\n press R to restart"
        self.image = self.font.render(self.text, True, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 75

    def update(self):
        self.text = "GAME OVER,\n press R to restart"
        self.image = self.font.render(self.text, True, (255, 0, 0))

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 30)
        self.text = "score = 0"
        self.image = self.font.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 20
        self.score = 0

    def update(self):
        self.score += 1
        self.text = f"score = {self.score}"
        self.image = self.font.render(self.text, True, WHITE)

class Objects(pygame.sprite.Sprite):
    def __init__(self, color, speed, x, isflipped=False):
        super().__init__()
        self.image = pygame.Surface((50, 10))
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = x
        self.speed = 12

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 799:
            self.kill()


def game(d, t):
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((800, 800))
    deliveryman = pygame.sprite.Sprite()
    BLUE = (0, 0, 255)
    carcounter = 0
    alive = True
    score = Score()
    timer = 0
    spawn_timer = 0

    deliveryman = Deliveryman(BLUE)

    object_sprites = pygame.sprite.Group()

    scoresprites = pygame.sprite.Group()
    scoresprites.add(score)
    main_sprites = pygame.sprite.Group()
    main_sprites.add(deliveryman)

    car_sprites = pygame.sprite.Group()

    gameover = GameOver()
    gameoversprites = pygame.sprite.Group()
    gameoversprites.add(gameover)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not deliveryman.rect.x <200 and alive:
                deliveryman.turn(-100)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not deliveryman.rect.x >600 and alive:
                deliveryman.turn(100)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and not alive:
                game(d, t)
                return

        window.fill((0, 0, 0))

        pygame.draw.rect(window, (0,255,0), (0,0, 100, 800))
        pygame.draw.rect(window, (0, 255, 0), (700, 0, 100, 800))
        pygame.draw.line(window, (255,255,255), (200,0), (200,800))
        pygame.draw.line(window, (255, 255, 255), (300, 0), (300, 800))
        pygame.draw.line(window, (255, 255, 255), (400, 0), (400, 800))
        pygame.draw.line(window, (255, 255, 255), (500, 0), (500, 800))
        pygame.draw.line(window, (255, 255, 255), (600, 0), (600, 800))
        pygame.draw.rect(window, (160,160,160), (100,0, 101, 800))
        pygame.draw.rect(window, (160, 160, 160), (600, 0, 100, 800))

        timer += 1

        if timer > t and alive:
            objects = Objects((120, 120, 120), 12+d, 115,)
            object_sprites.add(objects)
            objects = Objects((120, 120, 120), 12+d, 615, )
            object_sprites.add(objects)


            line = random.choice((215, 315, 415, 515))
            if line <350 and alive:
                cars = Cars((255, 255, 255), 14+d, line)
                car_sprites.add(cars)

                timer = 0


            else:
                cars = Cars((255, 255, 255), 3+d, line, True)
                car_sprites.add(cars)

                timer = 0


        if pygame.sprite.spritecollide(deliveryman, car_sprites, False):
            alive = False
            gameoversprites.draw(window)
            gameover.update()

        if pygame.sprite.spritecollide(deliveryman, object_sprites, False):
            alive = False
            gameoversprites.draw(window)
            gameover.update()

        if alive:
            car_sprites.draw(window)
            car_sprites.update()
            object_sprites.draw(window)
            object_sprites.update()
        if alive:
            score.update()
            scoresprites.draw(window)

        main_sprites.draw(window)
        pygame.display.update()
        clock.tick(60)

def menu():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((300, 400))
    text = Text("Menu", 80, 50, 70, BLACK)
    textsprites = pygame.sprite.Group()
    textsprites.add(text)
    text1 = Text("Easy", 80, 120, 30, BLACK)
    textsprites.add(text1)
    text2 = Text("Medium", 80, 200, 30, BLACK)
    textsprites.add(text2)
    text3 = Text("Hard", 80, 280, 30, BLACK)
    textsprites.add(text3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 80 < x < 230 and 120 < y < 180:
                    game(0, 150)

                elif 80 < x < 230 and 200 < y < 260:

                    game(2, 120)
                elif 80 < x < 230 and 280 < y < 340:

                    game(5, 40)

        pygame.draw.rect(window, (0, 255, 0), (80, 120, 150, 60), 60  )
        pygame.draw.rect(window, (255, 255, 0), (80, 200, 150, 60), 60)
        pygame.draw.rect(window, (255, 0, 0), (80, 280, 150, 60), 60)
        textsprites.draw(window)
        textsprites.update("Menu", 100, 50, BLACK)

        pygame.display.update()
        clock.tick(60)

menu()