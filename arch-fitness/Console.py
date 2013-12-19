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
import logging
import traceback
import sys

from pygame.locals import *

log = logging.getLogger("R.Console")

class ConsoleSTDOUT(object):
    def __init__(self, gameConsole):
        self.gameConsole = gameConsole
    def write(self, data):
        stream = "INFO ; STDOUT ; " + data + "\n"
        log.debug("!@ STDOUT received " + data + " ]]")
        if data != "\n":
            self.gameConsole.write(stream)
            self.gameConsole.flush()

def splitLine(string, overflow=70):
    w=[]
    n=len(string)
    for i in range(0,n,overflow):
        w.append(string[i:i+overflow])
    return w
def lightenColor(color, value):
    r, g, b, a = color
    r += value
    g += value
    b += value
    a = 255
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return (r,g,b,a)

class GameConsole(object):
    MESSAGE_HEIGHT = 15
    READING_BUFFER = 50
    ENTRY_BUFFER = 15
    BUFFER_LEFT = 15
    DARKEN_WIDTH = .80 # percent of screen width
    TEXT_OVERFLOW = 80 # characters at 1280 px width
    SOURCE_BUFFER = 25 # characters to space after log source
    MESSAGE_BUFFER_LENGTH = 40 # messages to render before deleting
    
    def __init__(self, game, level=logging.INFO):
        sys.stdout = ConsoleSTDOUT(self)
        
        rootLogger = logging.getLogger("R")

        GameConsole.TEXT_OVERFLOW = int(
            GameConsole.TEXT_OVERFLOW * float(game.width) / 1280.0)
        
        self.messages = []
        self.game = game
        self.hidden = True
        self.env = self
        self.stream = ""
        self.entry = ""

        self._everyOtherLine = -1

        self._entrySurface = None
        self._entryRect = None

        self._consoleSurface = pygame.Surface(
            (GameConsole.DARKEN_WIDTH*game.width, game.height)
            )
        self._consoleSurface.fill((0,0,0))
        self._consoleSurface.set_alpha(200)
        self._consoleSurface = self._consoleSurface.convert_alpha()

        self.font = pygame.freetype.Font("consola.ttf",
                                         ptsize = 12)

        self._renderEntry()

        handler = logging.StreamHandler(self)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(levelname)s ; %(name)s ; %(message)s")
        handler.setFormatter(formatter)
        rootLogger.addHandler(handler)

        self.resetConfiguration()

        for blacklistedSource in GameConsole.blacklistedSources:
            self.blacklistSource(blacklistedSource)

    def sprite(self, spriteName):
        return self.game.app.reg(spriteName)

    def runScript(self, script):
        gc = self
        exec(open("scripts/" + script).read())

    def resetConfiguration(self):
        exec(open("console.cfg", 'r').read())

    def blacklistSource(self, source):
        log.info("blacklisting " + source)
        if source not in GameConsole.blacklistedSources:
            GameConsole.blacklistedSources.append(source)

    def isSourceBlacklisted(self, source):
        components = source.split(".")
        i = 0
        for component in components:
            i += 1
            testing = components[:i]
            if ".".join(testing) in GameConsole.blacklistedSources:
                return True
        return False
    def isEnvironment(self, environment):
        return hasattr(environment, 'execute')
    isEnv = isEnvironment

    def getEnvironment(self):
        return self._environment
    def setEnvironment(self, environment):
        if self.isEnv(environment):
            self._environment = environment
        else:
            log.error("(execute) " + str(environment) + " is not an environment.")
    env = property(getEnvironment, setEnvironment)
    environment = property(getEnvironment, setEnvironment)
    def resetEnvironment(self):
        self.env = self
    def resetEnv(self):
        self.env = self

    def execute(self, c, command):
        c = self
        log.info("(execute) " + command)
        try:
            if command[0] == "$":
                self.env.execute(self, "c.runScript('" + command[1:] + ".py')")
            else:
                if self.env == self or command[0] == "#":
                    if command[0] == "#":
                        if command[1] == "?":
                            exec("print(" + command[2:] + ")")
                        else:
                            exec(command[1:])
                    else:
                        if command[0] == "?":
                            exec("print(" + command[1:] + ")")
                        else:
                            exec(command)
                else:
                    if command[0] == "?":
                        self.env.execute(self, "print(" + command[1:] + ")")
                    else:
                        self.env.execute(self, command)
        except:
            log.error("(execute) " + traceback.format_exc())

    def executeEntry(self):
        self.execute(self, self.entry)
        self.entry = ""
        self._renderEntry()

    def hide(self):
        self.hidden = True
    def unhide(self):
        self.hidden = False
    def toggleHidden(self):
        self.hidden = not self.hidden

    def _renderEntry(self):
        surface, rect = self.font.render(self.entry, (255,255,255,255))
        rect.left = GameConsole.BUFFER_LEFT
        rect.bottom = self.game.height - GameConsole.ENTRY_BUFFER

        self._entrySurface = surface
        self._entryRect = rect

    def renderMessage(self, stream):
        #log.debug("!@ rendering message stream: " + stream)
        if self.game.quitting == False:
            try:
                levelname, source, message = stream.split(" ; ")
                if not self.isSourceBlacklisted(source):
                    color = {"DEBUG":(200,200,200,255),"INFO":(150,150,255,255),
                             "WARNING":(255,255,50,255),"ERROR":(255,50,50,255),
                             "CRITICAL":(255,20,255,255)}[levelname]

