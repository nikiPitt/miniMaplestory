class Rect:
    def __init__(self, topLeftX, topLeftY, width, height):
        self.x = topLeftX
        self.y = topLeftY
        self.w = width
        self.h = height
    
    def hitsRect(self, other):
        if isinstance(other, Rect):
            return not (self.x+self.w <= other.x or other.x + other.w <= self.x or other.y + other.h <= self.y or self.y + self.h <= other.y)

    def containsRect(self, other):
        if isinstance(other, Rect):
            if self.x * self.y <= other.x * other.y:
                bigger, smaller = other, self
            else:
                bigger, smaller = self, other
            if (bigger.x <= smaller.x <= bigger.x + bigger.w and
                bigger.x <= smaller.x + self.w <= bigger.x + bigger.w and
                bigger.y <= smaller.y <= bigger.y + bigger.h and
                bigger.y <= smaller.y + self.h <= bigger.y + bigger.h):
                return True
        else: return False