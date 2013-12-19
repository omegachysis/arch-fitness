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

log = logging.getLogger("R.ArchFitness")

def main():
    log.info("starting ArchFitness")

    game = Engine.Game(1600, 900, True)

    startScreen = Engine.Application()
    startScreen.backgroundColor = (0,0,0,255)

    game.startApp(startScreen)
    game.run()

if __name__ == "__main__":
    Debug.test(main)
