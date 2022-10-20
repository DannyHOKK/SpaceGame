from re import L
import pygame
import random
import keyboard
import os
from pynput.keyboard import Key,Controller

height = 600
width = 500
FPS = 60

#colour 
red = (255,0,0)
white = (255,255,255)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

#game inital setup and display
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("DannyGame")

num_rock = 14
hit_counting = 0
score = 0

running = True
clock = pygame.time.Clock()


#import the image   
background_image = pygame.image.load(os.path.join("img","background.png")).convert()
player_image = pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_image = pygame.transform.scale(player_image,(25,19))
player_mini_image.set_colorkey(black)
# rock_image = pygame.image.load(os.path.join("img","boris.png")).convert()
bullet_image = pygame.image.load(os.path.join("img","bullet.png")).convert()
pygame.display.set_icon(player_mini_image)

# random rock size 
rock_image= []
for i in range(7):
  rock_image.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

# explosion 
expl_anim ={}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(black)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    player_expl_img.set_colorkey(black)
    expl_anim['player'].append(player_expl_img)

# sound
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
explosion_sound = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
backgorund_music = pygame.mixer.music.load(os.path.join("sound","background.ogg"))

# show the score in screen 
font_name = os.path.join("font.ttf")
def draw_text(surf, text , size , x, y):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def print_health(surf, hp ,x ,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 3)

def new_rock ():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_lives(surf, lives, img, x ,y ):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30* i
        img_rect.y = y
        surf.blit(img, img_rect)
    
def draw_init():
    screen.blit((background_image), (0,0))
    draw_text(screen, '太空生存戰!', 64, width/2 ,height /4)
    draw_text(screen, '<-- --> ', 22, width/2 ,height /2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False 
                return False

#control the sprite movement 
class Player(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image,(50,40))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width/2
        self.rect.bottom = height - 20
        self.speedx = 6
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0  


    def update (self):

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False 
            self.rect.centerx = width /2 
            self.rect.bottom = height -10

        key_pressed = pygame.key.get_pressed()

        #press key move
        if keyboard.is_pressed("a"):
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx

        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0 
    
    def shoot(self):
        if not(self.hidden):
            bullet = Bullet(self.rect.centerx , self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide (self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (width/2, height+500)

#The condition of rock falling
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_image)
        self.image_ori.set_colorkey(black)
        self.image = self.image_ori.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, (width- self.rect.width))
        self.rect.y = random.randrange(-200, -180)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        self.total_degree = 0
        self.rot_degree = 3



    def rotate (self):

        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center 
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update (self):

        self.rotate()
       
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if  self.rect.top > height or self.rect.left > width or self.rect.right < 0:
            self.rect.x = random.randrange(0, (width- self.rect.width))
            self.rect.y = random.randrange(-200, -180)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)

#The condition of bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self ,x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update (self):
        
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
            

class Explosion(pygame.sprite.Sprite):
    def __init__(self ,center ,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50


    def update (self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:

            self.last_update = now 
            self.frame += 1 

            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center



pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# main operation
show_init = True


while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
    
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        players = pygame.sprite.Group()
        players.add(player)

        # generate the rock 
        for i in range(num_rock):
            new_rock()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    hits = pygame.sprite.groupcollide(players, rocks, False, pygame.sprite.collide_circle)

    for hit in hits:
        player.health -= hit.radius
        new_rock()
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            die = Explosion(player.rect.center,'player')
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1 
            player.health = 100
            player.hide()

    if player.lives == 0 and not(die.alive()):
        show_init = True

    all_sprites.update()

    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(explosion_sound).play()
        score += hit.radius
        new_rock()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)

    # display setting
    screen.fill((black))
    screen.blit(background_image, (0,0))
    all_sprites.draw(screen)
    print_health(screen, player.health, 20, 20)
    draw_text(screen,str(score), 18, width/2, 10)
    draw_lives(screen, player.lives, player_mini_image, width - 100 , 15)
    pygame.display.update() 
     
pygame.quit()
