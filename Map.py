from cmu_graphics import *
from PIL import Image

class Map:
    def __init__(self, app, mapStyle):
        self.boardTop = 0
        self.boardLeft = 0
        self.numCols = 36
        self.numRows = 20
        self.cellSize = 40

        #Load Map Images to render
        #Image source: https://maplestory.fandom.com/wiki/
        self.starterMapImg = self.loadMapImg("images/map/starter_1440x800.png")
        #Image source: https://maplestory.fandom.com/wiki/
        self.villageMapImg = self.loadMapImg("images/map/village_1440x800.png")
        #Image source: https://maplestory.fandom.com/wiki/
        self.huntingFieldMapImg = self.loadMapImg("images/map/huntingField_1440x800.png")

        # solid cell dictionary
        self.mapDic = self.getSolidCell(mapStyle)

        # 2d tile map
        self.board2d = self.drawBoard(app)

        # 2d solid tile coordinat
        self.terrainBoundary = self.getBoundary()
    
    def loadMapImg(self, path):
        map2d = [[None for col in range(self.numCols)] for row in range(self.numRows)]
        map = Image.open(path)
        for row in range(self.numRows):
            for col in range(self.numCols):
                mapCell = CMUImage(map.crop((40*col, 40*row, 40+40*col, 40+40*row)))
                map2d[row][col] = mapCell
        return map2d

    def getSolidCell(self, mapStyle):
        mapDic = set()
        # generate map using empty map dictionary
        if mapStyle == 'starter' :
            for row in range(13, 20):
                for col in range(0, 36):
                    mapDic.add((row, col))
            for col in range(12, 36):
                    mapDic.add((12, col))
            for col in range(13, 36):
                    mapDic.add((11, col))
        elif mapStyle == 'village':
            for row in range(17, 20):
                for col in range(0, 36):
                    mapDic.add((row, col))
            for col in range(17, 36):
                mapDic.add((16, col))
            for col in range(18, 36):
                mapDic.add((15, col))
            for col in range(20, 36):
                mapDic.add((14, col))
            for col in range(16, 19):
                mapDic.add((13, col))
            for col in range(13, 17):
                mapDic.add((8, col))
            for col in range(13, 17):
                mapDic.add((6, col))
        elif mapStyle == 'huntingField':
            for row in range(14, 20):
                for col in range(0, 36):
                    mapDic.add((row, col))
            for row in range(11, 14):
                for col in range(26, 36):
                    mapDic.add((row, col))
            for col in range(0, 11):
                mapDic.add((13, col))
            for col in range(10, 27):
                mapDic.add((6, col))
            for col in range(17, 36):
                mapDic.add((2, col))
            mapDic.update({(13, 23), (13, 24), (13, 24), (12, 25)})
        return mapDic
    
    def getCellLeftTop(self, row, col, cellWidth, cellHeight):
        # multiply current col and row position with cellsize
        # and add with BOARD left and top value
        cellLeftCoor = self.boardLeft + cellWidth * col
        cellTopCoor = self.boardTop + cellHeight * row
        return cellLeftCoor, cellTopCoor

    def getCellSize(self, app, numRows, numCols):
        # don't be confused to divide width with cols
        # and height with rows
        cellWidth = app.width / numCols
        cellHeight = app.height / numRows
        return cellWidth, cellHeight

    def drawCell(self, app, row, col, board2d):
        # data we need to draw a cell
        cellWidth, cellHeight = self.getCellSize(app, self.numRows, self.numCols)
        cellLeft, cellTop = self.getCellLeftTop(row, col, cellWidth, cellHeight)
        board2d[row][col] = (cellLeft, cellTop, cellWidth, cellHeight)

    def drawBoard(self, app):
        board2d = [[[None] for i in range(self.numCols)] for j in range(self.numRows)]
        # drawing board is actually drawing cells one by one
        for row in range(self.numRows):
            for col in range(self.numCols):
                self.drawCell(app, row, col, board2d)
        return board2d

    def drawMap(self, gameData):
        if gameData.mapStyle == 'starter':
            map = self.starterMapImg
        elif gameData.mapStyle == 'village':
            map = self.villageMapImg
        elif gameData.mapStyle == 'huntingField':
            map = self.huntingFieldMapImg

        for row in range(self.numRows):
            for col in range(self.numCols):
                mapCell = map[row][col]
                drawImage(mapCell, 40*col, 40*row)
        
        #reference tile map
        # for cell in self.mapDic:
        #     cellX = cell[1] * self.cellSize
        #     cellY = cell[0] * self.cellSize
        #     drawRect(cellX, cellY, self.cellSize, self.cellSize, fill=None, border='black', borderWidth=1)

    def getBoundary(self):
        terrainBoundary = []
        for cell in self.mapDic:
            #This means 1 upper row in the same column
            upperCell = (cell[0]-1, cell[1]) 
            if upperCell not in self.mapDic:
                terrainBoundary.append(cell)
        return terrainBoundary
