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

        super(Fade, self).__init__()

    def begin(self, sprite):
        self.m = float(sprite.alpha) / float(self.time)
        sprite.unhide()

    
