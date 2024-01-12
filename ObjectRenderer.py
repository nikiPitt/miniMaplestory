from Objects import Portal
from cmu_graphics import *

class ObjectRenderer():
    def __init__(self, gameData, app):
        self.portal = []
        self.ropes = None
        self.generatePortals(gameData, app)
        
    def draw(self, gameData):
        cellSize = gameData.gameScreen.gameMap.cellSize
        for portal in self.portal:
            portal.draw()
        if self.ropes != None:
            for rope in self.ropes:
                ropeX, ropeY = rope[1] * cellSize, rope[0] * cellSize
                #reference rope representation
                #drawRect(ropeX, ropeY, cellSize, cellSize, fill=None, border='black', borderWidth=1)

    def generatePortals(self, gameData, app):
        if gameData.mapStyle == 'starter':
            #Image source: https://pngtree.com/so/portal
            newPortaltoVill = Portal('images/gameObjects/gimp/portal.png', 'village', 40, 440)
            self.portal.clear()
            self.portal.append(newPortaltoVill)
        elif gameData.mapStyle == 'village':
            #Image source: https://pngtree.com/so/portal
            newPortaltoStart = Portal('images/gameObjects/gimp/portal.png', 'starter', 40, 600)
            #Image source: https://pngtree.com/so/portal
            newPortaltoHF = Portal('images/gameObjects/gimp/portal.png', 'huntingField', 1280, 480)
            self.portal.clear()
            self.portal.extend([newPortaltoStart, newPortaltoHF])
        elif gameData.mapStyle == 'huntingField':
            #Image source: https://pngtree.com/so/portal
            newPortaltoVill = Portal('images/gameObjects/gimp/portal.png', 'village', 40, 440)
            #Image source: https://pngtree.com/so/portal
            newPortaltoStart = Portal('images/gameObjects/gimp/portal.png', 'starter', 1140, 360)
            self.portal.clear()
            self.portal.extend([newPortaltoVill, newPortaltoStart])
    
    def getRopeIndicatingCells(self, gameData):
        mapDic = set()
        #Generate map using empty map dictionary
        if gameData.mapStyle == 'village':
            for row in range(8, 13):
                mapDic.add((row, 16))
        if gameData.mapStyle == 'huntingField':
            for row in range(2, 6):
                mapDic.add((row, 18))
            for row in range(0, 6):
                mapDic.add((row, 9))
            for row in range(6, 13):
                mapDic.add((row, 14))
        self.ropes = mapDic