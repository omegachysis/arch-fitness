
import pygame
import sys
from pygame.locals import *

class Application(object):
    def __init__(self, canvas, width, height):
        self.sprites = []
        self.width = width
        self.height = height
        self.backgroundSurface = None
        self.backgroundColor = (0,0,0,255)
        self.canvas = canvas
        
    def addSprite(self, sprite):
        sprite.app = self
        self.sprites.append(sprite)
    def removeSprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
    
    def update(self):
        for sprite in self.sprites:
            sprite.update()
    def draw(self):
        if self.backgroundSurface:
            self.canvas.blit(self.backgroundSurface, (0,0))
        elif self.backgroundColor:
            self.canvas.fill(slef.backgroundColor)
        
        for sprite in self.sprites:
            sprite.draw()

class Sprite(object):
    def __init__(self, app, x, y, surface):
        self.app = app
        
        self.surface = surface
        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0
    
    def update(self):
        self.x += self.dx * app.dt
        self.y += self.dy * app.dt
    
    def draw(self):
        self.app.canvas.blit(self.surface, self.rect)

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
