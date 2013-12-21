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
from pygame.locals import *
import sys
import pygame.freetype
import traceback
import logging

import Engine
import Debug
import Interface
import Console
import Sprite

log = logging.getLogger("R.Main")

def main():
    log.info("starting Main")

    game = Engine.Game(1600, 900, True)

    startScreen = StartScreen()

    game.startApp(startScreen)
    game.run()

class StartScreen(Engine.Application):
    def __init__(self):
        super(StartScreen, self).__init__()

        self.backgroundColor = (0,0,0)

        self.quitButton = Interface.SolidButton(
            width = 70, height = 40,
            colorReset = (100,100,100),
            colorHover = (255,50,50),
            colorPress = (255,150,150),
            command = self.game.quit,
            textObject = Sprite.Text(
                "X", 0, 0, (255,255,255), 40, "consola.ttf"),
            )
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1
        self.addSprite(self.quitButton)

        self.pushupsButton = Interface.SolidButton(
            x = self.game.xprop(.5), y = self.game.yprop(.5),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            colorReset = (255,90,0),
            colorHover = (255,130,40),
            colorPress = (255,200,150),
            command = None,
            textObject = Sprite.Text(
                "Push-ups", 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "consola.ttf"),
            )
        self.pushupsButton.name = "pushupsButton"
        self.addSprite(self.pushupsButton)

        self.pullupsButton = Interface.SolidButton(
            x = self.game.xprop(.50 - .18), y = self.game.yprop(.5),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            colorReset = (0,90,255),
            colorHover = (40,130,255),
            colorPress = (150,200,255),
            command = None,
            textObject = Sprite.Text(
                "Pull-ups", 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "consola.ttf"),
            )
        self.pullupsButton.name = "pullupsButton"
        self.addSprite(self.pullupsButton)
        
        self.curlupsButton = Interface.SolidButton(
            x = self.game.xprop(.50 + .18), y = self.game.yprop(.5),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            colorReset = (205,50,205),
            colorHover = (205,90,205),
            colorPress = (255,160,255),
            command = None,
            textObject = Sprite.Text(
                "Curl-ups", 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "consola.ttf"),
            )
        self.curlupsButton.name = "curlupsButton"
        self.addSprite(self.curlupsButton)
        
        self.squatsButton = Interface.SolidButton(
            x = self.game.xprop(.50 + .18*2), y = self.game.yprop(.5),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            colorReset = (0,190,50),
            colorHover = (50,230,80),
            colorPress = (150,240,180),
            command = None,
            textObject = Sprite.Text(
                "Squats", 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "consola.ttf"),
            )
        self.squatsButton.name = "squatsButton"
        self.addSprite(self.squatsButton)

        self.dipsButton = Interface.SolidButton(
            x = self.game.xprop(.50 - .18*2), y = self.game.yprop(.5),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            colorReset = (210,0,0),
            colorHover = (250,50,50),
            colorPress = (255,120,120),
            command = None,
            textObject = Sprite.Text(
                "Dips", 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "consola.ttf"),
            )
        self.dipsButton.name = "dipsButton"
        self.addSprite(self.dipsButton)


if __name__ == "__main__":
    Debug.test(main)
