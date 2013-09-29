#Prototype2
#Created By: Paul Tai
#HackNY - 09.29.2013

import pygame, sys, random
from pygame.locals import *
from math import sqrt

pygame.init()
fpsClock = pygame.time.Clock()
X_MAX = 800
Y_MAX = 600
ZOMBIES = []
LUNGERS = []
CHASERS = []
HUMANS = []
SOLDIERS = []
BULLETS = []
HEALTH = 10
FPS = 60
speed = 2
direction = 1
infectRange = 15
score = 0

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

while True:
	runClock += 1
	windowSurfaceObj.fill(blackColor)
	
	msgSurfaceObj = fontObj.render("P",False,whiteColor)
	msgSurfaceObj2 = fontObj.render("Health " + str(HEALTH) + " of 10",False,whiteColor)
	textRect = msgSurfaceObj.get_rect()
	textRect2 = msgSurfaceObj2.get_rect()
	textRect2.center = (X_MAX/2, Y_MAX-100)
	textRect.center = (playerX, playerY)
	windowSurfaceObj.blit(msgSurfaceObj,textRect)
	windowSurfaceObj.blit(msgSurfaceObj2,textRect2)
	pygame.draw.rect(windowSurfaceObj,whiteColor,textRect,1)
	
	for human in HUMANS:
		if( human[0] > X_MAX or human[1] > Y_MAX or human[1] < 0 ):
			alarm += 1
			HUMANS.pop(HUMANS.index(human))
			break
		humanSprite = fontObj.render("H",False,whiteColor)
		textRect.center = (human[0],human[1])
		windowSurfaceObj.blit(humanSprite,textRect)
		distance = None
		closest = 50
		closeZed = None
		for zombie in ZOMBIES:
			distance = sqrt(((zombie[0] - human[0])**2 + (zombie[1]-human[1])**2))
			if( distance < infectRange ):
				ZOMBIES.append(HUMANS.pop(HUMANS.index(human)))
				score+=1
				break
			if( distance < closest ):
				closest = distance
				closeZed = zombie
		
		if(closeZed == None):
			human[1] += int(random.random()*5)
		else:
			if( human > closeZed[0] ):
				human[0] += 3
			else:
				human[0] -= 3
			if( human[1] > closeZed[1] ):
				human[1] += 3
			else:
				human[1] -= 3
	
	if alarm >= 5:
		alarm -= 5
		tempX = int(random.random()*(X_MAX-20)+20)
		SOLDIERS.append([tempX,5])
		tempY = int(random.random()*(Y_MAX-20)+20)
		SOLDIERS.append([5,tempY])
	
	for soldier in SOLDIERS:
		soldierSprite = fontObj.render("S",False,redColor)
		
		textRect.center = (soldier[0],soldier[1])
		windowSurfaceObj.blit(soldierSprite,textRect)
		
		if(runClock % (FPS*2) == 0):
			if(len(CHASERS) > 0):
				targetZed = CHASERS[int(random.random()*len(CHASERS))]
				pygame.draw.line(windowSurfaceObj, redColor, (soldier[0], soldier[1]), (targetZed[0],targetZed[1]),2)
				CHASERS.pop(CHASERS.index(targetZed))
			else:
				target = int(random.random()*((len(ZOMBIES) +1)))
				if (target < len(ZOMBIES)):
					targetZed = ZOMBIES[target]
					pygame.draw.line(windowSurfaceObj, redColor, (soldier[0], soldier[1]), (targetZed[0],targetZed[1]),2)
					ZOMBIES.pop(ZOMBIES.index(targetZed))
				elif(target >= (len(ZOMBIES))):
					HEALTH -= 1
					pygame.draw.line(windowSurfaceObj, redColor, (soldier[0],soldier[1]),(playerX,playerY),3)
				
			

	for zombie in ZOMBIES:
		zombieSprite = fontObj.render("Z",False,whiteColor)
		pygame.draw.circle(windowSurfaceObj, whiteColor, (zombie[0],zombie[1]),infectRange,1)
		textRect.center = (zombie[0],zombie[1])
		windowSurfaceObj.blit(zombieSprite,textRect)
		if len(HUMANS) != 0:
			target = HUMANS[0]
			min = sqrt((zombie[0] - human[0])**2 + (zombie[1]-human[1])**2)
			for human in HUMANS:
				if( sqrt(((zombie[0] - human[0])**2 + (zombie[1]-human[1])**2)) < min ):
					target = human
			if( target != None ):
				if( zombie[0] > target[0] ):
					zombie[0] -= 2
				else:
					zombie[0] += 2
				if( zombie[1] > target[1] ):
					zombie[1] -= 2
				else:
					zombie[1] += 2
	
	for lunger in LUNGERS:
		ZOMBIES.append(LUNGERS.pop(LUNGERS.index(lunger)))
	"""	pygame.draw.circle(windowSurfaceObj, blueColor, (lunger[0],lunger[1]),infectRange*2,1)
		zombieSprite = fontObj.render("Z",False,blueColor)
		textRect.center = (lunger[0],lunger[1])
		windowSurfaceObj.blit(zombieSprite,textRect)
		if len(HUMANS) != 0:
			min = HUMANS[0]
		for human in HUMANS:
			if( sqrt(((lunger[0] - human[0])**2 + (lunger[1]-human[1])**2)) < (infectRange*2) ):
				lunger[0]=human[0]
				lunger[1]=human[1]
				score+=1
				typeZ = int(random.random()*7)
				temp =HUMANS.pop(HUMANS.index(human))
				if(typeZ == 5):
					LUNGERS.append(temp)
				if(typeZ == 6):
					CHASERS.append(temp)
				else:
					ZOMBIES.append(temp)
				break	
	"""

	for zombie in CHASERS:
		zombieSprite = fontObj.render("Z",False,yellowColor)
		pygame.draw.circle(windowSurfaceObj, yellowColor, (zombie[0],zombie[1]),infectRange,1)
		textRect.center = (zombie[0],zombie[1])
		windowSurfaceObj.blit(zombieSprite,textRect)
		
		if( zombie[0] > mousex ):
			zombie[0] -= 3
		else:
			zombie[0] += 3
		if( zombie[1] > mousey ):
			zombie[1] -= 3
		else:
			zombie[1] += 3
					
		for soldier in SOLDIERS:
			if( sqrt(((zombie[0] - soldier[0])**2 + (zombie[1]-soldier[1])**2)) < (infectRange) ):
				temp = SOLDIERS.pop(SOLDIERS.index(soldier))
				score+=1
				typeZ = int(random.random()*7)
				if(typeZ == 3):
					LUNGERS.append(temp)
				if(typeZ == 4):
					CHASERS.append(temp)
				else:
					ZOMBIES.append(temp)
				break
		for human in HUMANS:
			if( sqrt(((zombie[0] - human[0])**2 + (zombie[1]-human[1])**2)) < (infectRange) ):
				temp = HUMANS.pop(HUMANS.index(human))
				score+=1
				typeZ = int(random.random()*7)
				if(typeZ == 3):
					LUNGERS.append(temp)
				if(typeZ == 4):
					CHASERS.append(temp)
				else:
					ZOMBIES.append(temp)
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
			#		if event.button == 1:
						#bite human
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
			#if event.key == K_LEFT:
			#	playerX -= speed
			#if event.key == K_RIGHT:
			#	playerX +=speed
			#if event.key == K_UP:
			#	playerY -= speed
			#if event.key == K_DOWN:
			#	playerY += speed
			#if event.key == K_SPACE:
			#	pass
			
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[K_a]:
		playerX -= speed
	if keys_pressed[K_d]:
		playerX += speed
	if keys_pressed[K_w]:
		playerY -= speed
	if keys_pressed[K_s]:
		playerY += speed	

	for human in HUMANS:
		if( sqrt((playerX - human[0])**2 + (playerY-human[1])**2) < (2*infectRange) ):
			temp = HUMANS.pop(HUMANS.index(human))
			typeZ = int(random.random()*7)
			if(typeZ == 3):
				LUNGERS.append(temp)
			if(typeZ == 4):
				CHASERS.append(temp)
			else:
				ZOMBIES.append(temp)
			HEALTH+=1
			score+=1
					
	for soldier in SOLDIERS:
		if( sqrt((playerX - soldier[0])**2 + (playerY-soldier[1])**2) < (2*infectRange) ):
			temp = SOLDIERS.pop(SOLDIERS.index(soldier))
			typeZ = int(random.random()*7)
			if(typeZ == 3):
				LUNGERS.append(temp)
			if(typeZ == 4):
				CHASERS.append(temp)
			else:
				ZOMBIES.append(temp)
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
		HUMANS.append([tempX,0])
