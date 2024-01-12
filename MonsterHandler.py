from Monsters import *
import random

class MonsterHandler:
    stepCount = 0
    monsterList = ['snail', 'shroom', 'orangeMushRoom', 'slime', 'stump', 'ribbonPig', 'fireBoar', 'octopus', 'stoneGolem']
    itemList = ['redPortion', 'bluePortion', 'exp']
    monsters = []
    items = []
    lightningAttk = False
    lightningAttkCounter = 0

    def __init__(self, gameData, app):
        # This will be starter monsters
        self.generateMonsters(gameData, app)
    
    # recursive method to retrieve x, y coordinate of monster
    def genLocationFromMap(self, gameData, frameW, frameH, app):
        terrain = gameData.gameScreen.gameMap.terrainBoundary
        cellSize = gameData.gameScreen.gameMap.cellSize
        randomIdx = random.randint(0, len(terrain) - 1)
        leftTopX, leftTopY = terrain[randomIdx][1] * cellSize, terrain[randomIdx][0] * cellSize
        # validity check (does not exceed boudary of the window)
        monX, monY = leftTopX, leftTopY - frameH
        if monX + frameW > app.width or monY < 0:
            return self.genLocationFromMap(gameData, frameW, frameH, app)
        else: return monX, monY

    def generateMonsters(self, gameData, app):
        self.monsters = []
        gameLevel = gameData.gameCharacter.stat['level']
        #If level increases generated number of monsters increases
        #Also stronger monsters appear
        numOfMons = random.randint(1, gameLevel+1)
        for _ in range(numOfMons):
            monIdx = random.randint(0, (gameLevel % len(self.monsterList)) + 1)
            picked = self.monsterList[monIdx]
            if picked == 'snail':
                # image source: https://www.spriters-resource.com/fullview/22034/
                newMon = snail('images/monsters/gimp/snailStrip_45x25.png', 45, 25)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(5)
            elif picked == 'shroom':
                # image source: https://www.spriters-resource.com/fullview/22038/
                newMon = shroom('images/monsters/gimp/shroom_38x35.png', 38, 35)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(4)
            elif picked == 'orangeMushRoom':
                #image source: https://freepngimg.com/png/91586-emoticon-sprite-text-game-video-maplestory/icon
                newMon = orangeMushroom('images/monsters/gimp/orangeMushroomStrip_63x63.png', 63, 63)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(5)
            elif picked == 'slime':
                #image source: https://www.spriters-resource.com/pc_computer/maplestory/
                newMon = slime('images/monsters/gimp/slime_70x85.png', 70, 85)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(5)
            elif picked == 'stump':
                #image source: https://www.spriters-resource.com/fullview/22082/
                newMon = stump('images/monsters/gimp/stump_70x60.png', 70, 60)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(4)
            elif picked == 'ribbonPig':
                #image source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/16187/
                newMon = ribbonPig('images/monsters/gimp/ribbonPig_70x50.png', 70, 50)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(3)
            elif picked == 'fireBoar':
                #image source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/21662/
                newMon = fireBoar('images/monsters/gimp/fireBoar_80x55.png', 80, 55)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(3)
            elif picked == 'octopus':
                #image source: https://www.spriters-resource.com/fullview/16184/
                newMon = octopus('images/monsters/gimp/octopus_50x70.png', 70, 70)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(5)  
            elif picked == 'stoneGolem':
                #image source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/22207/
                newMon = stoneGolem('images/monsters/gimp/stoneGolem_115x100.png', 115, 100)
                monX, monY = self.genLocationFromMap(gameData, newMon.frameW, newMon.frameH, app)
                newMon.setLocation(monX, monY)
                newMon.splitStrip(10)                
            self.monsters.append(newMon)

    def takeStep(self, gameData, app):
        lightningTrain = gameData.gameCharacter.skill['lightning']['train']
        # Dealing with edge case
        if lightningTrain == 0:
            self.lightningAttk = False
        if not self.lightningAttk:
            self.stepCount += 1
            self.makeMovement(gameData, app)
        else:
            self.lightningAttkCounter += 1
            if self.lightningAttkCounter == lightningTrain * 10:
                self.lightningAttk = False
                self.lightningAttkCounter = 0


    def legalMove(self, monster, gameData, app):
        solidTiles = gameData.gameScreen.gameMap.mapDic
        cellSize = gameData.gameScreen.gameMap.cellSize
        # window width check
        if (monster.topLeftX + monster.width >= app.width or 
            monster.topLeftX <= 0):
            return False
        
        # solid cell check - bottom
        bRR, bRC = (monster.topLeftY + monster.height) // cellSize, (monster.topLeftX + monster.width) // cellSize
        bLR, bLC = (monster.topLeftY + monster.height) // cellSize, monster.topLeftX // cellSize
        bottomCells = {(bRR, bRC), (bLR, bLC)}
        for cell in bottomCells:
            if cell not in solidTiles:
                return False
            
        if monster.direction == 1:
            for solidCell in solidTiles:
                cellblX = solidCell[1] * cellSize
                cellblY = solidCell[0] * cellSize + cellSize
                if ((cellblY - cellSize < monster.topLeftY + monster.height <= cellblY) and 
                    (cellblX <= monster.topLeftX + monster.width <= cellblX + cellSize)):
                    return False
            else: return True

        elif monster.direction == -1:
            for solidCell in solidTiles:
                cellbrX = solidCell[1] * cellSize + cellSize
                cellbrY = solidCell[0] * cellSize + cellSize
                if ((cellbrY - cellSize < monster.topLeftY + monster.height <= cellbrY) and 
                    (cellbrX - cellSize <= monster.topLeftX <= cellbrX)):
                    return False
            else: return True
        return True

    def makeMovement(self, gameData, app):
        if len(self.monsters) != 0:
            for monster in self.monsters:
                if not monster.pause:
                    #if player and monseter is in the same level
                    #row is same
                    cha = gameData.gameCharacter
                    cellSize = gameData.gameScreen.gameMap.cellSize
                    chaRow = (cha.posY + cha.height) // cellSize
                    monRow = (monster.topLeftY + monster.height) // cellSize
                    if chaRow == monRow:
                        vector = cha.posX - monster.topLeftX
                        if vector <= 0:
                            # this means player is on the left side of the screen
                            monster.direction = -1
                        else:
                            # this means player is on the right side of the screen
                            monster.direction = 1
                    monster.topLeftX += monster.direction * monster.speed
                if not self.legalMove(monster, gameData, app):
                    # revert the direction
                    monster.direction *= -1
    
    def genItem(self, monster):
        cx = monster.topLeftX + monster.width / 2
        cy = monster.topLeftY + monster.height
        randomIdx = random.randint(0, len(self.itemList) - 1)
        self.items.append([cx, cy, self.itemList[randomIdx]])

    def draw(self):
        if len(self.monsters) != 0:
            for monster in self.monsters:
                drawWidth, drawHeight = monster.frameW, monster.frameH
                monster.draw(monster.topLeftX, monster.topLeftY, self.stepCount, drawWidth, drawHeight)
                if monster.strength > 1:
                    drawRect(monster.topLeftX, monster.topLeftY + drawHeight + 5, monster.strength, 7, fill='red')
                else:
                    drawRect(monster.topLeftX, monster.topLeftY + drawHeight + 5, 1, 7, fill='red', visible=False)
        if len(self.items) != 0:
            for item in self.items:
                type = item[2]
                if type == 'redPortion':
                    drawCircle(item[0], item[1]-3.5, 7, fill='red')
                elif type == 'bluePortion':
                    drawCircle(item[0], item[1]-3.5, 7, fill='blue')
                elif type == 'exp':
                    drawCircle(item[0], item[1]-5, 10, fill='gold')
