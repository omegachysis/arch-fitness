#!/usr/bin/env python3

import pygame
from pygame.locals import *

import Engine

def main():
    game = Engine.Game(1280, 720)

    testApp = Engine.Application()
    testApp.backgroundColor = (0, 0, 0, 255)

    testButton = SolidButton(100, 100, 50, 50,
                             (0,0,255,255), (255,0,255,255), (0,255,0,255),
                             None)

    testApp.addSprite(testButton)

    testButton2 = SolidButton(200, 100, 50, 50,
                             (255,0,0,255), (255,0,255,255), (0,255,0,255),
                             game.quit)

    testApp.addSprite(testButton2)

    game.startApp(testApp)
    game.run()

class SolidButton(Engine.Sprite):
    STATE_RESET = 0
    STATE_HOVER = 1
    STATE_PRESS = 2
    def __init__(self, x, y, width, height, colorReset, colorHover, colorPress, command):
        """
        Create a solid colored button that runs 'command' when clicked.
        """

        # Fill a rectangular and blank surface with the reset color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(colorReset)

        # Set up Sprite object
        super(SolidButton, self).__init__(self.surface, x, y)

        self.state = SolidButton.STATE_RESET

        self.colorReset = colorReset
        self.colorHover = colorHover
        self.colorPress = colorPress

        self.command = command

    def hover(self):
        """State invoked when the mouse is on top of the button."""
        if self.state != SolidButton.STATE_HOVER:
            self.state = SolidButton.STATE_HOVER
            self.surface.fill(self.colorHover)
    def press(self):
        """State invoked when the mouse is on top of the button and clicks."""
        if self.state != SolidButton.STATE_PRESS:
            self.state = SolidButton.STATE_PRESS
            self.surface.fill(self.colorPress)
            if self.command:
                self.command()
    def reset(self):
        """State invoked when the mouse is outside of the button boundary."""
        if self.state != SolidButton.STATE_RESET:
            self.state = SolidButton.STATE_RESET
            self.surface.fill(self.colorReset)

    def update(self, dt):
        mousex, mousey = pygame.mouse.get_pos()

        if mousex > self.left and mousex < self.right and \
           mousey > self.top  and mousey < self.bottom:
            if pygame.mouse.get_pressed()[0]:
                self.press()
            else:
                self.hover()
        else:
            self.reset()
        
        super(SolidButton, self).update(dt)

if __name__ == "__main__":
    import Debug
    Debug.test(main)
