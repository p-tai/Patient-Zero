#Prototype2
#Created By: Paul Tai, Matt Robinson, Ed Choi
#HackNY - 09.29.2013

import pygame, sys, random
from pygame.locals import *
from math import sqrt

pygame.init()
fpsClock = pygame.time.Clock()
X_MAX = 800
Y_MAX = 600
zombies = []
lungers = []
chasers = []
humans = []
soldiers = []
bullets = []
FPS = 60
ZSPEED = 2
HSPEED = 3
HEALTH = 10
direction = 1
infectRange = 15
score = 0
hunger = 0
hungertime = 100

windowSurfaceObj = pygame.display.set_mode((X_MAX,Y_MAX))

pygame.display.set_caption( "Patient 0")

alarm = 1

blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
yellowColor = pygame.Color(255,255,0)
blueColor = pygame.Color(0,255,255)

mousex,mousey = 0,0
playerX, playerY = X_MAX/2, Y_MAX/2

clock = pygame.time.Clock()
runClock = 0

TEXTCOLOR = "white"
fontObj = pygame.font.Font('freesansbold.ttf',32)

class Entity(object):
    def __init__(self, xpos, ypos, speed, sprite=None):
        self.speed = speed
        self.xpos = xpos
        self.ypos = ypos
        if sprite is not None:
            self.sprite = sprite
            self.rect = sprite.get_rect()
            self.rect.center = (xpos, ypos)

    def kill(self, ent):
        pass

    def get_position(self):
        return (self.xpos, self.ypos)

    def move(self, xdelt=0, ydelt=0):
        self.xpos += xdelt
        self.ypos += ydelt
        self.rect.center = (self.xpos, self.ypos)

    def setPos(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.rect.center = (xpos, ypos)

class Zombie(Entity):
    def __init__(self, xpos, ypos, speed=ZSPEED, sprite=fontObj.render("Z",False,whiteColor)):
        super(Zombie, self).__init__(xpos, ypos, speed, sprite)

class Lunger(Zombie):
    def __init__(self, xpos, ypos, speed=ZSPEED, sprite=fontObj.render("Z",False,blueColor)):
        super(Lunger, self).__init__(xpos, ypos, speed, sprite)

class Chaser(Zombie):
    def __init__(self, xpos, ypos, speed=ZSPEED, sprite=fontObj.render("Z",False,yellowColor)):
        super(Chaser, self).__init__(xpos, ypos, speed, sprite)

class Player(Entity):
    def __init__(self, xpos, ypos, speed=HSPEED, sprite=fontObj.render("P",False,whiteColor)):
        super(Player, self).__init__(xpos, ypos, speed, sprite)

class Human(Entity):
    def __init__(self, xpos, ypos, speed=HSPEED, sprite=fontObj.render("H", False, whiteColor)):
        super(Human, self).__init__(xpos, ypos, speed, sprite)

class Soldier(Human):
    def __init__(self, xpos, ypos, speed=0, sprite=fontObj.render("S",False,redColor)):
        super(Soldier, self).__init__(xpos, ypos, speed, sprite)

player = Player(playerX, playerY)

while True:
    runClock += 1
    windowSurfaceObj.fill(blackColor)
    msgSurfaceObj = fontObj.render("Score: " + str(score),False,whiteColor)
    msgSurfaceObj2 = fontObj.render("Health: " + str(HEALTH) + " of 10",False,whiteColor)
    textRect = msgSurfaceObj.get_rect()
    textRect2 = msgSurfaceObj2.get_rect()
    textRect = (X_MAX/2, Y_MAX-50)
    textRect2.center = (X_MAX/2, Y_MAX-100)
    
    player.setPos(playerX, playerY)
    windowSurfaceObj.blit(player.sprite, player.rect)
    windowSurfaceObj.blit(msgSurfaceObj,textRect)
    windowSurfaceObj.blit(msgSurfaceObj2,textRect2)
    pygame.draw.rect(windowSurfaceObj,whiteColor,player.rect,1)
    
    for human in humans:
        if human.xpos > X_MAX or human.ypos > Y_MAX or human.ypos < 0:
            alarm += 1
            humans.pop(humans.index(human))
            break
        windowSurfaceObj.blit(human.sprite, human.rect)
        distance = None
        closest = 50
        closeZed = None
        for zombie in zombies:
            if runClock % (FPS*1) == 0:
                hunger += 1
            if hunger >= hungertime:
                hunger = 0
                zombies.pop(zombies.index(zombie))
                continue
            distance = sqrt(((zombie.xpos - human.xpos)**2 + (zombie.ypos-human.ypos)**2))
            if distance < infectRange :
                hunger = 0
                temp = humans.pop(humans.index(human))
                zombies.append(Zombie(temp.xpos, temp.ypos))
                score+=1
                break
            if distance < closest:
                closest = distance
                closeZed = zombie
        
        if(closeZed == None):
            human.move(0, int(random.random()*5))
        else:
            if( human > closeZed.xpos ):
                human.move(3, 0)
            else:
                human.move(-3, 0)
            if( human.ypos > closeZed.ypos ):
                human.move(0, 3)
            else:
                human.move(0, -3)
    
    if alarm >= 5:
        alarm -= 5
        tempX = int(random.random()*(X_MAX-20)+20)
        soldiers.append(Soldier(tempX, 5))
        tempY = int(random.random()*(Y_MAX-20)+20)
        soldiers.append(Soldier(5, tempY))
    
    for soldier in soldiers:
        windowSurfaceObj.blit(soldier.sprite, soldier.rect)
        
        if(runClock % (FPS*2) == 0):
            if(len(chasers) > 0):
                targetZed = chasers[int(random.random()*len(chasers))]
                pygame.draw.line(windowSurfaceObj, redColor, (soldier.xpos, soldier.ypos), (targetZed.xpos,targetZed.ypos), 2)
                chasers.pop(chasers.index(targetZed))
            else:
                target = int(random.random()*((len(zombies) +1)))
                if (target < len(zombies)):
                    targetZed = zombies[target]
                    pygame.draw.line(windowSurfaceObj, redColor, (soldier.xpos, soldier.ypos), (targetZed.xpos, targetZed.ypos), 2)
                    zombies.pop(zombies.index(targetZed))
                elif(target >= (len(zombies))):
                    HEALTH -= 1
                    pygame.draw.line(windowSurfaceObj, redColor, (soldier.xpos, soldier.ypos),(playerX, playerY), 3)
                
            

    for zombie in zombies:
        pygame.draw.circle(windowSurfaceObj, whiteColor, (zombie.xpos,zombie.ypos),infectRange,1)
        windowSurfaceObj.blit(zombie.sprite,zombie.rect)
        if len(humans) != 0:
            target = humans[0]
            min = sqrt((zombie.xpos - human.xpos)**2 + (zombie.ypos-human.ypos)**2)
            for human in humans:
                if( sqrt(((zombie.xpos - human.xpos)**2 + (zombie.ypos-human.ypos)**2)) < min ):
                    target = human
            if( target != None ):
                if( zombie.xpos > target.xpos ):
                    zombie.move(-zombie.speed, 0)
                else:
                    zombie.move(zombie.speed, 0)
                if( zombie.ypos > target.ypos ):
                    zombie.move(0, -zombie.speed)
                else:
                    zombie.move(0, zombie.speed)
    
    for lunger in lungers:
        pygame.draw.circle(windowSurfaceObj, blueColor, (lunger.xpos,lunger.ypos),infectRange*2,1)
        windowSurfaceObj.blit(lunger.sprite, lunger.rect)
        for human in humans:
            if runClock % (FPS*1) == 0:
                hunger += 1
            if hunger >= hungertime:
                hunger = 0
                lungers.pop(lungers.index(lunger))
                break
            if( sqrt(((lunger.xpos - human.xpos)**2 + (lunger.ypos-human.ypos)**2)) < (infectRange*2) ):
                hunger = 0
                lunger.setPos(human.xpos, human.ypos)
                score+=1
                typeZ = int(random.random()*7)
                temp =humans.pop(humans.index(human))
                if(typeZ == 5):
                    lungers.append(Lunger(temp.xpos, temp.ypos))
                if(typeZ == 6):
                    chasers.append(Chaser(temp.xpos, temp.ypos))
                else:
                    zombies.append(Zombie(temp.xpos, temp.ypos))
                break    

    for zombie in chasers:
        pygame.draw.circle(windowSurfaceObj, yellowColor, (zombie.xpos,zombie.ypos),infectRange,1)
        windowSurfaceObj.blit(zombie.sprite,zombie.rect)
        
        if( zombie.xpos > mousex ):
            zombie.move(-zombie.speed, 0)
        else:
            zombie.move(zombie.speed, 0)
        if( zombie.ypos > mousey ):
            zombie.move(0, -zombie.speed)
        else:
            zombie.move(0, zombie.speed)
                    
        for soldier in soldiers:
            if( sqrt(((zombie.xpos - soldier.xpos)**2 + (zombie.ypos-soldier.ypos)**2)) < (infectRange) ):
                temp = soldiers.pop(soldiers.index(soldier))
                score+=1
                typeZ = int(random.random()*7)
                if(typeZ == 3):
                    lungers.append(Lunger(temp.xpos, temp.ypos))
                if(typeZ == 4):
                    chasers.append(Chaser(temp.xpos, temp.ypos))
                else:
                    zombies.append(Zombie(temp.xpos, temp.ypos))
                break
        for human in humans:
            if( sqrt(((zombie.xpos - human.xpos)**2 + (zombie.ypos-human.ypos)**2)) < (infectRange) ):
                temp = humans.pop(humans.index(human))
                score+=1
                typeZ = int(random.random()*7)
                if(typeZ == 3):
                    lungers.append(Lunger(temp.xpos, temp.ypos))
                if(typeZ == 4):
                    chasers.append(Chaser(temp.xpos, temp.ypos))
                else:
                    zombies.append(Zombie(temp.xpos, temp.ypos))
                break
        
    
    
    if (HEALTH <= 0):
        pygame.event.post(pygame.event.Event(QUIT))
            
    for event in pygame.event.get():
        if event.type == QUIT:
                msg = "\nGAME OVER" + "\nZOMBIES SPAWNED = " + str(score)
                print(msg)
                pygame.quit()
                sys.exit()          
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
                    
            #elif event.type == MOUSEBUTTONUP:
            #        if event.button == 1:
                        #bite human
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            #if event.key == K_LEFT:
            #    playerX -= speed
            #if event.key == K_RIGHT:
            #    playerX +=speed
            #if event.key == K_UP:
            #    playerY -= speed
            #if event.key == K_DOWN:
            #    playerY += speed
            #if event.key == K_SPACE:
            #    pass
            
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_a]:
        playerX -= player.speed
    if keys_pressed[K_d]:
        playerX += player.speed
    if keys_pressed[K_w]:
        playerY -= player.speed
    if keys_pressed[K_s]:
        playerY += player.speed    

    for human in humans:
        if( sqrt((playerX - human.xpos)**2 + (playerY-human.ypos)**2) < (2*infectRange) ):
            temp = humans.pop(humans.index(human))
            typeZ = int(random.random()*7)
            if(typeZ == 3):
                lungers.append(Lunger(temp.xpos, temp.ypos))
            if(typeZ == 4):
                chasers.append(Chaser(temp.xpos, temp.ypos))
            else:
                zombies.append(Zombie(temp.xpos, temp.ypos))
            HEALTH+=1
            score+=1
                    
    for soldier in soldiers:
        if( sqrt((playerX - soldier.xpos)**2 + (playerY-soldier.ypos)**2) < (2*infectRange) ):
            temp = soldiers.pop(soldiers.index(soldier))
            typeZ = int(random.random()*7)
            if(typeZ == 3):
                lungers.append(Lunger(temp.xpos, temp.ypos))
            if(typeZ == 4):
                chasers.append(Chaser(temp.xpos, temp.ypos))
            else:
                zombies.append(Zombie(temp.xpos, temp.ypos))
            HEALTH+=1
            score+=1

    fpsClock.tick(FPS)
    pygame.display.update()

    if(HEALTH > 10):
        HEALTH = 10
        
    if(playerX < 0):
        playerX = 0
    elif(playerX > X_MAX):
        playerX = X_MAX
    if(playerY < 0):
        playerY = 0
    elif(playerY > Y_MAX):
        playerY = Y_MAX
    
    if(score >=100):
        msg = "\nZOMBIES HAVE TAKEN OVER THE CITY"
        print(msg)
        pygame.event.post(pygame.event.Event(QUIT))
        
        
    if(runClock % FPS*5 == 0):
        tempX = int(random.random()*X_MAX)
        humans.append(Human(tempX, 0))
