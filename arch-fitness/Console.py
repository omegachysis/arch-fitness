
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

class GameConsole(object):
    MESSAGE_HEIGHT = 15
    READING_BUFFER = 50
    ENTRY_BUFFER = 15
    BUFFER_LEFT = 15
    DARKEN_WIDTH = .80
    
    def __init__(self, game, level=logging.INFO):
        sys.stdout = ConsoleSTDOUT(self)
        
        rootLogger = logging.getLogger("R")
        
        self.messages = []
        self.game = game
        self.hidden = True
        self.env = self
        self.stream = ""
        self.entry = ""

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

        exec(open("gameConsole.cfg", 'r').read())

        for blacklistedSource in GameConsole.blacklistedSources:
            self.blacklistSource(blacklistedSource)

    def resetConfiguration(self):
        exec(open("gameConsole.cfg", 'r').read())

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
            if ",".join(testing) in GameConsole.blacklistedSources:
                return True
        return False

    def getEnvironment(self):
        return self._environment
    def setEnvironment(self, environment):
        if hasattr(environment, 'execute'):
            self._environment = environment
        else:
            log.error("(execute) " + str(environment) + " is not an environment.")
    env = property(getEnvironment, setEnvironment)
    environment = property(getEnvironment, setEnvironment)
    def resetEnvironment(self):
        self.env = self
    def resetEnv(self):
        self.env = self

    def execute(self, command):
        log.info("(execute) " + command)
        try:
            if self.env == self or command[0] == "#":
                if command[0] == "#":
                    exec(command[1:])
                else:
                    exec(command)
            else:
                self.env.execute(command)
        except:
            log.error("(execute) " + traceback.format_exc())

    def executeEntry(self):
        self.execute(self.entry)
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
        try:
            levelname, source, message = stream.split(" ; ")
            if not self.isSourceBlacklisted(source):
                color = {"DEBUG":(150,150,150,255),"INFO":(100,100,255,255),
                         "WARNING":(255,255,50,255),"ERROR":(255,20,20,255),
                         "CRITICAL":(255,20,20,255)}[levelname]

                multiline = message.split("\n")

                for msg in multiline:
                    surface, rect = self.font.render(msg, color)
                    self.messages.append([surface,rect])

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
