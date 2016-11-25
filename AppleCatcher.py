# Ryan Marino
# Apple_Catcher.py
# A graphic application where the goal is to last as long as possible in an
# increasingly-difficult game.

import pygame, sys
from pygame.locals import *
import os
import time
from random import randint

# Initialize game variables
applestonextlevel = 2
level = 1
lives = 4
speed = 1.0 + level
playgameoversound = 0

# Class for the red basket object
class Basket(object):

    # Object constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("basket_red.png")
        self.rect = pygame.Rect(self.x,self.y,80,40)

    # Button input that causes the object to do things
    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 6 + speed
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and self.y < 550:
            self.y += dist

        elif (key[pygame.K_UP] or key[pygame.K_w]) and self.y > 150:
            self.y -= dist

        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.x < 710:
            self.x += dist

        elif (key[pygame.K_LEFT] or key[pygame.K_a]) and self.x> 10:
                self.x -= dist

    # Draws the object on the screen
    def draw(self, surface):
        GAMESCREEN.blit(self.image, (self.x, self.y))
        self.rect = pygame.Rect(self.x,self.y,80,40)

# Class for the red apple object
class RedApple(pygame.sprite.Sprite):

    # Object constructor
    def __init__(self, GAMESCREEN):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("red_apple.png")
        self.x = randint(40,718)
        self.y = 100
        self.rect = pygame.Rect(self.x,self.y,50,50)

    # Makes the apple fall and disappear if reached the bottom or collided with the basket
    def update(self):
        global lives
        global applestonextlevel
        self.rect.move_ip(0,speed)
        if self.rect.bottom > 590:
            redapplesplatsound.play()
            self.kill()
            #lives -= 1
        if pygame.sprite.collide_rect(self, red_basket):
                redapplesound.play()
                self.kill()
                applestonextlevel -= 1

# Class for the bad apple object
class BadApple(pygame.sprite.Sprite):

    # Object constructor
    def __init__(self, GAMESCREEN):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bad_apple.png")
        self.x = randint(40,718)
        self.y = 100
        self.rect = pygame.Rect(self.x,self.y,50,50)

    # Makes the apple fall and disappear if reached the bottom or collided with the basket
    def update(self):
        global lives
        self.rect.move_ip(0,speed)
        if self.rect.bottom > 590:
            self.kill()
        if pygame.sprite.collide_rect(self, red_basket):
            badapplesound.play()
            lives -= 1         # Subtracts 1 from lives if hit the basket
            self.kill()

# Class for the green apple object
class GreenApple(pygame.sprite.Sprite):

    # Object constructor
    def __init__(self, GAMESCREEN):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("green_apple.png")
        self.x = randint(40,718)
        self.y = 100
        self.rect = pygame.Rect(self.x,self.y,50,50)

    # Makes the apple fall and disappear if reached the bottom or collided with the basket
    def update(self):
        global applestonextlevel
        self.rect.move_ip(0,speed ** 1.5)
        if self.rect.bottom > 590:
            self.kill()
        if pygame.sprite.collide_rect(self, red_basket):
            if applestonextlevel == 1:
                applestonextlevel -= 1
                self.kill()
                greenapplesound.play()
            else:
                applestonextlevel //= 2
                self.kill()
                greenapplesound.play()

# Class for the yellow apple object
class YellowApple(pygame.sprite.Sprite):

    # Object constructor
    def __init__(self, GAMESCREEN):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("yellow_apple.png")
        self.x = randint(40,718)
        self.y = 100
        self.rect = pygame.Rect(self.x,self.y,50,50)

    # Makes the apple fall and disappear if reached the bottom or collided with the basket
    def update(self):
        global lives
        global applestonextlevel
        self.rect.move_ip(0, speed ** 1.5)
        if self.rect.bottom > 590:
            self.kill()
        # Counts as a regular apple, and also adds a life
        if pygame.sprite.collide_rect(self, red_basket):
            applestonextlevel -= 1
            lives += 1
            self.kill()
            yellowapplesound.play()

# Initialize
pygame.init()
pygame.mixer.init()
pygame.display.init()

# Create game window
GAMESCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Apple Catcher')

# Define colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
LIGHTGREEN = (204, 255, 204)

# Import sounds
redapplesound = pygame.mixer.Sound("Ding.wav")
redapplesplatsound = pygame.mixer.Sound("bang.wav")
badapplesound = pygame.mixer.Sound("bad_apple.wav")
gameoversound = pygame.mixer.Sound("lose.wav")
levelupsound = pygame.mixer.Sound("levelup.wav")
greenapplesound = pygame.mixer.Sound("greenDing.wav")
yellowapplesound = pygame.mixer.Sound("woop.wav")

