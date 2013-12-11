
class Sprite(object):
    def __init__(self, x, y, surface):
        self.surface = surface

        self.x = x
        self.y = y
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass

    # ----------------------------------------------
    # Setup class properties
    
    def getX(self):
        return self._x
    def setX(self, x):
        self._x = x
    def getY(self):
        return self._y
    def setY(self, y):
        self._y = y
    x = property(getX, setX)
    y = property(getY, setY)

    def getLeft(self):
        return self._x - self._width / 2
    def setLeft(self, left):
        self._x = left + self._width / 2
    def getRight(self):
        return self._x + self._width / 2
    def setRight(self, right):
        self._x = right - self.width / 2
    def getTop(self):
        return self._y - self._height / 2
    def setTop(self, top):
        self._y = top + self._height / 2
    def getBottom(self):
        return self._y + self._height / 2
    def setBottom(self, bottom):
        self._y = bottom - self._height / 2
    left = property(getLeft, setLeft)
    right = property(getRight, setRight)
    top = property(getTop, setTop)
    bottom = property(getBottom, setBottom)

    def getSurface(self):
        return self._surface
    def setSurface(self, surface):
        self._surface = surface
        self._width = surface.get_width()
        self._height= surface.get_height()
    surface = property(getSurface, setSurface)

    #---------------------------------------------
