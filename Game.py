from GameScreen import *
from Character import *
from ObjectRenderer import *
from MonsterHandler import *

class Game:
    def __init__(self, app):
        # Define which map to render
        self.mapStyle = 'starter'
        # load gameScreen data according to the map style
        self.gameScreen = GameScreen(app, self.mapStyle)
        # draw object on the game screen
        self.objectRenderer = ObjectRenderer(self, app)
        # draw character on the game screen
        self.gameCharacter = Character(self, app)
        # draw monsters on the game screen
        # monsterHandler should be called when map is Startter or Hunting Field
        self.monsterHandler = MonsterHandler(self, app)
    
    def reloadGameData(self, app):
        self.gameScreen.generateMapData(self.mapStyle)
        self.objectRenderer.generatePortals(self, app)
        self.objectRenderer.getRopeIndicatingCells(self)
        self.monsterHandler.generateMonsters(self, app)
    
    def drawGame(self, app):
        self.gameScreen.draw(app, self)
        self.objectRenderer.draw(self)
        self.monsterHandler.draw()
        self.gameCharacter.draw()
        self.gameScreen.gameInterface.drawFreezeWindow(app)
        if app.popUpWindow:
            self.gameScreen.gameInterface.drawPopUpWindow(app, self.gameCharacter)
        if app.popUpHelpWindow:
            self.gameScreen.gameInterface.drawPopUpHelpWindow(app)

    def takeStep(self):
        self.gameCharacter.takeStep(self, app)
        self.monsterHandler.takeStep(self, app)
    
    def keyPressMotion(self, key, app):
        self.gameCharacter.keyPressMotion(self, key, app)
    
    def keyReleaseMotion(self, key):
        self.gameCharacter.keyReleaseMotion(key)
    
    def keyHoldMotion(self, keys, app):
        self.gameCharacter.keyHoldMotion(keys, self)
    
    def mousePressMotion(self, mouseX, mouseY):
        self.gameScreen.mousePressMotion(mouseX, mouseY, self.gameCharacter)
