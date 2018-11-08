#!/usr/bin/python3
#https://pythonprogramming.net/pygame-crashing-objects/?completed=/drawing-objects-pygame-tutorial/
#https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
import os
import pygame
from pygame import *
import pyganim

ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
WIN_WIDTH =  800 # Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = '#a4b0c4' #'#0639a8' # "#004400"
BLACK = (0,0,0)
WHITE = (255,255,255)
RED =   (255,0,0)
BLUE =  (0,0,255)
GREEN = (0,255,0)
GROUND = (WIN_HEIGHT * 0.8) + 43
WIDTH = 100 #22
HEIGHT = 100 #32
COLOR =  "#888888"
MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

ANIMATION_DELAY = 100 # скорость смены кадров
ANIMATION_JUMP = [('assets/dino/dino_jump.png'.format(ICON_DIR), 100)]
ANIMATION_RUN = [('assets/dino/dino_r1.png'.format(ICON_DIR)),
                ('assets/dino/dino_r2.png').format(ICON_DIR),]


def main():
    pygame.init()

    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption('Dinorun')
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
    hero = Dino(50, 200)  # создаем героя по (x,y) координатам
    cactus = BlockDie(1000, 400,'small')

    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)
    entities.add(cactus)
    temp_group = pygame.sprite.Group()
    temp_group.add(cactus, hero)

    level = ['',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '',
             '-----------------------------']
    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)  # создаем экземпляр класса Platform
                entities.add(pf)  # добавляем его в группу спрайтов entities
                platforms.append(pf)  # массив платформ

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_q:
                raise SystemExit

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False

        screen.blit(bg, (0,0))
        hero.update(up, platforms, cactus)  # передвижение
        cactus.update()
        entities.draw(screen)
        pygame.display.update()

        # print(dead)

        # if len(dead) > 0:
        #     print('[+]', hero.rect.x)

        if cactus.rect.x < 0:
            cactus.rect.x = 1000


class Dino(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.startX = x
        self.startY = y
        self.xvel = 0
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        # Анимация бега
        boltAnim = []
        for anim in ANIMATION_RUN:
            boltAnim.append((anim,ANIMATION_DELAY))
        self.boltAnimRun = pyganim.PygAnimation(boltAnim)
        self.boltAnimRun.play()

        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()


    def update(self, up, platforms, cactus):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))


        if not self.onGround:
                self.yvel += GRAVITY

        self.image.fill(Color(COLOR))
        self.boltAnimRun.blit(self.image, (0, 0))
        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, cactus)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, cactus)


    def collide(self, xvel, yvel, platforms, cactus):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

        # dead = pygame.sprite.collide_rect_ratio(ratio)(left, right):
        dead = pygame.sprite.collide_rect_ratio(0.5)(self, cactus)
        if dead:
            print(seld.rect.x)
            self.die()

        # if sprite.collide_rect(self, cactus):
        # if x(0.5):

        # if self.rect.x + 32 > cactus.rect.x and self.rect.y + 64 > cactus.rect.y:

        # dead = pygame.sprite.spritecollide(self, cactus, True)
        # if dead:
        #     print(cactus.rect.x)
            # self.die()


    def die(self):
        time.wait(1500)
        raise SystemExit


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("assets/blocks/platform.png".format(ICON_DIR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = image.load('assets/blocks/penis.png'.format(ICON_DIR))
        self.type = size
        # Не забудь сделать self.rect
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
        self.startX = x # начальные координаты
        self.startY = y
        self.xvel = -3
        self.yvel = 0

    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel


if __name__ == '__main__':
    main()

