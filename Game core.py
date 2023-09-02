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
        #creating lasers
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self,velocity,objs):
        self.cooldown_handler() #handler increments when lasers move
        for laser in self.lasers:
            laser.move(velocity)

        if laser.off_screen(height):
            self.lasers.remove(laser)
        elif laser.collision(objs):
            objs.health -=10
            self.lasers.remove(laser)


    #cooldown
    CooldownTime=30

    #handling the counting of cooldown
    def cooldown_handler(self):
        if self.cooldoown>=self.CooldownTime:
            self.cooldown_handler=0

        if self.cooldown_handler>0:
            self.cooldown_handler+=1
        
    
    def shoot_laser(self):
        if self.cooldoown==0:
            laser_ =Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser_)

            # satrting cooldown again
            self.cooldoown=1
            

    #actual height and width of ship image



    def get_height(self):
        return self.ship_img.get_height()

    def get_width(self):
        return self.ship_img.get_width()


#laser projectile bullet
class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y+= vel
    def off_screen(self, height):
        return self.y<= height and self.y>= 0
    def collision(self, obj):
        return collide(self, obj)




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


#creating enemy class (similar in construction design to 2 previous ships) enemy ships will have different colors (green, red, blue)
class enemy_(ship):
    #using dictionary to display different ships and their assets based on their color:
    color_enm_dict={"red":(red_enemy,red_laser),
                    "blue":(blue_enemy,blue_laser),
                    "green":(green_enemy,green_laser)}


    def __init__(self,x,y,color,health=100):
        super().__init__(x, y, health)
        #we dont need draw method since its inherited
        self.ship_img,self.laser_img=self.color_enm_dict[color]
        #mask
        self.mask = pygame.mask.from_surface(self.ship_img)

    def movement(self,vel):
        #enemy ships will move only down
        self.y+=vel


def collide(obj_1, obj_2):
    offset_x = obj_2.x - obj_1.x #distance from object 1 to 2
    offset_y = obj_2.y - obj_1.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) !=None
    #bool function telling if masks overlap


def core():
    run=True
    FPS=60
    #checking if player moves "x" number of Frames per second
    clock_check=pygame.time.Clock()
    lose=False
    gamoverscreen_dispaly_time=0

    enemeis=[]
    amount_enem=5 #enemies will come in waves with increasing amounts
    vel_enemy=4


    lvl=0
    player_lives=5
    message_font=pygame.font.SysFont("TTF",35)
    game_over_font=pygame.font.SysFont("TTF",70)

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

        #displaying enemies on screen
        for enemy in enemeis:
            enemy.draw(window)

        players_ship.draw(window)

        if lose is True:
            g_over_label = game_over_font.render("GAME OVER", 1, (255, 255, 255))
            window.blit(g_over_label,(width/2-g_over_label.get_width()/2,350))
            #center of screen is widht/2 but we draw from top left


        pygame.display.update()

    while run:
        clock_check.tick(FPS) #our game will stay consistent in terms of run speed
        refresh_screen()

        if player_lives<=0 or players_ship.health<=0:
            lose=True
            gamoverscreen_dispaly_time+=1

        if lose:
            if gamoverscreen_dispaly_time>FPS*5: #the displaying time of game over screen will last 5 seconds after which we quit game
                run=False
            else: #since GAME OVER message will be on screen for some time we will need to wait before game closes while also not doing any further operations
                continue


        if len(enemeis)==0:
            lvl+=1
            amount_enem+=5
            for i in range(amount_enem):
                #spawning enemies and appending them to list                *(lvl//5+lvl%5)
                enem=enemy_(random.randrange(50,width-100),random.randrange(-1234,-100),random.choice(["red","blue","green"]))
                #all of the enemies will be spawned off screen while moving at the same speed singualr ships will have different positions making the "illusion" of moving in different duration
                enemeis.append(enem)

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
        if keys_movement[pygame.K_SPACE]: #shooting laser
            players_ship.shoot_laser() 

        for enemy in enemeis[:]: #copy of enemies we dont modify list we are looping through
            enemy.movement(vel_enemy)
            #removing enemies
            if enemy.y+enemy.get_height()>height:
                player_lives-=1
                enemeis.remove(enemy)





#initializing the game
core()
