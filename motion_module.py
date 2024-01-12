from cmu_graphics import *
from Shape import Rect

class CharacterMotion:
    @staticmethod
    def legalLeftRightMove(charac, gameMap):
        if charac.direction == 1:
            for solidCell in gameMap.mapDic:
                cellblX = solidCell[1] * gameMap.cellSize
                cellblY = solidCell[0] * gameMap.cellSize + gameMap.cellSize
                if ((cellblY - gameMap.cellSize < charac.posY + charac.height <= cellblY) and 
                    (cellblX <= charac.posX + charac.width - charac.hitboxOffset < cellblX + gameMap.cellSize)):
                    return False
            else: return True
        elif charac.direction == -1:
            for solidCell in gameMap.mapDic:
                cellbrX = solidCell[1] * gameMap.cellSize + gameMap.cellSize
                cellbrY = solidCell[0] * gameMap.cellSize + gameMap.cellSize
                if ((cellbrY - gameMap.cellSize < charac.posY + charac.height <= cellbrY) and 
                    (cellbrX - gameMap.cellSize < charac.posX + charac.hitboxOffset <= cellbrX)):
                    return False
            else: return True

    def onTerrain(charac, gameMap):
        bRcolIdx = (charac.posX + charac.width) // gameMap.cellSize
        bRrowIdx = (charac.posY + charac.height) // gameMap.cellSize

        bLcolIdx = charac.posX // gameMap.cellSize
        bLrowIdx = (charac.posY + charac.height) // gameMap.cellSize
        
        if ((bRrowIdx, bRcolIdx) in gameMap.mapDic or 
            (bLrowIdx, bLcolIdx) in gameMap.mapDic):
            return True

        elif ((bRrowIdx+1, bRcolIdx) not in gameMap.mapDic or 
            (bLrowIdx+1, bLcolIdx) not in gameMap.mapDic):
            return False

    @staticmethod
    def moveRight(charac):
        charac.posX += charac.dx
        charac.dx+= charac.ddx
        charac.direction = 1
    
    @staticmethod
    def moveLeft(charac):
        charac.posX -= charac.dx
        charac.dx += charac.ddx
        charac.direction = -1

    @staticmethod
    def drop(charac, gameMap):
        if charac.direction == 1:
            colIdx = (charac.posX + charac.width) // gameMap.cellSize
            rowIdx = (charac.posY + charac.height) // gameMap.cellSize
        elif charac.direction == -1:
            colIdx = charac.posX // gameMap.cellSize
            rowIdx = (charac.posY + charac.height) // gameMap.cellSize
        if (rowIdx, colIdx) in gameMap.mapDic:
            return rowIdx, colIdx
        else:
            return None
        
    @staticmethod
    def jump(charac):
        charac.posY -= 70
        charac.onAir = True

    @staticmethod
    def attack(charac, gameData, app, attackPower):
        monster = CharacterMotion.detectAttack(charac, gameData.monsterHandler.monsters)
        if monster != None:
            charac.attackSound.play()
            #monster back off little bit when attacked
            monster.strength -= attackPower
            #if monster's location is legal than move
            if not gameData.monsterHandler.lightningAttk:
                monster.topLeftX += charac.direction * 30
                if not gameData.monsterHandler.legalMove(monster, gameData, app):
                    monster.topLeftX -= charac.direction * 30
            CharacterMotion.afterAttack(charac, monster, gameData)
    
    @staticmethod
    def afterAttack(charac, monster, gameData):
            if monster.strength <= 0:
                charac.stat['exp'] += 5
                gameData.monsterHandler.genItem(monster)
                gameData.monsterHandler.monsters.remove(monster)
                if (len(gameData.monsterHandler.monsters)) == 0:
                    gameData.monsterHandler.generateMonsters(gameData, app)
            # This indicates power up!
            if charac.stat['exp'] >= charac.stat['expCap']:
                charac.stat['level'] += 1
                charac.stat['expCap'] *= 1.5
                charac.stat['exp'] = 5
                charac.stat['skillPoint'] += 10
                charac.stat['hp'] = charac.stat['hpCap']
                charac.stat['mp'] = charac.stat['mpCap']
    
    @staticmethod
    def eat(charac, gameData):
        items = gameData.monsterHandler.items
        x0, y0 = charac.posX + charac.width / 2 , charac.posY + charac.height
        for item in items:
            x1, y1 = item[0], item[1]
            if distance(x0, y0, x1, y1) < charac.width / 2:
                charac.eatingSound.play()
                if item[2] == 'redPortion':
                    if charac.stat['hp'] <= charac.stat['hpCap'] - 25:
                        charac.stat['hp'] += 50
                elif item[2] == 'bluePortion':
                    if charac.stat['mp'] <= charac.stat['mpCap'] - 25:
                       charac.stat['mp'] += 50
                elif item[2] == 'exp':
                    charac.stat['exp'] += 5
                items.remove(item)

    @staticmethod
    def portalMove(charac, gameData):
        portalList = gameData.objectRenderer.portal
        portal = portalList[0]
        charac.posX = portal.topLeftX
        charac.posY = portal.topLeftY + (portal.height - charac.height)

    @staticmethod
    def climbing(charac, gameData):
        solidCells = gameData.gameScreen.gameMap.mapDic
        cellSize = gameData.gameScreen.gameMap.cellSize
        # player's (row, col) based on mid bottom location
        row, col = (charac.posY + charac.height) // cellSize, charac.posX // cellSize            
        charac.posY -= 5
        if (row+1, col) in solidCells:
            charac.state = 'standing'

    @staticmethod
    def blink(charac, gameData):
        charac.stat['mp'] -= charac.skill['blink']['consume']
        charac.posX, charac.posY = charac.getRandomPosOnTerrain(gameData)

    @staticmethod
    def final(charac, gameData, app):
        charac.stat['mp'] -= charac.skill['final']['consume']
        # attack offset increases only in one direction
        originalAttkOffset = charac.attkOffset
        charac.attkOffset *= (charac.skill['final']['train']) 
        CharacterMotion.attack(charac, gameData, app, charac.skill['final']['power'])
        charac.attkOffset = originalAttkOffset

    @staticmethod
    def flame(charac, gameData, app):
        charac.stat['mp'] -= charac.skill['flame']['consume']
        monsters = gameData.monsterHandler.monsters
        flameBoxList = []
        for _ in range(charac.skill['flame']['train']):
            flameX, flameY = charac.getRandomPosOnTerrain(gameData)
            flameBox = Rect(flameX, flameY, 100, charac.height)
            flameBoxList.append(flameBox)
            for mon in monsters:
                width, height = mon.getSize()
                topLeftX, topLeftY = mon.getCoordinate()
                monBox = Rect(topLeftX, topLeftY, width, height)
                if flameBox.hitsRect(monBox):
                    charac.attackSound.play()
                    mon.strength -= charac.skill['flame']['power']
                    mon.topLeftX += charac.direction * 30
                    if not gameData.monsterHandler.legalMove(mon, gameData, app):
                        mon.topLeftX -= charac.direction * 30
                    CharacterMotion.afterAttack(charac, mon, gameData)
        charac.flameBoxes.append(flameBoxList)

    @staticmethod
    def lightning(charac, gameData, app):
        charac.stat['mp'] -= charac.skill['lightning']['consume']
        # holds monsters movement for few seconds
        # train = seconds to hold monsters
        lightningToggle = gameData.monsterHandler.lightningAttk
        gameData.monsterHandler.lightningAttk = not lightningToggle
        monsters = gameData.monsterHandler.monsters
        lightBoxList = []
        for _ in range(charac.skill['lightning']['train']):
            lightX, lightY = charac.getRandomPosOnTerrain(gameData)
            lightBox = Rect(lightX, lightY, 30, 100)
            lightBoxList.append(lightBox)
            for mon in monsters:
                width, height = mon.getSize()
                topLeftX, topLeftY = mon.getCoordinate()
                monBox = Rect(topLeftX, topLeftY, width, height)
                if lightBox.hitsRect(monBox):
                    charac.attackSound.play()
                    mon.strength -= charac.skill['lightning']['power']
                    mon.topLeftX += charac.direction * 30
                    if not gameData.monsterHandler.legalMove(mon, gameData, app):
                        mon.topLeftX -= charac.direction * 30
                    CharacterMotion.afterAttack(charac, mon, gameData)
        charac.lightBoxes.append(lightBoxList)     

    #Helper distance method
    def distance(x0, y0, x1, y1):
        return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
    def detectAttack(charac, monsterList):
        for mon in monsterList:
            width, height = mon.getSize()
            topLeftX, topLeftY = mon.getCoordinate()
            monBox = Rect(topLeftX, topLeftY, width, height)
            if charac.direction == 1:
                # Compare left x coordinate
                # hibox threshold applied
                attkBox = Rect(charac.posX + charac.width, charac.posY, charac.attkOffset, charac.height)
                if attkBox.hitsRect(monBox) or attkBox.containsRect(monBox):
                    return mon
            elif charac.direction == -1:
                # Compare right x coordinate
                # hitbox threshold applied
                attkBox = Rect(charac.posX - charac.attkOffset, charac.posY, charac.attkOffset, charac.height)
                if attkBox.hitsRect(monBox) or attkBox.containsRect(monBox):
                    return mon
        return None