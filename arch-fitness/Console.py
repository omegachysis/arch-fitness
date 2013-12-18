
import pygame
import logging
import traceback
import sys

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
    
    def __init__(self, game, level=logging.INFO):
        sys.stdout = ConsoleSTDOUT(self)
        
        rootLogger = logging.getLogger("R")
        
        self.messages = []
        self.game = game
        self.hidden = True
        self.environment = self
        self.stream = ""
        self.entry = ""

        self._entrySurface = None
        self._entryRect = None

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

        for blacklistedSource in GameConsole.blacklistSources:
            log.info("Blacklisting " + blacklistedSource)

    def setEnvironment(self, environment):
        self.environment = environment

    def execute(self, command):
        log.info("(execute) " + command)
        try:
            if self.environment == self:
                exec(command)
            else:
                self.environment.execute(command)
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
        log.debug("!@ rendering message stream: " + stream)
        levelname, source, message = stream.split(" ; ")
        if source not in self.blacklistSources:
            color = {"DEBUG":(150,150,150,100),"INFO":(100,100,255,200),
                     "WARNING":(255,255,50,220),"ERROR":(255,20,20,255),
                     "CRITICAL":(255,20,20,255)}[levelname]

            multiline = message.split("\n")

            for msg in multiline:
                surface, rect = self.font.render(msg, color)
                self.messages.append([surface,rect])

            self._recalculateCoordinates()

    def _recalculateCoordinates(self):
        i = len(self.messages)
        for message in self.messages:
            i -= 1
            message[1].top = self.game.height - \
                                GameConsole.MESSAGE_HEIGHT * i - \
                                GameConsole.READING_BUFFER
            message[1].left = GameConsole.BUFFER_LEFT

    def draw(self, canvas):
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
