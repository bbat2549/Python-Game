#Author:       Bruce Batson
#Date:         12/6/2013
#Program Name: pong.py

background_image_filename = 'images.jpg'


import pygame, sys, random
from pygame.locals import *

#used to draw text to the screen
def drawText(text, font, surface, x, y): 
    textobj = font.render(text, 1, WHITE) 
    textrect = textobj.get_rect() 
    textrect.topleft = (x, y) 
    surface.blit(textobj, textrect)

#will randomly pick a number. If one, it will return true, else false
def changeDirction():
    num = random.randint(1, 2)
    if num == 1:
        return True
    else:
        return False

#used to end the game
def terminate(): 
    pygame.quit() 
    sys.exit()

#used to wait for the player to hit a key. If escape is pressed, end game
def waitForPlayerToPressKey(): 
    while True: 
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                terminate() 
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: # pressing escape quits 
                    terminate()
                elif event.key ==ord(' '):
                    return     


#set up pygam
pygame.init()
mainClock = pygame.time.Clock()
WINDOWWIDTH = 1000 
WINDOWHEIGHT = 600 
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) 
pygame.display.set_caption("Pong")
Background = pygame.image.load(background_image_filename).convert()

#set up direction and speed variables 
DOWNLEFT = 1 
DOWNRIGHT = 3 
UPLEFT = 7 
UPRIGHT = 9 
movespeed = 6
ballspeed = 2
speedup = 1
maxspeed = 10

#set up players and ball
player = pygame.Rect(100, 100, 25, 75)
player2 = pygame.Rect(900, 100, 25, 75)
ball = {'rect':pygame.Rect(500, 300, 20, 20), 'dir':UPLEFT}

#set up colors
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 

#set fonts
font = pygame.font.SysFont(None, 40)
menufont = pygame.font.SysFont(None, 100)

