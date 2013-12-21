#!/usr/bin/env python3

##   Copyright 2013 Matthew A. Robinson
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

import pygame
import sys
from pygame.locals import *
from pygame import transform
import pygame.freetype
import traceback
import logging

from Motion.Action import Action

import Debug
#import Interface
import Console
import Sprite

log = logging.getLogger("R.Engine")

class Game(object):
    
    def __init__(self, width, height, fullscreen=False):
        log.info("initializing game engine")

        self.width = width
        self.height = height

        self.quitting = False
        
        pygame.init()
        
        if fullscreen:
            self.canvas = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            self.canvas = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

        self.gameConsole = Console.GameConsole(self, Debug.levelGameConsole)

        Application.canvas = self.canvas
        Application.game = self
        Sprite.Sprite.game = self

        self.app = None

    def xprop(self, proportion):
        return int(self.width * proportion)
    def yprop(self, proportion):
        return int(self.height * proportion)

    def execute(self, c, command):
        exec(command)
        
    def startApp(self, application):
        self.app = application

    def postEvent(self, event):
        log.info("posted event - " + repr(event))
        pygame.event.post(pygame.event.Event(event))
        
    def run(self):
        log.info("starting main loop")
        while True:
            dt = self.clock.get_time()
            
            if self.app:
                self.app.update(dt)
                self.app.draw()
            if not self.gameConsole.hidden:
                self.gameConsole.draw(self.canvas)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.postEvent(QUIT)
                    elif event.key == K_BACKQUOTE:
                        self.gameConsole.toggleHidden()
                    elif event.key == K_RETURN:
                        if not self.gameConsole.hidden:
                            self.gameConsole.executeEntry()
                    elif event.key == K_BACKSPACE:
                        if not self.gameConsole.hidden:
                            self.gameConsole.entryBackspace()
                    else:
                        if not self.gameConsole.hidden:
                            self.gameConsole.entryAdd(event.unicode)

            pygame.display.update()
            self.clock.tick(0)

    def quit(self):
        log.info("running game.quit")
        self.quitting = True
        pygame.quit()
        sys.exit(0)

class Application(object):
    canvas = None
    game = None
    def __init__(self):
        self._layers = []
        self.layers = {}
        self.registrar = {}

        log.info("initializing application")
        
        self.width, self.height = Application.canvas.get_size()
        self.backgroundsurface = None
        self.backgroundColor = (0,0,0,255)
        
        self.canvas = Application.canvas

        self.addLayer("default")

    def execute(self, c, command):
        exec(command)

    def getLayerlevel(self, layer):
        return self._layers.index(layer)

    def addLayer(self, name, level=0):
        log.info("adding new layer '%s' on level %d"%(name,level))
        layer = Layer(name)
        layer.app = self
        self.layers[name] = layer
        self._layers.append(layer)
        layer.level = len(self.layers) - 1
        # by default, new layers are created on top.
        # smaller level values mean higher up (cannot be negative)
        layer.setLevel(level)
        
    def removeLayer(self, layer):
        log.info("removing layer '%s' on level %d"%(layer.name, layer.level))
        layer = self.getLayer(layer)
        self._layers.remove(layer)
        del self.layers[layer.name]
        
    def renameLayer(self, layer, name):
        log.info("renaming layer '%s' to new name '%s'"%(layer.name,name))
        del self.layers[layer.name]
        self.layers[name] = layer
        
    def moveLayer(self, layer, level):
        log.info("moving layer '%s' to level %d"%(layer.name,level))
        layer = self.getLayer(layer)
        
        if level < -1:
            level = len(self._layers) - level
        
        if level >= len(self._layers) or level == -1:
            self._layers.append(layer)
        else:
            self._layers = self._layers[:level] + [layer] + self._layers[level:]
            
        self.layers[layer.name] = layer

    def getLayer(self, layer):
        if isinstance(layer, Layer):
            return layer
        elif isinstance(layer, str):
            return self.layers[layer]
        elif isinstance(layer, int):
            return self._layers[layer]
        else:
            return None

    def registerSprite(self, sprite, name):
        sprite._name = name
        log.debug("registering sprite '%s'"%(sprite.name))
        self.registrar[name.lower()] = sprite
    def unregisterSprite(self, sprite):
        log.debug("unregistering sprite '%s'"%(sprite.name))
        if sprite.name.lower() in self.registrar:
            log.debug("sprite of name '%s' unregistered successfully"%(sprite.name))
            del self.registrar[sprite.name.lower()]
        else:
            log.warning("sprite of name '%s' is not in application"%(sprite.name))
    def renameSprite(self, sprite, newName):
        sprite._name = newName
        log.debug("renaming sprite '%s' to new name '%s'"%(sprite.name, newName))
        if sprite.name.lower() in self.registrar:
            del self.registrar[sprite.name.lower()]
        else:
            if sprite.name != None:
                log.warning("sprite of name '%s' is not in application"%(sprite.name))
        self.registrar[newName] = sprite
    def reg(self, name):
        if name.lower() in self.registrar:
            return self.registrar[name.lower()]
        else:
            log.warning("sprite of name '%s' is not in application"%(name))

    def addSprite(self, sprite, layer=0):
        log.debug("adding sprite to layer %s"%(layer))
        if sprite.name != None:
            self.registerSprite(sprite, sprite.name)
        if isinstance(layer, Layer):
            layer.addSprite(sprite)
        elif isinstance(layer, str):
            self.layers[layer].addSprite(sprite)
        elif isinstance(layer, int):
            self._layers[layer].addSprite(sprite)
        else:
            pass
        
    def removeSprite(self, sprite):
        log.debug("removing sprite on level %d"%(sprite.layer.level))
        self._layers[sprite.layer.level].removeSprite(sprite)
        self.unregisterSprite(sprite)
    
    def update(self, dt):
        dt /= 1000.0
        i = len(self._layers)
        while i > 0:
            i -= 1
            self._layers[i].update(dt)
                
    def draw(self):
        if self.backgroundsurface:
            self.canvas.blit(self.backgroundsurface, (0,0))
        elif self.backgroundColor:
            self.canvas.fill(self.backgroundColor)
        
        i = len(self._layers)
        while i > 0:
            i -= 1
            self._layers[i].draw(Application.canvas)

