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

    game = Engine.Game(1024, 600, False)

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
                "X", 0, 0, (255,255,255), 40, "font/consola.ttf"),
            )
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1
        self.addSprite(self.quitButton)

        self.pushupsButton = self.createExerciseButton(
            "pushups", "Push-ups", .5, .5)

        self.pullupsButton = self.createExerciseButton(
            "pullups", "Pull-ups", .50 - .18, .5)

        self.curlupsButton = self.createExerciseButton(
            "curlups", "Curl-ups", .50 + .18, .5)

        self.squatsButton = self.createExerciseButton(
            "squats", "Squats", .50 + .18 * 2, .5)

        self.dipsButton = self.createExerciseButton(
            "dips", "Dips", .50 - .18 * 2, .5)

    def createExerciseButton(self, exerciseName, label, xprop, yprop, command=None):
        button = Interface.ImageButton(
            x = self.game.xprop(xprop), y = self.game.yprop(yprop),
            width = self.game.xprop(.15), height = self.game.xprop(.15),
            imageGroup = Interface.loadButtonImageGroup("image/" + exerciseName + "Button",".png"),
            command = command,
            textObject = Sprite.Text(
                label, 0, self.game.xprop(.055),
                (255,255,255), self.game.xprop(.028), "font/consola.ttf"),
            )
        button.name = exerciseName + "Button"
        self.addSprite(button)

        return button


if __name__ == "__main__":
    Debug.test(main)
