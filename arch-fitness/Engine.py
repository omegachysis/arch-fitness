#!/usr/bin/env python3

import pygame
import sys
from pygame.locals import *
import traceback

def main():
    game = Game(640, 480)
    testApp = Application()
    game.startApp(testApp)
    game.run()

class Game(object):
    
    def __init__(self, width, height):
        self.canvas = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

        Application.canvas = self.canvas
        Application.game = self
        Sprite.game = self

        self.app = None
        
    def startApp(self, application):
        self.app = application
        
    def run(self):
        while True:
            dt = self.clock.get_time()
            
            if self.app:
                self.app.update(dt)
                self.app.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

            pygame.display.update()
            self.clock.tick(0)

class Application(object):
    canvas = None
    game = None
    def __init__(self):
        self.sprites = []
        self.width, self.height = Application.canvas.get_size()
        self.backgroundSurface = None
        self.backgroundColor = (0,0,0,255)
        
        self.canvas = Application.canvas
        
    def addSprite(self, sprite):
        sprite.app = self
        self.sprites.append(sprite)
    def removeSprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
    
    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)
    def draw(self):
        if self.backgroundSurface:
            self.canvas.blit(self.backgroundSurface, (0,0))
        elif self.backgroundColor:
            self.canvas.fill(self.backgroundColor)
        
        for sprite in self.sprites:
            sprite.draw(self.canvas)

class Sprite(object):
    game = None
    def __init__(self, app, x, y, surface):
        self.app = app
        
        self.surface = surface
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0
    
    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
    
    def draw(self, canvas):
        canvas.blit(self.surface, self.rect)

    # ----------------------------------------------
    # Setup class properties
    
    def getX(self):
        return self._x
    def setX(self, x):
        self._x = x
    def getY(self):
        return self._y
    def setY(self, y):
        self._y = y
    x = property(getX, setX)
    y = property(getY, setY)

    def getLeft(self):
        return self._x - self._width / 2
    def setLeft(self, left):
        self._x = left + self._width / 2
    def getRight(self):
        return self._x + self._width / 2
    def setRight(self, right):
        self._x = right - self.width / 2
    def getTop(self):
        return self._y - self._height / 2
    def setTop(self, top):
        self._y = top + self._height / 2
    def getBottom(self):
        return self._y + self._height / 2
    def setBottom(self, bottom):
        self._y = bottom - self._height / 2
    left = property(getLeft, setLeft)
    right = property(getRight, setRight)
    top = property(getTop, setTop)
    bottom = property(getBottom, setBottom)

    def getSurface(self):
        return self._surface
    def setSurface(self, surface):
        self._surface = surface
        self._width = surface.get_width()
        self._height= surface.get_height()
        self.setRect(surface.get_rect())
    surface = property(getSurface, setSurface)

    def getRect(self):
        self._rect.centerx = self._x
        self._rect.centery = self._y
        return self._rect
    def setRect(self, rect):
        self._rect = rect
    rect = property(getRect, setRect)

    #---------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except:
        print (traceback.format_exc())
        input ()
