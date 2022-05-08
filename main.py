from pygame import *
import time as t

mixer.init()
font.init()
#import time
from random import randint
#создай окно игры
font2 = font.SysFont("Arial", 25)
font3 = font.SysFont("Arial", 50)
window = display.set_mode((800, 500))
display.set_caption("Шутер")
win_width = 700
win_hight = 500
backrround = transform.scale(image.load("galaxy.jpg"), (700, 500))


clock = time.Clock()
FPS = 60
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
game = True
score = 0
lost = 0
finish = True
c = True
q = 1
e = 1
#ВСЕ КЛАССЫ
class GameSprite(sprite.Sprite):
    def __init__(self, background, player_x, player_y, player_speed, sizex, sizey):
        super().__init__()
        self.image = transform.scale(image.load(background), (sizex, sizey))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, background, player_x, player_y, player_speed, sizex, sizey):
        self.image = transform.scale(image.load(background), (sizex, sizey))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("rocket.png", self.rect.centerx, self.rect.top, -2, 10, 10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            # print(self.rect.y)
            lost += 1
            self.rect.x = randint(20, win_width - 60)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # print(self.rect.y)
        if self.rect.y < 0:
            self.kill()

class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_width, wall_higth, wall_x, wall_y, speed):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.hight = wall_higth
        self.image = Surface((self.width, self.hight))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        self.speed = speed
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            # print(self.rect.y)
            lost += 1
            self.rect.x = randint(20, win_width - 60)
            self.rect.y = 0
class Boss(sprite.Sprite):
    def __init__(self, background, player_x, player_y, player_speed, health, sizex, sizey):
        super().__init__()
        self.image = transform.scale(image.load(background), (sizex, sizey))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.health = health
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_hight:
            # print(self.rect.y)
            global lost
            lost += 3
            self.rect.x = randint(20, win_width - 60)
            self.rect.y = 0
            self.health = 5
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def fire(self):
        bullet1 = Bullet("rocket.png", self.rect.centerx, self.rect.top, -2, 10, 10)
        bullets.add(bullet)
class Asteroid(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global lost
        if self.rect.y == 0:
            # print(self.rect.y)
            self.rect.x = randint(20, win_width - 60)
            self.rect.y = 500



    
#СOЗДАНИЕ ОБЪЕКТОВ И ИХ ОПИСАНЕ
player = Player("rocket.png", 0, 430, 10, 60, 70)
monster = sprite.Group()
for i in range (1, 6):
    ufo = Enemy("ufo.png", randint(20, win_width - 60), 0, randint(1, 3), 60, 50)
    monster.add(ufo)
walls = sprite.Group()
for i in range (1,3):
    wall = Wall(0, 255, 0, 200, 10, randint(20, win_width - 60), 0, randint(1, 2))
    walls.add(wall)
asteroids = sprite.Group()
for i in range (1, 3):
    asteroid = Asteroid("asteroid.png", randint(20, win_width - 60), 500, randint(1, 3), 60, 50)
    asteroids.add(asteroid)
bullets = sprite.Group()

players = sprite.Group()
# players.add(player)
bosss = sprite.Group()
boss = Boss("ufo.png", 200, 0, 1, 5, 150, 140)
bosss1 = sprite.Group()
boss1 = Boss("ufo.png", 200, 0, 1.3, 10, 150, 140)
bosss2 = sprite.Group()
boss2 = Boss("ufo.png", 200, 0, 1.5, 15, 150, 140)

bosss.add(boss)
bosss1.add(boss1)
bosss2.add(boss2)
h = 1
p = 0
g = False

real_time = t.time()
#ОСНОВНОЙ ЦИКЛ
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not g:
                fire.play()
                player.fire()
                p += 1
#ОТРЕСОВКА НАДПЕСЕЙ
    window.blit(backrround, (0, 0))
    text = font2.render("Счет:" + str(score), 1, (255, 255, 255))
    text2 = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
    text_win = font3.render("ТЫ ВЫЙГРАЛ!!!!!", 1, (0, 255, 0))
    text_lose = font3.render("ТЫ ПРОИГРАЛ!!!!", 1, (255, 0, 0))
    window.blit(text, (10, 20))
    window.blit(text2, (10, 50))
#ОТРЕСОВКА ВСЕХ ПЕРСОНАЖЕЙ И  ИХ ФУНКЦИИ
    if finish:
        player.reset()
        player.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        #walls.update()
        #walls.draw(window)
        monster.update()
        monster.draw(window)

#УСЛОВИЯ ПРОИГРАША И ВЫЙГРАША  
        if sprite.groupcollide(monster, bullets, True, True):
            score += 1
        if len(monster) < 5:
            ufo = Enemy("ufo.png", randint(20, win_width - 60), 0, randint(1, 3), 60, 50)
            monster.add(ufo)
        if sprite.groupcollide(players, walls, True, True):
            finish = False
            window.blit(text_lose, (200, 200))
        if sprite.groupcollide(players, asteroids, True, True):
            finish = False
            window.blit(text_lose, (200, 200))
        if sprite.groupcollide(monster, players, True, True):
            # print(1)
            finish = False 
            window.blit(text_lose, (200, 200))     
        if lost == 10:
            finish = False
            window.blit(text_lose, (200, 200))
        '''if score == 60:
            print(2)
            finish = False
            window.blit(text_win, (200, 200))'''
#БОССЫ
        if score >= 10 and h == 1:
            boss.reset()
            boss.update()
            c = False
        if sprite.groupcollide(bullets, bosss, True, False):
            print(boss.health)
            boss.health -= 1
        if boss.health == 0:
            h = 0
            boss.kill()

        if score >= 50 and q == 1:
            boss1.reset()
            boss1.update()
            c = False
        if sprite.groupcollide(bullets, bosss1, True, False):
            print(boss1.health)
            boss1.health -= 1
        if boss1.health == 0:
            q = 0
            boss1.kill()


    
        
                
#ПЕРЕЗАРЯДКА
        # print(p, g)
        if p >= 15 and not g:
            real_time = t.time()
            g = True
        else:
            if abs(int(real_time)- int(t.time())) > 2:
                real_time = t.time()
                p = 0
                g = False


    display.update()
    clock.tick(FPS)

   
