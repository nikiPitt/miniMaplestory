from cmu_graphics import *
from PIL import Image

class Monsters:
    topLeftX = None
    topLeftY = None
    width = None
    height = None
    pause = False

    def __init__(self, path):
        self.sprites = [[], []]
        self.spritestrip = Image.open(path)
        self.spritestripR = self.spritestrip.transpose(Image.FLIP_LEFT_RIGHT)

    def splitStrip(self, numOfSprites):
        for i in range(numOfSprites):
            frame = self.spritestrip.crop((self.frameW*i, 0, self.frameW+self.frameW*i, self.frameH))
            frameR = self.spritestripR.crop((self.frameW*i, 0, self.frameW+self.frameW*i, self.frameH))
            sprite, spriteR = CMUImage(frame), CMUImage(frameR)
            self.sprites[0].append(sprite)
            self.sprites[1].append(spriteR)

    def getSize(self):
        if self.width != None and self.height != None:
            return self.width, self.height
    
    def getCoordinate(self):
        if self.topLeftX != None and self.topLeftY != None:
            return self.topLeftX, self.topLeftY
    
    def setLocation(self, x, y):
        self.topLeftX = x
        self.topLeftY = y
    
    def setScale(self, factor):
        self.frameW = self.frameW * factor
        self.frameH = self.frameH * factor

    def draw(self, topLeftX, topLeftY, stepCount, sizeWidth, sizeHeight):
        if self.direction == 1: k = 1
        elif self.direction == -1: k = 0

        sprite = self.sprites[k][stepCount % len(self.sprites[k])]
        self.topLeftX, self.topLeftY = topLeftX, topLeftY
        self.width, self.height = sizeWidth, sizeHeight
        drawImage(sprite, topLeftX, topLeftY, width=sizeWidth, height=sizeHeight, align = 'left-top')
        #drawRect(topLeftX, topLeftY, sizeWidth, sizeHeight, fill=None, border='black')
    
class orangeMushroom(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 3
        self.strength = 10
        self.speed = 2
        self.direction = 1

    def repr(self):
        return "OrangeMushRoom"

class snail(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 1
        self.strength = 3
        self.speed = 1
        self.direction = 1

    def repr(self):
        return "snail"

class slime(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 2
        self.strength = 10
        self.speed = 4
        self.direction = 1

    def repr(self):
        return "slime"

class stump(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 3
        self.strength = 15
        self.speed = 2
        self.direction = 1

    def repr(self):
        return "stump"

class shroom(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 2
        self.strength = 5
        self.speed = 3
        self.direction = 1

    def repr(self):
        return "shroom"

class ribbonPig(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 4
        self.strength = 10
        self.speed = 4
        self.direction = 1

    def repr(self):
        return "ribbonPig"

class fireBoar(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 5
        self.strength = 12
        self.speed = 5
        self.direction = 1

    def repr(self):
        return "fireBoar"

class octopus(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 6
        self.strength = 15
        self.speed = 3
        self.direction = 1

    def repr(self):
        return "octopus"
    
class stoneGolem(Monsters):
    def __init__(self, path, frameWidth, frameHeight):
        super().__init__(path)
        self.frameW = frameWidth
        self.frameH = frameHeight
        self.attackPower = 8
        self.strength = 20
        self.speed = 5
        self.direction = 1

    def repr(self):
        return "stoneGolem"

