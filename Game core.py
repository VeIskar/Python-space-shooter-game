#Core of the game with all the classes, methods, functions and my commentary

import pygame
import  os
import time
import random

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

#players ship
players_spaceship=pygame.image.load('px_spaceship_player.png')

#projectiles

red_laser=pygame.image.load('pixel_laser_red_proj.png')
green_laser=pygame.image.load('pixel_laser_green_proj.png')
blue_laser=pygame.image.load('pixel_blue_laser_proj.png')
yellow_laser=pygame.image.load('pixel_laser_yellow_proj.png')


#sectors backgrounds:
background1=pygame.image.load('backgorund_sector1.png')


def core():
    run=True
    FPS=60
    #checking if player moves "x" number of Frames per second
    clock_check=pygame.time.Clock()


    while run:
        clock_check.tick(FPS) #our game will stay consistent in terms of run speed


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False