import pygame
import random
import time
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 675
SCREEN_TITLE = "car go brrr"
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
movedelta = SCREEN_WIDTH / 6
left_road_edge = SCREEN_WIDTH / 4
right_road_edge = (SCREEN_WIDTH / 4) + SCREEN_WIDTH / 2
red = (255,0,0)
frame = 0
enemy_costumes = ["images\\enemy_car.png", "images\\enemy_car_crashed.png"]
player_costumes = ["images\\our_car.png", "images\\our_car_crashed.png"]
last_spawn = 0
count_enemy = 0
last_score = 0
enemy_probability = 7
def drawtext(text, x, y, color, size):
    myfont = pygame.font.SysFont('Comic Sans MS', size)
    textsurface = myfont.render(text,False, color)
    window.blit(textsurface,(x, y))
    #pygame.display.update()

def timer():
#    myfont = pygame.font.SysFont('Comic Sans MS', 30)
#    textsurface = myfont.render("Time :"+str(int(frame / 60)),False, (255, 0, 0))
#    window.blit(textsurface,(20, 60))
    drawtext("time :"+str(int(frame / 60)), 20, 60, red, 30)

def lives():
    drawtext("lives :"+str(int(police.lives)), 20, 120, red, 30)

def update_frame():
    window.fill((0,0,0))
    timer()
    lives()
    drawtext("score: "+str(int(police.num)),20, 90, red, 30)
    pygame.draw.rect(window, (0,255,0), (left_road_edge, -25, SCREEN_WIDTH / 2, SCREEN_HEIGHT + 50) ,3)
    road_sprite.draw(window)
    enemy_sprite.draw(window)
    player_sprite.draw(window)
    heart_gp.draw(window)

def gameover():
    enemy_sprite.draw(window)
    update_frame()
    pygame.display.update()
    police.lives = police.lives - 1
    time.sleep(2)
    police.image = pygame.image.load(player_costumes[0])
    police.image = pygame.transform.scale(police.image, (50,100))


    if police.lives == 0:
        police.kill()
        enemy.kill()
        window.fill((0,0,0))
        drawtext('GAME OVER', SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 50, red, 30)
        drawtext("you survived for "+str(int(frame / 60)) + " seconds.", SCREEN_WIDTH / 2 - 200,  SCREEN_HEIGHT / 2 + 70, red, 30)
        drawtext("you dodged  "+str(int(police.num)) + " cars",SCREEN_WIDTH / 2 - 150,  SCREEN_HEIGHT / 2 + 100, red, 30)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
    else:
        for en in enemy_sprite:
            en.rect.y = SCREEN_HEIGHT+100
        police.num -=1




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(player_costumes[0])
        self.image = pygame.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect()
        self.size = self.image.get_rect().size
        self.rect.x = 300
        self.rect.y = 500
        self.speed_x = 0
        self.num = 0
        self.speed_increase = 1
        self.score_changed = False
        self.prev_score = 0
        self.lives = 3

    def update(self):
        if self.rect.x < left_road_edge or self.rect.x + self.size[0] > right_road_edge:
            gameover()
            self.rect.x = SCREEN_WIDTH / 2
        col = pygame.sprite.groupcollide(enemy_sprite, player_sprite, False, False)

        for sprite in col:
            sprite.image = pygame.image.load(enemy_costumes[1])
            sprite.image = pygame.transform.scale(sprite.image, (50,100))
            self.image = pygame.image.load(player_costumes[1])
            self.image = pygame.transform.scale(self.image, (50,100))
            gameover()

        for e in enemy_sprite:
            if e.rect.y > SCREEN_HEIGHT:
                self.num += 1
                e.kill()

        lives_col = pygame.sprite.groupcollide(player_sprite, heart_gp, False, True)
        if lives_col:
            self.lives += 1






    def speed_update(self):
        if self.prev_score<self.num:
            self.prev_score = self.num
            if self.num < 10:
                self.speed_increase += 1




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_costumes[0])
        self.image = pygame.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect()
        self.size = self.image.get_rect().size
        self.fourpos = (left_road_edge ,left_road_edge + movedelta, left_road_edge + (movedelta * 2) - self.size[0], left_road_edge + (movedelta * 3) - self.size[0], police.rect.x)
        if count_enemy == 0:
            self.rect.x = self.fourpos[4]
        else:
            self.rect.x = self.fourpos[random.randint(0,4)]
            self.rect.y = 0 - self.size[1]
            self.speed_y = police.speed_increase

    def update(self):
        self.rect.y += police.speed_increase
#        if self.rect.y > SCREEN_HEIGHT:
#            police.num += 1
#            for i in range(random.randint(1,3)):
#                enemy = Enemy()
#                player_sprite.add(enemy)
#            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,70))
        self.rect = self.image.get_rect()
        self.size = self.image.get_rect().size
        self.delta_y = (position * 120)-70
        self.rect.x = SCREEN_WIDTH / 2 - (self.size[0]/2)
        if position == -1:
            self.rect.y = -55
        else:
            self.rect.y = self.delta_y
        pygame.draw.rect(self.image,(0,255,0), (0, 0, 15, 70))
        self.speed_y = police.speed_increase

    def update(self):
        self.speed_y = police.speed_increase
        self.rect.y += police.speed_increase
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
            stripe = Background(-1)
            road_sprite.add(stripe)

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images\\life.png')
        self.image = pygame.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect()
        self.size = self.image.get_rect().size
        self.rect.x = random.randint(left_road_edge, right_road_edge - self.size[0])
        self.rect.y = 0 - self.size[1]

    def update(self):
        self.rect.y += police.speed_increase
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()




police = Player()
enemy1 = Enemy()

#stripe = Background()
road_sprite = pygame.sprite.Group()
for i in range(0,6):
    stripe = Background(i)
    road_sprite.add(stripe)

player_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
heart_gp = pygame.sprite.Group()

player_sprite.add(police)
enemy_sprite.add(enemy1)
while True:
    time.sleep(0.0166667)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                police.speed_x = police.speed_increase
            if event.key == pygame.K_LEFT:
                police.speed_x = -police.speed_increase

    gen = random.randint(1,1000)
    if gen < enemy_probability and frame > last_spawn + 90:
        count_enemy += 1
        enemy = Enemy()
        enemy_sprite.add(enemy)
        last_spawn = frame

    if last_score < police.num:
        if police.num%5 == 0 and police.num != 0:
            heart = Heart()
            heart_gp.add(heart)
        last_score = police.num
        enemy_probability += 2
        print(enemy_probability)

    player_sprite.update()
    enemy_sprite.update()
    road_sprite.update()
    heart_gp.update()
    police.speed_update()

#update

    update_frame()
    police.rect.x += police.speed_x
    pygame.display.update()
    frame += 1
