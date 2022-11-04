#Core of the game with all the classes, methods, functions and my commentary

import pygame
import  os
import time
import random
pygame.font.init()


#game window
width=900
height=900
window=pygame.display.set_mode((width,height))
#games name caption:
pygame.display.set_caption('Python space shooter game')


#loading assets
red_enemy=pygame.image.load('px_ship_red_small_enemy.png')
green_enemy=pygame.image.load('px_ship_green_small_enemy.png')
blue_enemy=pygame.image.load('px_ship_blue_enemy_large.png')

#resized players ship
players_spaceship=pygame.transform.scale((pygame.image.load('px_spaceship_player.png')),(100,90))

#projectiles

red_laser=pygame.image.load('pixel_laser_red_proj.png')
green_laser=pygame.image.load('pixel_laser_green_proj.png')
blue_laser=pygame.image.load('pixel_blue_laser_proj.png')
yellow_laser=pygame.image.load('pixel_laser_yellow_proj.png')


#sectors backgrounds:
background1=pygame.transform.scale((pygame.image.load('backgorund_sector1.png')),(width,height))

#general ship class for other ships
class ship:
    def __init__(self,x,y,health=100):
        #ship coordinates
        self.x=x
        self.y=y
        self.health=health
        #changeable attributes
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cooldoown=0

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))

    #actual height and width of ship image


    def get_height(self):
        return self.ship_img.get_height()

    def get_width(self):
        return self.ship_img.get_width()


#player calss will iherit from the general ship class
class player(ship):
    def __init__(self,x,y,health=100):
        #calling initialization from general class
        super().__init__(x,y,health)
        #self.ship_img=players_spaceship
        self.ship_img=players_spaceship
        self.laser_img=yellow_laser

        #creating mask for perfect pixel collision
        self.mask=pygame.mask.from_surface(self.ship_img) #mask tells us where pixels are this will help us create much better hitbox
        self.max_healath=health


class enemy(ship):
    def __init__(self,x,y,health=100):
        super().__init__(x, y, health)

def core():
    run=True
    FPS=60
    #checking if player moves "x" number of Frames per second
    clock_check=pygame.time.Clock()

    lvl=1
    player_lives=5
    message_font=pygame.font.SysFont("TTF",35)

    vel_player=5 #velocity of palyer how fast he moves
    players_ship=player(420,800)

    #redrawing everything and refreshing
    def refresh_screen():
        #dispalying backgorund
        window.blit(background1,(0,0))
        #drawing text
        lives_label=message_font.render(f"Players lives: {player_lives}",1,(255,255,255))
        level_label=message_font.render(f"Level: {lvl}",1,(255,255,255))

        #dispalying text
        window.blit(lives_label,(10,10))
        window.blit(level_label,(width-level_label.get_width()-10,10))

        players_ship.draw(window)

        pygame.display.update()

    while run:
        clock_check.tick(FPS) #our game will stay consistent in terms of run speed
        refresh_screen()

        #checking if player closed the game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        keys_movement=pygame.key.get_pressed()
        if keys_movement[pygame.K_LEFT] and players_ship.x -vel_player>0: #moving left with borders
            players_ship.x -=vel_player
        if keys_movement[pygame.K_RIGHT] and players_ship.x +vel_player + players_ship.get_width() <width: #moving right with borders
            players_ship.x += vel_player
        if keys_movement[pygame.K_UP] and players_ship.y -vel_player >0: #moving up with borders
            players_ship.y -= vel_player
        if keys_movement[pygame.K_DOWN] and players_ship.y +vel_player + players_ship.get_height() <height: #moving down with borders
            players_ship.y +=vel_player




#initializing the game
core()