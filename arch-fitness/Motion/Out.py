from Motion.Action import Action

import logging

log = logging.getLogger("R.Engine.Motion")

class Disappear(Action):
    name = "out.appear"
    def __init__(self, sprite):
        super(Disappear, self).__init__()

    def update(self, dt):
        self.sprite.hide()
        self.finish()

class Fade(Action):
    name = "out.fade"
    def __init__(self, time):
        self.time = time
        self._spriteAlpha = None

        super(Fade, self).__init__()

    def begin(self, sprite):
        if self._spriteAlpha == None:
            self._spriteAlpha = sprite.alpha
        self.m = float(self._spriteAlpha) / float(self.time)
        sprite.unhide()

    def cancel(self):
        log.debug

    def update(self, dt):
        if self.x >= self.time:
            self.x = self.time
            self.sprite.alpha = 255
            self.finish()
        else:
            self.sprite.alpha = self.m * self.x

    
