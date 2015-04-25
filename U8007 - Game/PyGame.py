""" Project for U8007 - PyGame game.
Version 3.1 - 25th April 2015
"""

import pygame
import sys
import random
from pygame.locals import *

print (sys.version)
pygame.init()

# --- 1a : import from first level? ---

previous_score = 0


# --- 1b : Classes ---

class Bullet (pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        # == Create and color image ==
        self.image = pygame.Surface([width, height]) #appearence
        self.image.fill(color)
        self.speed = 20 #

        #Fetch dimensions and update posi?
        self.rect = self.image.get_rect()

    def update(self):
        """ Called each frame. """
 
        #Move block right one pixel
        self.rect.x += self.speed

        if self.rect.x > displayX:
           self.kill()

class Enemy (pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        # == Create and color image ==
        self.image = pygame.Surface([width, height]) #appearance
        self.image.fill(color)
        self.speed = 10

        #Fetch dimensions and update posi?
        self.rect = self.image.get_rect()

    def update(self):
        """ Called each frame. """
 
        # Move block left one pixel
        self.rect.x -= self.speed

        if self.rect.x < 0:
           self.kill()

# --- 1c : Varibles (such as Colours) ---

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)

ship = pygame.image.load('ship.png')

#pygame.mouse.set_visible(False)
FPS = 10000
clock = pygame.time.Clock()


# --- 2. Set display size and name ----
displayX = 1280
displayY = 720
setDisplay = pygame.display.set_mode((displayX, displayY)) # Game's window mode
pygame.display.set_caption('U8007 - Business Game Project BETA') # Game's title
background = pygame.image.load('background.png')
font = pygame.font.SysFont(None, 25, bold = False, italic = True)

bullet_list = pygame.sprite.Group() # This is a list of all bullets
enemy_list = pygame.sprite.Group() # This is a list of all enemies
all_sprites_list = pygame.sprite.Group() # This is a list of every sprite. 


# --- 3. ####### MAIN PROGRAM ########  ---

def createBullet(x,y):
    new_bullet = Bullet(yellow, 10, 5)
    new_bullet.rect.x = x
    new_bullet.rect.y = y
    bullet_list.add(new_bullet)
    all_sprites_list.add(new_bullet)

def createEnemy(screen_width, screen_height):
    new_enemy = Enemy(red, 30, 30)
    random_num = random.randint(50, (screen_height - 50))
    new_enemy.rect.x = (screen_width - 10)
    new_enemy.rect.y = random_num
    enemy_list.add(new_enemy)
    all_sprites_list.add(new_enemy)

'''
This section is under a while loop as live events are occuring
'''    
def gameLoop():
    timer = 0
    score = 0
    isBullet = False
    game_run = True
    while game_run == True:
        for event in pygame.event.get():
            #code for exiting program
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bulletx = (shipX + 90) # Get ship position X
                bullety = (shipY + 70) # Get ship position Y
                createBullet(bulletx,bullety) # "create" new bullet
        # ~~~ 3A Ship interaction START ~~~
        player_position = pygame.mouse.get_pos()
        shipX = 20

        # == Movement Boundary if statement ==
        if player_position[1] < 50:
            shipY = 0
        elif player_position[1] > (displayY - 40):
            shipY = displayY - 90
        else:
            shipY = (player_position[1]) - 50


        setDisplay.blit(background, (0, 0))# Blit background to screen
        setDisplay.blit(ship, (shipX, shipY)) # Blit ship to screen
        ''' ~~~ 3A Ship interaction END ~~~ '''
        
        # ~~~~ 3B Bullets START ~~~~
        if int(timer) % 5 == 0:
            createEnemy(displayX, displayY) # IMPORTANT "create" new enemy


        #set_timer(USEREVENT + 1, 3000)
        # ~~~~~ 3B bullet END ~~~~~

        # ~~~~~ 3C collisions START ~~~~~
        collision_list = pygame.sprite.groupcollide(bullet_list, enemy_list, True, True)
        for collision in collision_list:
            score += 1
        # ~~~~~ 3C collisions END ~~~~~
        
        all_sprites_list.update() # update all sprites for movement
        all_sprites_list.draw(setDisplay) # Blit all active sprites to screen
        seconds = clock.tick()/1000.0
        timer += seconds / 1
        timer_text=font.render('Timer: '+str(timer),1,(255,255,255))
        size = timer_text.get_rect()
        timerXpos = (displayX - size[2])/2
        setDisplay.blit(timer_text, [timerXpos,20])
        score_text = font.render("Score: " + str(score) , 1 ,(255,255,255))
        setDisplay.blit(score_text,(1100,30)) # Blit Text to screen

        clock.tick(FPS)
        pygame.display.flip() #update entire screen

    pygame.quit()
    sys.exit()

# --- 5. Run --- 
gameLoop()
pygame.quit()


