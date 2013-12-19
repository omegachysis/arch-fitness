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
            textObject = Engine.Text(
                "X", 0, 0, (255,255,255), 40, "consola.ttf"),
            )
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1
        self.addSprite(self.quitButton)

        self.pushupsButton = Interface.SolidButton(
            x = self.game.xprop(.5), y = self.game.yprop(.5),
            width = self.game.xprop(.2), height = self.game.xprop(.2),
            colorReset = (255,130,0),
            colorHover = (255,200,100),
            colorPress = (255,255,200),
            command = None,
            textObject = Engine.Text(
                "Pushups", 0, self.game.xprop(.08),
                (255,255,255), self.game.xprop(.03), "consola.ttf"),
            )
        self.addSprite(self.pushupsButton)

if __name__ == "__main__":
    Debug.test(main)
