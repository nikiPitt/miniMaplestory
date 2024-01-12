from Game import *
from cmu_graphics import *
import os, pathlib

#This driver file is the final running file.
def onAppStart(app):
    app.game = Game(app)
    app.stepsPerSecond = 10
    app.freeze = False
    app.freezeCounter = 0
    app.popUpWindow = False
    app.popUpHelpWindow = False
    app.bgm = loadSound("music/henesys.mp3")
    app.bgm.play(restart = True)

def onStep(app):
    if not app.freeze:
        app.game.takeStep()
    #Player dead...
    #Freeze game for 20 seconds
    elif not app.popUpWindow and not app.popUpHelpWindow: 
        app.freezeCounter += 1
        if app.freezeCounter == 200:
            app.freeze = False
            app.freezeCounter = 0

def onKeyPress(app, key):
    app.game.keyPressMotion(key, app)

def onKeyRelease(app, key):
    app.game.keyReleaseMotion(key)

def onKeyHold(app, keys):
    app.game.keyHoldMotion(keys, app)

def onMousePress(app, mouseX, mouseY):
    app.game.mousePressMotion(mouseX, mouseY)

def redrawAll(app):
    app.game.drawGame(app)

def loadSound(relativePath):
    absolutePath = os.path.abspath(relativePath)
    url = pathlib.Path(absolutePath).as_uri()
    return Sound(url)

def main():
    runApp(1440, 800)

main()  