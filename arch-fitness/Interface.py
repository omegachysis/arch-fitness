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
import logging

import Engine
import Sprite

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

    testButton2.text = Sprite.Text("X", 50, 50, (255,255,255,255), 250, "consola.ttf")

    testApp.addSprite(testButton2)

    game.startApp(testApp)
    game.run()

class SolidButton(Sprite.Sprite):
    STATE_RESET = 0
    STATE_HOVER = 1
    STATE_PRESS = 2
    def __init__(self, x=0, y=0, width=50, height=50,
                 colorReset=(0,0,0), colorHover=(0,0,0), colorPress=(0,0,0),
                 command=None, textObject=None):
        """
        Create a solid colored button that runs 'command' when clicked.
        """
        log.debug("intializing new solid button")

        self.text = None

        # Fill a rectangular and blank surface with the reset color
        self.surface = pygame.Surface((width, height))
        self.surface.fill(colorReset)

        # Set up Sprite object
        super(SolidButton, self).__init__(self.surface, x, y)

        self.state = SolidButton.STATE_RESET

        self.colorReset = colorReset
        self.colorHover = colorHover
        self.colorPress = colorPress

        self.text = textObject
        if textObject:
            self.text._parentedX = self.text.x
            self.text._parentedY = self.text.y
            self.text.x = self.x + self.text._parentedX
            self.text.y = self.y + self.text._parentedY

        self.command = command
        
    def draw(self, canvas):
        super(SolidButton, self).draw(canvas)
        if self.text:
            self.text.draw(canvas)
        
    def setX(self, x):
        super(SolidButton, self).setX(x)
        if self.text:
            self.text.x = self.x + self.text._parentedX
    def setY(self, y):
        super(SolidButton, self).setY(y)
        if self.text:
            self.text.y = self.y + self.text._parentedY
    x = property(Sprite.Sprite.getX, setX)
    y = property(Sprite.Sprite.getY, setY)

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
