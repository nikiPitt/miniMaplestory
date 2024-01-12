from cmu_graphics import *
from PIL import Image

class Objects:
    topLeftX = None
    topLeftY = None

    def __init__(self, path):
        self.gameObj = Image.open(path)
        self.width = self.gameObj.width
        self.height = self.gameObj.height
    
    def getSize(self):
        return self.width, self.height
    
    def getCoordinate(self):
        return self.topLeftX, self.topLeftY

    def setScale(self, factor):
        self.width = self.width * factor
        self.height = self.height * factor
    
    def draw(self, topLeftX, topLeftY):
        self.topLeftX, self.topLeftY = topLeftX, topLeftX
        drawImage(CMUImage(self.gameObj), topLeftX, topLeftY, width=self.width, height=self.height)

class Portal(Objects):
    def __init__(self, path, name, topLeftX, topLeftY):
        super().__init__(path)
        self.destination = name
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
    
    def getTopLeft(self):
        return self.topLeftX, self.topLeftY
    

    def draw(self):
        drawImage(CMUImage(self.gameObj), self.topLeftX, self.topLeftY, width=self.width, height=self.height)