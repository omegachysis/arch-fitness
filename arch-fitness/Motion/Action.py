
class Action(object):
    def __init__(self):
        self.loop = 1
    def begin(self, sprite):
        pass
    def cancel(self):
        pass
    def finish(self):
        self.loop -= 1
        if self.loop:
            self.begin(self.sprite)
        else:
            self.sprite.removeMotion(self)
    def update(self, dt):
        pass
