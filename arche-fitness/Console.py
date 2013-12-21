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
    """
    Used to recieve output from python calls to print() and similar functions.  It then transfers
    these calls to the GameConsole.
    """
    def __init__(self, gameConsole):
        self.gameConsole = gameConsole
    def write(self, data):
        stream = "INFO ; STDOUT ; " + data + "\n"
        log.debug("!@ STDOUT received " + data + " ]]")
        if data != "\n":
            self.gameConsole.write(stream)
            self.gameConsole.flush()

def splitLine(string, overflow=70):
    """
    Split a line with new lines where the line buffer width is 'overflow'
    """
    w=[]
    n=len(string)
    for i in range(0,n,overflow):
        w.append(string[i:i+overflow])
    return w

##def lightenColor(color, value):
##    """
##    Brighten every color element value by 'value'
##    """
##    r, g, b, a = color
##    r += value
##    g += value
##    b += value
##    a = 255
##    if r > 255:
##        r = 255
##    if g > 255:
##        g = 255
##    if b > 255:
##        b = 255
##    return (r,g,b,a)

class GameConsole(object):
    MESSAGE_HEIGHT = 15 # spacing in pixels to give each message, including the message itself
    CONSOLE_PADDING = 50 # space in pixels from the bottom of the screen where messages start
    ENTRY_PADDING = 15 # space in pixels from the bottom of the screen where the entry box starts
    PADDING_LEFT = 15 # padding in pixels from the left of the screen to text.
    DARKEN_WIDTH = .80 # percent of screen width to darken from console background
    TEXT_OVERFLOW = 80 # characters at 1280 px width
    LOGSOURCE_SPACING = 25 # characters to space after logging source values
    MESSAGE_BUFFER_LENGTH = 40 # messages to render before deleting
    
    def __init__(self, game, level=logging.INFO):
        sys.stdout = ConsoleSTDOUT(self)
        
        rootLogger = logging.getLogger("R")

        self.fps = 0
        self._fpsUpdateWait = 0
        self._fpsUpdateDelay = 100

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

        self.font = pygame.freetype.Font("font/consola.ttf",
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
        """ Return sprite from application registry """
        return self.game.app.reg(spriteName)

    def runScript(self, script):
        """
        Run script from script directory.
        See console command guide for shortcut ($)
        """
        gc = self
        exec(open("script/" + script).read())

    def resetConfiguration(self):
        """ Load default console configuration. """
        exec(open("config/console.cfg", 'r').read())

    def blacklistSource(self, source):
        """ Prevent a logging source from logging to the console. """
        log.info("blacklisting " + source)
        if source not in GameConsole.blacklistedSources:
            GameConsole.blacklistedSources.append(source)

    def isSourceBlacklisted(self, source):
        """ Return whether a given logsource is not allowed to log to the console. """
        components = source.split(".")
        i = 0
        for component in components:
            i += 1
            testing = components[:i]
            if ".".join(testing) in GameConsole.blacklistedSources:
                return True
        return False
    def isEnvironment(self, environment):
        """ Return whether 'environment' is a suitable environ for the console. """
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
    def resetEnv(self): #shorthand
        self.env = self

    def execute(self, c, command):
        """ Execute a console command with 'c' as the GameConsole instance. """
        c = self # we only use 'c' in the execute function for compatibility with other environments!
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
        rect.left = GameConsole.PADDING_LEFT
        rect.bottom = self.game.height - GameConsole.ENTRY_PADDING

        self._entrySurface = surface
        self._entryRect = rect

    def _renderFPS(self, fps):
        surface, rect = self.font.render(str(fps), (255,255,255,255))
        rect.left = GameConsole.PADDING_LEFT
        rect.top = GameConsole.PADDING_LEFT

        self._fpsSurface = surface
        self._fpsRect = rect

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
                            
                    multiline[0] = source + " " * (self.LOGSOURCE_SPACING - len(source)) + multiline[0]
                    i = 0
                    for line in multiline[1:]:
                        i += 1
                        multiline[i] = " "*self.LOGSOURCE_SPACING + multiline[i]

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
                                GameConsole.CONSOLE_PADDING
            message[1].left = GameConsole.PADDING_LEFT

    def draw(self, canvas):
        canvas.blit(self._consoleSurface, (0,0))
        canvas.blit(self._entrySurface, self._entryRect)
        for message in self.messages:
            canvas.blit(message[0], message[1])
        canvas.blit(self._fpsSurface, self._fpsRect)
            

    def entryAdd(self, unicode):
        self.entry += unicode
        self._renderEntry()
    def entryBackspace(self):
        self.entry = self.entry[:-1]
        self._renderEntry()

    def update(self, dt):
        self._fpsUpdateWait -= dt
        if self._fpsUpdateWait <= 0.0:
            self.fps = int(1.0/(dt/1000.0))
            self._renderFPS(self.fps)
            self._fpsUpdateWait = self._fpsUpdateDelay

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
