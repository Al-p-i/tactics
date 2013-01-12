__author__ = 'Alpi'

import pygame, sys, math, random
from pygame.locals import *

TACT_TIME = 30
FIRE_ACCURACY = 0.97
WALK_ACCURACY = 0.7

def distance((x1, y1),(x2, y2)):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.tactNumber = 0
        self.bullets = []
        return

    def tact(self):
        self.tactNumber += 1
        #print 'tact ', self.tactNumber
        for unit in self.player1.units:
            unit.tact()

        for unit in self.player2.units:
            unit.tact()

        for bullet in self.bullets:
            bullet.tact()
        return

class Player:
    def __init__(self, name, color):
        self.units = []
        self.name = name
        self.color = color
        self.enemy = None
        return

class Unit:
    def __init__(self, destination, position): return
    def draw(self): return
    def findAim(self):
        minDistance = self.scope
        closestUnit = None
        for unit in self.player.enemy.units:
            distanceToUnit = distance(self.position, unit.position)
            if(distanceToUnit <= minDistance):
                closestUnit = unit
                minDistance = distanceToUnit
        return closestUnit

    def tact(self):
        self.aim = self.findAim()
        self.move()
        if self.aim != None and self._reloadCounter <= 0:
            self.fire(self.aim)
        self._reloadCounter -= TACT_TIME
        return

    def fire(self, aim):
        FIRE_SOUND.play()
        randomAngle = self.angle + random.random()*(1 - FIRE_ACCURACY)*2*math.pi - (1 - FIRE_ACCURACY)*math.pi
        game.bullets.append(Bullet(self.player, self.position, randomAngle))
        self._reloadCounter = self.recharge
        return

    def move(self):
        if self.aim != None:
            distanceX = self.aim.position[0] - self.position[0]
            distanceY = self.aim.position[1] - self.position[1]
            distanceToEnemy = distance(self.position, self.aim.position)
            if distanceToEnemy > 20:
                if distanceX >= 0:#aim to the right
                    self.angle = math.asin(distanceY/distanceToEnemy)
                else:           #aim to the left
                    self.angle = - math.asin(distanceY/distanceToEnemy) + math.pi
            randomAngle = self.angle + random.random()*(1 - WALK_ACCURACY)*2*math.pi - (1 - WALK_ACCURACY)*math.pi
            dx = math.cos(randomAngle) * self.speed
            dy = math.sin(randomAngle) * self.speed
            self.position = (int(self.position[0] + dx), int(self.position[1] + dy))
        self.draw()
        return

class Marine(Unit):
    def __init__(self, player, position):
        self.speed = 3
        self.health = 1
        self.scope = 200
        self.destination = (0,0)
        self.recharge = 1000
        self.aim = None
        self.angle = 0.0
        self._reloadCounter = 0.0
        self.player = player
        self.position = position
        self.draw()
        self.player.units.append(self)
        return

    def draw(self):
        pygame.draw.circle(windowSurfaceObj, self.player.color, self.position, 4, 2)
        return


class Tank(Unit):
    def __init__(self, player, position):
        self.speed = 2
        self.health = 1
        self.scope = 300
        self.destination = (0,0)
        self.recharge = 4000
        self.aim = None
        self.angle = 0.0
        self._reloadCounter = 0.0
        self.player = player
        self.position = position
        self.draw()
        self.player.units.append(self)
        return

    def draw(self):
        pygame.draw.rect(windowSurfaceObj, self.player.color, (self.position[0] - 5, self.position[1] - 5, 10, 10), 2)
        #pygame.draw.circle(windowSurfaceObj, self.player.color, self.position, 5, 2)
        return


class Bullet():
    def __init__(self, player, position, angle):
        #prevposition = (0,0)
        self.position = (0,0)
        self.speed = 15
        self.player = player
        self.position = position
        self.angle = angle
        self._distanceCovered = 0.0
        self.scope = 300
        return
    def move(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.position = (int(self.position[0] + dx), int(self.position[1] + dy))
        for unit in game.player1.units:
            if distance(self.position, unit.position) < 5:
                game.player1.units.remove(unit)
                #game.bullets.remove(self)
        for unit in game.player2.units:
            if distance(self.position, unit.position) < 5:
                game.player2.units.remove(unit)
                #game.bullets.remove(self)

        self._distanceCovered += self.speed
        if self._distanceCovered >= self.scope:
            game.bullets.remove(self)
        return
    def draw(self):
        pygame.draw.circle(windowSurfaceObj, self.player.color, self.position, 2, 0)
        return
    def tact(self):
        self.move()
        self.draw()
        return


class Entity:
    pass

class Building(Entity):
    def __init__(self):
        self.poly = None
        return

class MusicPlayer:
    playlist = []
    def __init__(self):
        import os
        for songName in os.listdir('./music'):
            if songName[-4:] == '.wav':
                self.playlist.append(songName)
        return

    def next(self):
        if len(self.playlist) != 0:
            songNumber = random.randint(0, len(self.playlist) - 1)
            song = pygame.mixer.Sound('./music/' + self.playlist[songNumber])
            print 'musicalPlayer: ', self.playlist[songNumber]
            song.play()
        else:
            print 'musicalPlayer: playlist is empty'
            return


### initialization ####################################################
pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((800,480))
pygame.display.set_caption('Battle')

#pygame.draw.line(windowSurfaceObj,(10,100,100),(10,200),(20,300),2)
#pygame.display.flip()

planSurfaceObj = pygame.image.load('plan.jpg')
plan = planSurfaceObj.convert()
del planSurfaceObj
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
WHITE = pygame.Color(255,255,255)
FIRE_SOUND = pygame.mixer.Sound('shot.wav')
FIRE_SOUND.set_volume(0.2)

mousex, mousey = 0, 0

#fontObj = pygame.font.Font('')
#soundObj = pygame.mixer.Sound('motherhood.wav')


musicalPlayer = MusicPlayer()
####################################################################



game = Game(Player('Sasha', RED), Player('Roma', BLUE))
game.player1.enemy = game.player2
game.player2.enemy = game.player1
windowSurfaceObj.blit(plan,(0,0))

while True:
    #windowSurfaceObj.fill(WHITE)
    windowSurfaceObj.blit(plan,(-55,-10))
    if not pygame.mixer.get_busy():
        musicalPlayer.next()
    #windowSurfaceObj.blit(catSurfaceObj, (mousex, mousey))
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            rand = random.random()
            if rand < 0.25:
                Marine(game.player1, event.pos)
            elif rand < 0.5:
                Marine(game.player2, event.pos)
            elif rand < 0.75:
                Tank(game.player1, event.pos)
            else:
                Tank(game.player2, event.pos)

    game.tact()
    pygame.display.update()
    fpsClock.tick(TACT_TIME)



