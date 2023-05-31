import pygame
pygame.init()

from pygame import mixer
mixer.init()

import random

import globals
import data as sampleData
import brain
import goz

ASSETS = {'zombie':"assets/zombie.wav", 'brains': "assets/brains.wav", 'nice': "assets/nice.mp3", 'scary':"assets/scary.mp3"}

INFECTION_ROLL = 666
MIN_TIME_TO_INFECTION = 300
ZOMBIE_TIMER = 600

data = sampleData.Data()

############################################################################
# "Is this coordinate safe from infection" function
#
def isSafe(x,y):
    return data.isSafe( x,y )
    
############################################################################

############################################################################
# Sample
#
def checkSample():
    global brain

    sample = data.getSample()

    inputs = [ sample['x'], sample['y'], 1 ]
    
    answer = 1
    if sample['type'] == sampleData.INFECTED:
        answer = 0

    brain.train(inputs, answer)
    
    calculateFence()

############################################################################

def isInfected( x,y ):
    global minInfectionTimer
    global hasZombies
    if minInfectionTimer == MIN_TIME_TO_INFECTION:

        roll = random.randint(0,10000)
        if roll == INFECTION_ROLL:

            if not isSafe( x - globals.SCREEN_CENTER_X, globals.SCREEN_CENTER_Y - y ):
                if not hasZombies:
                    mixer.Sound.play(zombieSound)
                    mixer.music.load(ASSETS['scary'])
                    mixer.music.play()
                    hasZombies = True
                return True
    
    return False

def isBehindFence(x,y):
    global brain

    prediction = brain.getPrediction( [x - globals.SCREEN_CENTER_X, globals.SCREEN_CENTER_Y - y, 1])
    
    if prediction > 0:
        return True
    else:
        return False

def drawCell(color, x, y, size):
    global screen
    pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size) )
           

def calculateFence():
    global brain
    global fencePoints
 
    y1 = brain.getY(-globals.SCREEN_CENTER_X)
    y2 = brain.getY(globals.SCREEN_CENTER_X)  

    screenY1 = globals.SCREEN_CENTER_Y - y1
    screenY2 = globals.SCREEN_CENTER_Y - y2

    fencePoints[0] = ( 0, screenY1 + 2 )
    fencePoints[1] = ( globals.SCREEN_WIDTH, screenY2 + 2 )

############################################################################

brain = brain.Brain()

goz = goz.GameOfZombie()

screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))

showCells = False
isEvolving = False
evolutionRate = 10
evolutionCounter = 0

fencePoints = [(0,0), (0,0)]

calculateFence()

isTraining = True

hasZombies = False
zombieSoundCounter = 0
minInfectionTimer = 0
zombieTimer = ZOMBIE_TIMER

fogColor = globals.FIELD_COLOR

brainSound = mixer.Sound(ASSETS['brains'])
brainSound.set_volume(0.4)

zombieSound = mixer.Sound(ASSETS['zombie'])
zombieSound.set_volume(0.5)

mixer.music.set_volume(0.3)
mixer.music.load(ASSETS['nice'])

clock = pygame.time.Clock()
FPS = 60

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if isTraining:
                    checkSample()
            if event.key == pygame.K_t:
                if showCells:
                    goz.updateCells(isInfected, isBehindFence)
            if event.key == pygame.K_r:
                if showCells:
                    isEvolving = not(isEvolving)
            if event.key == pygame.K_g:
                mixer.music.play()
                showCells = True
                isEvolving = False
                isTraining = False
                goz.seedCells()

    if isEvolving:
        if minInfectionTimer < MIN_TIME_TO_INFECTION:
            minInfectionTimer += 1

        if evolutionCounter < evolutionRate:
            evolutionCounter += 1
        else:
            goz.updateCells(isInfected, isBehindFence)
            evolutionCounter = 0

    if hasZombies:
        screen.fill(fogColor)
        r = max(25, fogColor[0] - 1)
        g = max(30, fogColor[1] - 1)
        b = max(25, fogColor[2] - 1)

        fogColor = (r,g,b)

    else:
        screen.fill(globals.FIELD_COLOR)

    if isTraining:
        for sample in data.samples:
            x = sample['x'] + globals.SCREEN_CENTER_X
            y = globals.SCREEN_CENTER_Y - sample['y']

            color = sample['color']
            
            if sample['checked'] == sampleData.CHECKED:
                pygame.draw.circle(screen, color, (x,y), 10)

    if showCells:
        goz.drawCells(drawCell)    

    pygame.draw.line(screen, globals.FENCE_COLOR, fencePoints[0], fencePoints[1], width = 3) 
    
    if hasZombies:
        if zombieSoundCounter == zombieTimer:
            mixer.Sound.play(brainSound)
            zombieSoundCounter = 0
            zombieTimer = ZOMBIE_TIMER + random.randint(60,600)
        else:
            zombieSoundCounter += 1

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()     