#draw Opening screen
windowSurface.blit(Background, (0,0))
drawText('PONG', menufont, windowSurface, (WINDOWWIDTH/2) - 100, WINDOWHEIGHT/3)
drawText('When both player are ready, press space to start.', font, windowSurface, 150, (WINDOWHEIGHT/3) + 100)
pygame.display.update()
waitForPlayerToPressKey()
p1win = 0
p2win = 0
while True:

    #Set up scores and movement variables
    p1score = 0;
    p2score = 0;
    moveUp = False 
    moveDown = False 
    moveUp2 = False
    moveDown2 = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN: 
                # change the keyboard variables 
                if event.key == K_UP or event.key == K_LEFT: 
                    moveDown = False 
                    moveUp = True 
                if event.key == K_DOWN or event.key == K_RIGHT: 
                    moveUp = False 
                    moveDown = True
                if event.key == ord('a') or event.key == ord('w'): 
                    moveDown2 = False 
                    moveUp2 = True 
                if event.key == ord('d') or event.key == ord('s'): 
                    moveUp2 = False 
                    moveDown2 = True
            if event.type == KEYUP: 
                if event.key == K_ESCAPE: 
                    pygame.quit() 
                    sys.exit() 
                if event.key == K_UP or event.key == K_LEFT: 
                    moveUp = False 
                if event.key == K_DOWN or event.key == K_RIGHT: 
                    moveDown = False
                if event.key == ord('a') or event.key == ord('w'): 
                    moveUp2 = False 
                if event.key == ord('d') or event.key == ord('s'): 
                    moveDown2 = False 

        #move the player 
        if moveDown and player2.bottom < WINDOWHEIGHT: 
            player2.top += movespeed 
        if moveUp and player2.top > 0: 
            player2.top -= movespeed
        if moveDown2 and player.bottom < WINDOWHEIGHT: 
            player.top += movespeed 
        if moveUp2 and player.top > 0: 
            player.top -= movespeed

        #move the ball
        if ball['dir'] == DOWNLEFT: 
            ball['rect'].left -= ballspeed 
            ball['rect'].top += ballspeed 
        if ball['dir'] == DOWNRIGHT: 
            ball['rect'].left += ballspeed 
            ball['rect'].top += ballspeed 
        if ball['dir'] == UPLEFT: 
            ball['rect'].left -= ballspeed 
            ball['rect'].top -= ballspeed 
        if ball['dir'] == UPRIGHT: 
            ball['rect'].left += ballspeed 
            ball['rect'].top -= ballspeed 

        #check if the ball has move out of the window 
        if ball['rect'].top < 0:
            #ball has moved past the top 
            if ball['dir'] == UPLEFT: 
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT: 
                ball['dir'] = DOWNRIGHT
        if ball['rect'].bottom > WINDOWHEIGHT:
            #ball has moved past the bottom 
            if ball['dir'] == DOWNLEFT: 
                ball['dir'] = UPLEFT 
            if ball['dir'] == DOWNRIGHT: 
                ball['dir'] = UPRIGHT 
        if ball['rect'].left < 0:
            #ball has moved past the l
            ballspeed = 2
            p2score += 1
            ball['rect'].topleft = (500, 300)
            if ball['dir'] == DOWNLEFT: 
                ball['dir'] = DOWNRIGHT 
            if ball['dir'] == UPLEFT: 
                ball['dir'] = UPRIGHT 
        if ball['rect'].right > WINDOWWIDTH:
            #ball has moved past the right side
            ballspeed = 2
            p1score += 1
            ball['rect'].topleft = (500, 300)
            if ball['dir'] == DOWNRIGHT: 
                ball['dir'] = DOWNLEFT 
            if ball['dir'] == UPRIGHT: 
                ball['dir'] = UPLEFT
            
        #check if ball has hit a player
        if player.colliderect(ball['rect']):
            #ball has hit the right side of player
            if ball['dir'] == DOWNLEFT:
                if ballspeed == maxspeed:
                    if changeDirction():
                        ball['dir'] = UPRIGHT
                    else:
                        ball['dir'] = DOWNRIGHT
                else:
                    ball['dir'] = DOWNRIGHT
                    ballspeed += speedup
            if ball['dir'] == UPLEFT:
                if ballspeed == maxspeed:
                    if changeDirction():
                        ball['dir'] = DOWNRIGHT
                    else:
                        ball['dir'] = UPRIGHT
                else:
                    ball['dir'] = UPRIGHT
                    ballspeed += speedup
        if player2.colliderect(ball['rect']):
            #ball has hit the left side of player2
            if ball['dir'] == DOWNRIGHT:
                if ballspeed == maxspeed:
                    if changeDirction():
                        ball['dir'] = UPLEFT
                    else:
                        ball['dir'] = DOWNLEFT
                else:
                    ball['dir'] = DOWNLEFT
                    ballspeed += speedup
            if ball['dir'] == UPRIGHT:
                if ballspeed == maxspeed:
                    if changeDirction():
                        ball['dir'] = DOWNLEFT
                    else:
                        ball['dir'] = UPLEFT
                else:
                    ball['dir'] = UPLEFT
                    ballspeed += speedup
        #draw the ball, players, and background onto the surface 
        windowSurface.blit(Background, (0,0))
        pygame.draw.rect(windowSurface, WHITE, player)
        pygame.draw.rect(windowSurface, WHITE, player2)
        pygame.draw.rect(windowSurface, BLACK, ball['rect'])
        drawText('Player 1: %s' % (p1score), font, windowSurface, 425, 0)
        drawText('Player 2: %s' % (p2score), font, windowSurface, 425, 40)
    
    
        #draw the window onto the screen
        pygame.display.update()

        #Check for winner
        if p1score == 10 or p2score == 10:
            break
        mainClock.tick(60)

    windowSurface.blit(Background, (0,0))
    if p1score > p2score:
        p1win += 1
    else:
        p2win += 1

    drawText('Player 1 wins: %s' % (p1win), menufont,windowSurface, 250, WINDOWHEIGHT/4)
    drawText('Player 2 wins: %s' % (p2win), menufont,windowSurface, 250, (WINDOWHEIGHT/4)+80)
    drawText('When both player are ready, press space to play again.', font, windowSurface, 130, (WINDOWHEIGHT/3) + 100)
    pygame.display.update()
    waitForPlayerToPressKey()
