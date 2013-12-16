#!/usr/bin/env python3

import pygame
from pygame.locals import *
import logging

import Engine

log = logging.getLogger("R.Interface")

def main():
    game = Engine.Game(1280, 720)

    testApp = Engine.Application()
    testApp.backgroundColor = (0, 0, 0, 255)

    testButton = SolidButton(100, 200, 50, 50,
                             (0,0,255,255), (255,0,255,255), (0,255,0,255),
                             None)

    testApp.addSprite(testButton)

    testButton2 = SolidButton(400, 200, 200, 200,
                             (255,0,0,255), (255,0,255,255), (0,255,0,255),
                             game.quit)

    testButton2.text = Engine.Text("X", 50, 50, (255,255,255,255), 250, "consola.ttf")

    testApp.addSprite(testButton2)

    game.startApp(testApp)
    game.run()

class SolidButton(Engine.Sprite):
    STATE_RESET = 0
    STATE_HOVER = 1
    STATE_PRESS = 2
    def __init__(self, x, y, width, height,
                 colorReset, colorHover, colorPress, command, textObject=None):
        """
        Create a solid colored button that runs 'command' when clicked.
        """
        log.debug("intializing new solid button")

        # Fill a rectangular and blank surface with the reset color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(colorReset)

        self.text = textObject

        # Set up Sprite object
        super(SolidButton, self).__init__(self.surface, x, y)

        self.state = SolidButton.STATE_RESET

        self.colorReset = colorReset
        self.colorHover = colorHover
        self.colorPress = colorPress

        if textObject:
            self.text.x = self.x
            self.text.y = self.y

        self.command = command
        
    def draw(self, canvas):
        super(SolidButton, self).draw(canvas)
        if self.text:
            self.text.draw(canvas)
        
    def setX(self, x):
        super(SolidButton, self).setX(x)
        if self.text:
            self.text.x = self.x
    def setY(self, y):
        super(SolidButton, self).setY(y)
        if self.text:
            self.text.y = self.y
    x = property(Engine.Sprite.getX, setX)
    y = property(Engine.Sprite.getY, setY)

    def hover(self):
        """State invoked when the mouse is on top of the button."""
        if self.state != SolidButton.STATE_HOVER:
            log.debug("hovering over button")
            self.surface.fill(self.colorHover)
            if self.state == SolidButton.STATE_PRESS:
                if self.command:
                    self.command()
            self.state = SolidButton.STATE_HOVER
    def press(self):
        """State invoked when the mouse is on top of the button and clicks."""
        if self.state != SolidButton.STATE_PRESS:
            log.debug("pressing button")
            self.state = SolidButton.STATE_PRESS
            self.surface.fill(self.colorPress)
    def reset(self):
        """State invoked when the mouse is outside of the button boundary."""
        if self.state != SolidButton.STATE_RESET:
            log.debug("resetting button")
            self.state = SolidButton.STATE_RESET
            self.surface.fill(self.colorReset)

    def update(self, dt):
        pass

    def tick(self, dt):
        mousex, mousey = pygame.mouse.get_pos()

        if mousex > self.left and mousex < self.right and \
           mousey > self.top  and mousey < self.bottom:
            if pygame.mouse.get_pressed()[0]:
                self.press()
            else:
                self.hover()
        else:
            self.reset()

        super(SolidButton, self).tick(dt)

        self.update(dt)
        

if __name__ == "__main__":
    import Debug
    Debug.test(main)