# Define fonts
titlefont = pygame.font.SysFont("verdana", 44, True)
buttonfont = pygame.font.SysFont("verdana", 30)
textfont = pygame.font.SysFont("verdana", 20)
textfont2 = pygame.font.SysFont("verdana", 20, True)
interfacefont = pygame.font.SysFont("comicsansms", 24)
interfacenumfont = pygame.font.SysFont("comicsansms", 24, True)

# Load background
forest = pygame.image.load('forest.jpg')

# Input specifications
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 10)

# Create red basket object
red_basket = Basket(350,300)

# Create apple groups
redapples = pygame.sprite.Group()
badapples = pygame.sprite.Group()
greenapples = pygame.sprite.Group()
yellowapples = pygame.sprite.Group()

# Initial gamemode (menu screen)
gamestart = 0

# Clock for limiting framerate
clock = pygame.time.Clock()

# Game loop - game is active while running = True
running = True
while running:
    GAMESCREEN.fill( (0,0,0) )
    GAMESCREEN.blit(forest, (0, 0))

    # Detect mouse position
    m_x,m_y = pygame.mouse.get_pos()

    # Gamemode 0: Title Screen
    if gamestart == 0:

        # Big Title Panel
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(200,100,400,200))
        pygame.draw.rect(GAMESCREEN,BLACK,(200,100,400,200),4)
        titlelabel = titlefont.render("Apple Catcher", 1, BLACK)
        GAMESCREEN.blit(titlelabel, (237, 130))

        # Button 1: Start
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(190,410,150,80))
        pygame.draw.rect(GAMESCREEN,BLACK,(190,410,150,80),3)
        button1label = buttonfont.render("Start", 1, BLACK)
        GAMESCREEN.blit(button1label, (225,430))

        # Button 2: Instructions
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(400,410,220,80))
        pygame.draw.rect(GAMESCREEN,BLACK,(400,410,220,80),3)
        button2label = buttonfont.render("Instructions", 1, BLACK)
        GAMESCREEN.blit(button2label, (420,430))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Button 1 (Start) clicked
                if m_x > 190 and m_x < 340 and m_y > 410 and m_y < 490:
                    gamestart = 1

                # Button 2 (Instructions) clicked
                if m_x > 400 and m_x < 620 and m_y > 410 and m_y < 490:
                    gamestart = 2

            # Quit game if close button is clicked
            if event.type == QUIT:
                running = False

    # Gamemode 1: One-player mode
    if gamestart == 1:

        # Create interface
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(0,0,800,70))
        pygame.draw.rect(GAMESCREEN,BLACK,(0,0,800,70),3)

        levellabel = interfacefont.render("Level:", 1, BLACK)
        GAMESCREEN.blit(levellabel, (20,15))

        appleslabel = interfacefont.render("Apples to Next Level:", 1, BLACK)
        GAMESCREEN.blit(appleslabel, (160,15))

        lifelabel = interfacefont.render("Life:", 1, BLACK)
        GAMESCREEN.blit(lifelabel, (500,15))

        # Event handling
        for event in pygame.event.get():
        # Quit game if close button is clicked
            if event.type == QUIT:
                running = False
        # Reset variables and return to menu screen if game over button is clicked
            if lives == 0 and m_x > 300 and m_x < 500 and m_y > 360 and m_y < 440:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    lives = 4
                    applestonextlevel = 2
                    level = 1
                    speed = 1 + level
                    playgameoversound = 0
                    gamestart = 0

        # Update interface
        levellabelnum = interfacenumfont.render(str(level), 1, BLACK)
        GAMESCREEN.blit(levellabelnum, (100,15))

        appleslabelnum = interfacenumfont.render(str(applestonextlevel), 1, BLACK)
        GAMESCREEN.blit(appleslabelnum, (430,15))
        # Changes the number of life indicators based on the number of remaining lives
        if lives == 4:
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (570,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (625,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (680,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (735,10))
        elif lives == 3:
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (570,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (625,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (680,10))
        elif lives == 2:
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (570,10))
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (625,10))
        elif lives == 1:
            GAMESCREEN.blit(pygame.image.load("red_apple.png"), (570,10))

        # While the player is still alive...
        if lives != 0:

            # Update speed based on level
            speed = 1 + level

            # Makes sure there is at least 1 red apple on the screen
            if bool(redapples) == False:
                redapples.add(RedApple(GAMESCREEN))

            # Randomly spawn green apples
            spawngreenapple = randint(0,499)
            if spawngreenapple == 0:
                greenapples.add(GreenApple(GAMESCREEN))

            # If the level is 3 or higher, randomly spawn bad apples
            if level >= 3:
               spawnbadapple = randint(0,49)
               if spawnbadapple == 0:
                    badapples.add(BadApple(GAMESCREEN))

            # If the level is 5 or higher, randomly spawn additional red apples
            if level >= 5:
               spawnredapple = randint(0,499)
               if spawnbadapple == 0:
                    redapples.add(RedApple(GAMESCREEN))

            # If at least one life is missing, randomly spawn yellow apples
            if lives <= 3:
                spawnyellowapple = randint(0,599)
                if spawnyellowapple == 0:
                    yellowapples.add(YellowApple(GAMESCREEN))

            # Advance level
            if applestonextlevel == 0:
                level += 1
                applestonextlevel = 2 * level
                levelupsound.play()

            # Handle basket movements
            red_basket.handle_keys()

            # Update apples
            redapples.update()
            badapples.update()
            greenapples.update()
            yellowapples.update()

            # Draw game objects
            red_basket.draw(GAMESCREEN)
            redapples.draw(GAMESCREEN)
            badapples.draw(GAMESCREEN)
            greenapples.draw(GAMESCREEN)
            yellowapples.draw(GAMESCREEN)

        # Player has died
        else:

            # Game over sound
            if playgameoversound == 0:
                gameoversound.play()
                playgameoversound = 1

            # Destroy remaining apples
            badapples.empty()
            greenapples.empty()
            redapples.empty()
            yellowapples.empty()

            # Game over screen
            pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(250,210,300,100))
            pygame.draw.rect(GAMESCREEN,BLACK,(250,210,300,100),3)
            gameoverlabel = titlefont.render("Game Over", 1, BLACK)
            GAMESCREEN.blit(gameoverlabel, (262, 230))

            # Restart Button
            pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(300,360,200,80))
            pygame.draw.rect(GAMESCREEN,BLACK,(300,360,200,80),3)
            restartlabel = buttonfont.render("Menu", 1, BLACK)
            GAMESCREEN.blit(restartlabel, (360, 378))

    # Gamemode 2: Instruction Screen
    if gamestart == 2:

        # Big Instruction Panel
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(50,50,700,450))
        pygame.draw.rect(GAMESCREEN,BLACK,(50,50,700,450),4)
        instructionstitlelabel = titlefont.render("How to Play Apple Catcher", 1, BLACK)
        GAMESCREEN.blit(instructionstitlelabel, (75, 70))

        # Back Button
        pygame.draw.rect(GAMESCREEN,LIGHTGREEN,(325,515,150,70))
        pygame.draw.rect(GAMESCREEN,BLACK,(325,515,150,70),3)
        backbuttonlabel = buttonfont.render("Back", 1, BLACK)
        GAMESCREEN.blit(backbuttonlabel, (360, 530))

        # Instructions body
        instruct1 = textfont.render("Use the WASD keys to catch as many red apples", 1, BLACK)
        GAMESCREEN.blit(instruct1, (75, 150))
        GAMESCREEN.blit(pygame.image.load("red_apple.png"), (600,135))
        instruct3 =  textfont.render("as possible! Catch a certain number of apples to move on to the", 1, BLACK)
        GAMESCREEN.blit(instruct3, (75, 200))
        instruct5 =  textfont.render("next level. Don't let the red apples hit the ground!", 1, BLACK)
        GAMESCREEN.blit(instruct5, (75, 250))
        GAMESCREEN.blit(pygame.image.load("bad_apple.png"), (75,300))
        instruct6 = textfont2.render("Bad apples will take away a life if caught!", 1, BLACK)
        GAMESCREEN.blit(instruct6, (135, 310))
        GAMESCREEN.blit(pygame.image.load("green_apple.png"), (75,360))
        instruct7 = textfont2.render("Green apples half the number of apples needed", 1, BLACK)
        GAMESCREEN.blit(instruct7, (135, 355))
        instruct8 = textfont2.render("to advance to the next level!", 1, BLACK)
        GAMESCREEN.blit(instruct8, (135, 385))
        GAMESCREEN.blit(pygame.image.load("yellow_apple.png"), (75,420))
        instruct9 = textfont2.render("Yellow apples give an additional life!", 1, BLACK)
        GAMESCREEN.blit(instruct9, (135, 430))

        # Event handling
        for event in pygame.event.get():
            # Quit game if close button is clicked
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Back Button clicked
                if m_x > 325 and m_x < 475 and m_y > 515 and m_y < 585:
                    gamestart = 0

    # Update the gamescreen
    pygame.display.update()

    # Limits framerate
    clock.tick(20)
pygame.display.quit()
sys.exit()



