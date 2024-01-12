from cmu_graphics import *
from motion_module import CharacterMotion as charMotion
from PIL import Image
import random
import os, pathlib

class Character:
    #Class instance - physical tratis
    #Velocity
    dy = 8
    dx = 10

    #Acceleration
    ddx = 0.05
    ddy = 0.5   

    #Hitbox threshold
    hitboxOffset = 20
    attkOffset = 10

    ########################################################################
    ############################ Constructor ###############################
    ########################################################################

    def __init__(self, gameData, app):
        #Motion data
        self.height = 60
        self.width = 50
        self.posX, self.posY = self.getRandomPosOnTerrain(gameData)
        self.onAir = False
        self.state = 'standing'
        self.direction = 1
        self.stepCount  = 0
        self.flameBoxes = []
        self.lightBoxes = []

        #Displays & Sounds
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        self.walking = self.loadMotionImageFrames('images/player/gimp/walking_50x60.png', 50, 60, 4)
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        self.jumping = self.loadSingleMotionImage('images/player/gimp/jumping_50x60.png')
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        self.standing = self.loadSingleMotionImage('images/player/gimp/standingStill_47x60.png')
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        attacking = self.loadMotionImageFrames('images/player/gimp/attacking_80x80.png', 80, 80, 5, True)
        attackingReversed = self.loadMotionImageFrames('images/player/gimp/reversedAttacking_80x80.png', 80, 80, 6, True)
        self.attacking = [attacking, attackingReversed]
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        self.attacked = self.loadSingleMotionImage('images/player/gimp/attacked_50x142.png')
        #Player source: https://www.deviantart.com/jaydonb5/art/MapleStory-Dennis-Sprite-Sheet-440446809
        self.climbing = self.loadMotionImageFrames('images/player/gimp/climbing_50x60.png', 50, 60, 2)
        #Sound effect source: https://www.sounds-resource.com/pc_computer/maplestoryadventures/sound/2888/
        self.attackSound = loadSound("music/soundeffects/attack.wav")
        self.eatingSound = loadSound("music/soundeffects/itemEating.wav")
        self.gameoverSound = loadSound("music/soundeffects/gameOver.wav")

        #Skills
        #Skill effect source: https://orangemushroom.net/2013/07/03/kms-ver-1-2-196-maplestory-red-1st-impact/
        self.blink = self.loadSingleMotionImage('images/skills/gimp/blink_80x78.png')
        #Skill effect source: https://en.ac-illust.com/clip-art/24209979/pixel-art-attack-slashing-illustration
        self.final = self.loadSingleMotionImage('images/skills/gimp/final_165x165.png')
        #Skill effect source: https://craftpix.net/product/fire-pixel-art-animation-sprites/
        self.flame = self.loadSingleMotionImage('images/skills/gimp/flame_96x100.png')
        #Skill effect source: https://orangemushroom.net/2013/07/03/kms-ver-1-2-196-maplestory-red-1st-impact/
        self.lightning = self.loadSingleMotionImage('images/skills/gimp/lightning_95x165.png')

        #Character stat
        self.stat = {'hp' : 280, 'hpCap': 280, 'mp': 280, 'mpCap': 280, 'exp': 5, 'expCap': 10, 'attackPower': 1, 'level': 0, 'skillPoint': 0}

        #Character skill
        self.skill = {'blink' : {'train': 0, 'power': 0, 'consume': 10}, 
                      'final': {'train': 0, 'power': 0, 'consume' : 15},
                      'flame': {'train': 0, 'power': 0, 'consume': 25},
                      'lightning': {'train': 0, 'power': 0, 'consume': 30}
                      }

    #Draw method which is eventually called by redrawAll(app)
    def draw(self):
        #Motion type is determined by direction of the player
        if self.direction == 1: k = 1
        elif self.direction == -1: k = 0

        #Draw character's motion by motion state
        if self.state == 'onRope':
            drawImage(self.climbing[0][0], self.posX, self.posY, align = 'left-top')
        elif self.state == 'climbing':
            drawImage(self.climbing[0][self.stepCount % len(self.climbing)], self.posX, self.posY, align = 'left-top')
        elif self.state == 'walking':
            sprite = self.walking[k][self.stepCount % len(self.walking)]
            drawImage(sprite, self.posX, self.posY, align = 'left-top')
        elif self.state == 'standing':
            sprite = self.standing[k][0]
            drawImage(sprite, self.posX, self.posY, align = 'left-top')
        elif self.state == 'attacking':
            attackingcount = self.stepCount // 5
            sprite = self.attacking[k][attackingcount % len(self.attacking)]
            drawImage(sprite, self.posX, self.posY-20, align = 'left-top')
        elif self.state == 'jumping' or self.onAir and not 'attacking':
            drawImage(self.jumping[k][0], self.posX, self.posY, align = 'left-top')
        elif self.state == 'attacked':
            drawImage(self.attacked[k][0], self.posX, self.posY-82, align = 'left-top')
        elif self.state == 'blinkMode':
            sprite = self.jumping[k][0]
            drawImage(sprite, self.posX, self.posY-20, align = 'left-top')
            drawImage(self.blink[k][0], self.posX, self.posY-82, align = 'left-top')
        elif self.state == 'finalMode':
            sprite = self.attacking[k][1]
            drawImage(sprite, self.posX, self.posY-20, align = 'left-top')
            drawImage(self.final[k][0], self.posX, self.posY-82, align = 'left-top')

        #Reference hitbox representation
        #drawRect(self.posX, self.posY, self.width+self.attkOffset, self.height, fill=None, border='black', borderWidth=1)

        #Images to draw for skills
        #Flame skill
        if self.flameBoxes != []:
            for flameBoxList in self.flameBoxes:
                for flameBox in flameBoxList:
                    drawImage(self.flame[k][0], flameBox.x, flameBox.y-40, align = 'left-top')
        #Lighting skill
        if self.lightBoxes != []:
            for lightBoxList in self.lightBoxes:
                for lightBox in lightBoxList:
                    drawImage(self.lightning[k][0], lightBox.x, lightBox.y-105, align = 'left-top')
    
    ########################################################################
    ############################# Take Step ################################
    ########################################################################

    # This takeStep method is eventually called by onStep(app)
    def takeStep(self, gameData, app):
        # Player's motion control
        self.stepCount += 1
        gameMap = gameData.gameScreen.gameMap
        if self.stepCount % 50 == 0:
            if self.stat['mp'] < self.stat['mpCap']:
                self.stat['mp'] += 1
        if self.onAir and self.state != 'onRope' and self.state != 'climbing':
            self.posY += self.dy
            self.dy += self.ddy
            newPos = charMotion.drop(self, gameMap)
            #Move character's location back to on top of the cell
            if newPos != None:
                self.onAir = False
                self.state = 'standing'
                self.dy = 8
                self.posY = newPos[0] * gameMap.cellSize - self.height
        if not charMotion.onTerrain(self, gameMap):
            if self.state != 'onRope' or self.state != 'climbing':
                self.onAir = True
        if self.state == 'attacking' and not self.onAir:
            if self.stepCount % 5 == 0:
                self.state = 'standing'
        
        #Detect any collision with monsters
        monster = self.detectCollision(gameData.monsterHandler.monsters)
        if monster != None:
            self.stat['hp'] -= monster.attackPower
            self.state = 'attacked'
            if self.stat['hp'] <= 0:
                app.freeze = True
                self.gameoverSound.play()
                self.stat['hp'] = 100

        # Visual clear-up for skill effects
        if self.stepCount % 10 == 0:
            if len(self.flameBoxes) != 0:
                self.flameBoxes = self.flameBoxes[1:]
        
        if not gameData.monsterHandler.lightningAttk:
            if len(self.lightBoxes) != 0:
                self.lightBoxes = self.lightBoxes[1:]
        
    ########################################################################
    ############################## Key Press ###############################
    ########################################################################
     
    def keyPressMotion(self, gameData, key, app):
        if not app.freeze:
            if key == 'up' and not self.state == 'attacked':
                if self.onAir == False:
                    self.state = 'jumping'
                    charMotion.jump(self)
                    rope = self.isRopeCell(gameData.objectRenderer.ropes, gameData.gameScreen.gameMap.cellSize)
                    if rope != None:
                        if self.state == 'onRope':
                            self.state = 'climbing'
                        self.onAir = False
                        self.state = 'onRope'
            elif key == 'down':
                destination = self.fronOfPortal(gameData)
                if destination != None:
                    gameData.mapStyle = destination
                    if destination == 'village':
                        app.bgm = loadSound("music/treetops.mp3")
                        app.bgm.play(restart = True)
                    else: 
                        app.bgm = loadSound("music/henesys.mp3")
                        app.bgm.play(restart = True)
                    gameData.reloadGameData(app)
                    charMotion.portalMove(self, gameData)
            elif key == 'x' and not self.state == 'attacked':
                self.state = 'attacking'
                self.attack = True
                charMotion.attack(self, gameData, app, self.stat['attackPower'])
            elif key == 'z':
                charMotion.eat(self, gameData)
            elif key == 'q':
                if self.stat['mp'] > self.skill['blink']['consume']:
                    self.state = 'blinkMode'
                    charMotion.blink(self, gameData)
            elif key == 'w':
                if self.stat['mp'] > self.skill['final']['consume']:
                    self.state = 'finalMode'
                    charMotion.final(self, gameData, app)
            elif key == 'a':
                if self.stat['mp'] > self.skill['flame']['consume']:
                    charMotion.flame(self, gameData, app)
            elif key == 's':
                if self.stat['mp'] > self.skill['lightning']['consume']:
                    charMotion.lightning(self, gameData, app)

    ########################################################################
    ############################# Key Release ##############################
    ########################################################################
    
    def keyReleaseMotion(self, key):
        if not app.freeze:
            if key == 'right' and not self.onAir:
                self.state = 'standing'
                self.dx = 10
            if key == 'left' and not self.onAir:
                self.state = 'standing'
                self.dx = 10
            if key == 'up' and self.state == 'climbing':
                self.state = 'onRope'

    ########################################################################
    ############################# Key Hold #################################
    ########################################################################

    def keyHoldMotion(self, keys, gameData):
        if not app.freeze:
            if 'right' in keys and self.state != 'onRope' and self.state != 'climbing':
                if not self.onAir:
                    self.state = 'walking'
                if self.onAir:
                    self.state = 'jumping'
                charMotion.moveRight(self)
                if not charMotion.legalLeftRightMove(self, gameData.gameScreen.gameMap):
                    self.posX -= self.dx
            elif 'left' in keys and self.state != 'onRope' and self.state != 'climbing':
                if not self.onAir:
                    self.state = 'walking'
                if self.onAir:
                    self.state = 'jumping'
                charMotion.moveLeft(self)
                if not charMotion.legalLeftRightMove(self, gameData.gameScreen.gameMap):
                    self.posX += self.dx
            elif ('up' in keys and self.state != 'jumping' and self.state != 'standing' and 
                  self.state != 'attacking' and self.state != 'attacked'):
                self.state = 'climbing'
                self.onAir = False
                charMotion.climbing(self, gameData)

    ########################################################################
    ##################### Other Character class methods ####################
    ########################################################################
    
    #Method that returns random and valid position for player
    #Retruns topLeftX and topLeftY coordinate
    def getRandomPosOnTerrain(self, gameData):
        terrain = gameData.gameScreen.gameMap.terrainBoundary
        cellSize = gameData.gameScreen.gameMap.cellSize
        randomIdx = random.randint(0, len(terrain) - 1)
        leftTopX, leftTopY = terrain[randomIdx][1] * cellSize, terrain[randomIdx][0] * cellSize
        # validity check (does not exceed boudary of the window)
        return leftTopX, leftTopY - self.height
    
    #Helper method that process on input image and store in the characters class
    def loadSingleMotionImage(self, imagePath):
        spriteList = [[], []]
        sprite = Image.open(imagePath)
        spriteList[0].append(CMUImage(sprite))
        flippedSprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        spriteList[1].append(CMUImage(flippedSprite))
        return spriteList
    
    #Helper method that process on input strip image, split accdordingly
    #and store in the characters class databse
    def loadMotionImageFrames(self, imagePath, frameW, frameH, numOfSprites, oneDirection=False):
        if oneDirection:
            spriteList = []
            strip = Image.open(imagePath)
            self.splitStrip(strip, spriteList, frameW, frameH, numOfSprites)
        else:
            spriteList = [[], []]
            # store orginial version
            strip = Image.open(imagePath)
            self.splitStrip(strip, spriteList[0], frameW, frameH, numOfSprites)
            # store flipped version
            flippedStrip = strip.transpose(Image.FLIP_LEFT_RIGHT)
            self.splitStrip(flippedStrip, spriteList[1], frameW, frameH, numOfSprites)
        return spriteList

    def splitStrip(self, strip, spritesList, frameW, frameH, numOfSprites):
        for i in range(numOfSprites):
            frame = strip.crop((frameW*i, 0, frameW + frameW*i, frameH))
            sprite = CMUImage(frame)
            spritesList.append(sprite)

    #Helper method that verifies whether the player pressed arrow down in fron of the portal
    def fronOfPortal(self, gameData):
        characTopLeft = self.posX, self.posY
        for portal in gameData.objectRenderer.portal:
            portalTopLeft = portal.getTopLeft()
            portalSize = portal.getSize()
            if (portalTopLeft[0] <= characTopLeft[0] <= portalTopLeft[0] + portalSize[0] 
                and portalTopLeft[1] <= characTopLeft[1] <= portalTopLeft[1] + portalSize[1]):
                return portal.destination
        else: return None
    
    #Helper method that verifies whether the player is in the rope celll or not
    def isRopeCell(self, ropeCellList, cellSize):
        if ropeCellList != None:
            for rope in ropeCellList:
                leftX, rightX = rope[1]*cellSize, rope[1]*cellSize + cellSize
                topY, bottomY = rope[0]*cellSize, rope[0]*cellSize + cellSize
                midX = self.posX + self.width / 2
                if (leftX < midX < rightX and topY <= self.posY < bottomY):
                    return rope
        return None

    #Helper method that detects any collision with player and list of others
    def detectCollision(self, listOfOthers):
        for other in listOfOthers:
            #Retrieve reference corners and size of an object
            width, height = other.getSize()
            topLeftX, topLeftY = other.getCoordinate()
            bottomRightX, bottomRightY= topLeftX + width, topLeftY + height
            #Compute rather character is colliding with an object
            if (topLeftX <= self.posX + self.width and self.posX <= bottomRightX and
                self.posY <= bottomRightY and self.posY + self.height >= topLeftY) :
                return other
        return None
    
#Referenced Mike's Sound demo file
def loadSound(relativePath):
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)