##                  if self._everyOtherLine < 0:
##                      #log.debug("!@ EVERY OTHER LINE")
##                      color = lightenColor(color, 80)
##                  self._everyOtherLine = -self._everyOtherLine

                    multiline = message.split("\n")
                    newMultiline = []
                    for line in multiline:
                        if len(line) >= self.TEXT_OVERFLOW:
                            newMultiline += splitLine(line, self.TEXT_OVERFLOW)
                        else:
                            newMultiline += [line]
                    multiline = newMultiline
                            
                    multiline[0] = source + " " * (self.SOURCE_BUFFER - len(source)) + multiline[0]
                    i = 0
                    for line in multiline[1:]:
                        i += 1
                        multiline[i] = " "*self.SOURCE_BUFFER + multiline[i]

                    for msg in multiline:
                        surface, rect = self.font.render(msg, color)
                        self.messages.append([surface,rect])
                        if len(self.messages) > self.MESSAGE_BUFFER_LENGTH:
                            self.messages = self.messages[1:]

                    self._recalculateCoordinates()
            except:
                log.error("!@ error rendering last stream" +\
                          traceback.format_exc())

    def _recalculateCoordinates(self):
        i = len(self.messages)
        for message in self.messages:
            i -= 1
            message[1].top = self.game.height - \
                                GameConsole.MESSAGE_HEIGHT * i - \
                                GameConsole.READING_BUFFER
            message[1].left = GameConsole.BUFFER_LEFT

    def draw(self, canvas):
        canvas.blit(self._consoleSurface, (0,0))
        canvas.blit(self._entrySurface, self._entryRect)
        for message in self.messages:
            canvas.blit(message[0], message[1])

    def entryAdd(self, unicode):
        self.entry += unicode
        self._renderEntry()
    def entryBackspace(self):
        self.entry = self.entry[:-1]
        self._renderEntry()

    def update(self, dt):
        pass

    def write(self, data):
        try:
            self.stream += str(data)
        except:
            log.critical("!@ " + traceback.format_exc())

    def flush(self):
        try:
            # ANYTHING you don't want to render to the
            # game console, precede with these symbols:
            # "!@ " (not including quotes)
            if "!@ " not in self.stream:
                self.renderMessage(self.stream[:-1])
            self.stream = ""
        except:
            log.critical("!@ " + traceback.format_exc())
