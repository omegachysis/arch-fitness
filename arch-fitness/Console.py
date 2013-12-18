
import pygame
import logging

log = logging.getLogger("R.Console")

class GameConsole(object):
    MESSAGE_HEIGHT = 15
    
    def __init__(self, game, level=logging.INFO):
        rootLogger = logging.getLogger("R")
        
        self.messages = []

        self.game = game

        self.hidden = True

        self.stream = ""

        self.font = pygame.freetype.Font("consola.ttf",
                                         ptsize = 12)

        handler = logging.StreamHandler(self)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(levelname)s ; %(name)s ; %(message)s")
        handler.setFormatter(formatter)
        rootLogger.addHandler(handler)

        exec(open("gameConsole.cfg", 'r').read())

        for blacklistedSource in GameConsole.blacklistSources:
            log.info("Blacklisting " + blacklistedSource)

    def hide(self):
        self.hidden = True
    def unhide(self):
        self.hidden = False
    def toggleHidden(self):
        self.hidden = not self.hidden

    def renderMessage(self, stream):
        levelname, source, message = stream.split(" ; ")
        if source not in self.blacklistSources:
            color = {"DEBUG":(150,150,150,100),"INFO":(100,100,255,200),
                     "WARNING":(255,255,50,220),"ERROR":(255,50,50,255),
                     "CRITICAL":(10,10,255,255)}[levelname]
            
            surface, rect = self.font.render(message, color)
            self.messages.append([surface,rect])
            self._recalculateCoordinates()

    def _recalculateCoordinates(self):
        i = len(self.messages)
        for message in self.messages:
            i -= 1
            message[1].bottom = self.game.height - \
                                GameConsole.MESSAGE_HEIGHT * i
            message[1].left = 15

    def draw(self, canvas):
        for message in self.messages:
            canvas.blit(message[0], message[1])

    def update(self, dt):
        pass

    def write(self, data):
        self.stream += str(data)

    def flush(self):
        self.renderMessage(self.stream[:-1])
        self.stream = ""