class Layer(object):
    def __init__(self, name):
        self.sprites = []
        self._name = name
        self.app = None

    def getLevel(self):
        return self.app.getLayerlevel(self)
    def setLevel(self, level):
        if level != self.getLevel():
            self.app.moveLayer(self, level)
    level = property(getLevel, setLevel)

    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        self.app.renameLayer(self, name)
    name = property(getName, setName)

    def addSprite(self, sprite):
        sprite.app = self.app
        sprite.layer = self
        self.sprites.append(sprite)

    def removeSprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.tick(dt)
    def draw(self, canvas):
        for sprite in self.sprites:
            sprite.draw(canvas)

##def main():
##    import Motion
##
##    game = Game(1600, 900, True)
##    
##    testApp = Application()
##    testApp.backgroundColor = (0, 0, 50, 255)
##
##    testsurface = pygame.image.load("test.png")
##    testSprite = Sprite(testsurface.convert(), 250, 250)
##    testSprite.alpha = 255
##
##    testApp.addSprite(testSprite, 0) # add to top layer - 0
##
##    testText = Text("Hello World!", 200, 100, (255,255,255,255),
##                    50, "consola.ttf")
##
##    exitButton = Interface.SolidButton(400, 200, 50, 50,
##                             (255,0,0,255), (255,0,255,255), (0,255,0,255),
##                             game.quit)
##
##    exitButton.text = Text("X", 50, 50, (255,255,255,255), 50, "consola.ttf")
##
##    testApp.addSprite(exitButton)
##
##    testApp.addSprite(testText, "default") # add to default layer
##
##    testText = Text("Hello World!", 200, 200, (255,255,255,255),
##                    50, "consola.ttf")
##
##    testApp.addLayer("top layer", 0)
##
##    testApp.addSprite(testText, "top layer")
##
##    newMotion = Motion.looped(Motion.In.Fade(testSprite, 5.0, 255), 0)
##
##    #---------------------------------------
##
##    global subjectSprite
##    global subjectMotion
##
##    subjectSprite = Sprite(testsurface.convert(), 500, 500)
##    testApp.addSprite(subjectSprite)
##
##    def start():
##        Motion.looped(Motion.In.Fade(subjectSprite, 4.0, 255), 0)
##    def stop():
##        subjectSprite.removeMotion("in.fade")
##
##    startButton = Interface.SolidButton(400, 600, 100, 50,
##                              (0,255,0,255), (50,255,50,255), (100,255,100,255),
##                              start)
##    stopButton = Interface.SolidButton(600, 600, 100, 50,
##                             (255,0,0,255), (255,50,50,255), (255,100,100,255),
##                             stop)
##
##    testApp.addSprite(startButton)
##    testApp.addSprite(stopButton)
##    
##    game.startApp(testApp)
##    game.run()

##if __name__ == "__main__":
##    Debug.test(main)
