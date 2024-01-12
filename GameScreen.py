from Interface import *
from Map import *

class GameScreen:
    def __init__(self, app, mapStyle):
        self.gameInterface = Interface()
        self.gameMap = Map(app, mapStyle)

    def generateMapData(self, mapStyle):
        self.gameMap.mapDic = self.gameMap.getSolidCell(mapStyle)
        self.gameMap.terrainBoundary = self.gameMap.getBoundary()
    
    def draw(self, app, gameData):
        self.gameMap.drawMap(gameData)
        self.gameInterface.drawInterface(app, gameData.gameCharacter)
    
    def mousePressMotion(self, mouseX, mouseY, gameCharac):
        self.gameInterface.mousePressMotion(mouseX, mouseY, gameCharac)