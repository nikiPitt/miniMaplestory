from cmu_graphics import *
from PIL import Image
import os, pathlib


class Interface:
    selectedBtn = False

    def __init__(self):
        app.skillsWindowCornerX = app.width-app.width/2-100
        app.skillsWindowCornerY = app.height-app.height/2-150

        # Save window buttons
        self.buttons = {'help' : Button('helpWindow', app.width - 40, app.height - 40, 30, 30),
                        'closeHelpWindow' : Button('closeHelpWindow', app.width/2 - 300, app.height/2 - 275, 20, 20),
                        'skill' : Button('skillWindow', app.width - 80, app.height - 40, 30, 30),
                        'closeWindow' : Button('closeWindow', app.skillsWindowCornerX, app.skillsWindowCornerY-20, 20, 20)
                        }
        
        # Save skill +/- buttons
        skillsName = ['blink', 'final', 'flame', 'lightning']
        for i in range(len(skillsName)):
            self.buttons[f'{skillsName[i]}tField'] = Button(f'{skillsName[i]}tField', app.skillsWindowCornerX + 95, app.skillsWindowCornerY + 70*i + 35, 20, 20)
            self.buttons[f'{skillsName[i]}pField'] = Button(f'{skillsName[i]}pField', app.skillsWindowCornerX + 120, app.skillsWindowCornerY + 70*i + 35, 20, 20)
            self.buttons[f'{skillsName[i]}Plus'] = Button(f'{skillsName[i]}Plus', app.skillsWindowCornerX + 145, app.skillsWindowCornerY + 70*i + 35, 20, 20)
            self.buttons[f'{skillsName[i]}Minus'] = Button(f'{skillsName[i]}Minus', app.skillsWindowCornerX + 170, app.skillsWindowCornerY + 70*i + 35, 20, 20)

        self.skillsCards = self.loadSkillCardImages()

        #Sound effects source: https://www.sounds-resource.com/pc_computer/maplestoryadventures/sound/2888/
        self.buttonclick = self.loadSound("music/soundeffects/clicking.wav")

    def drawInterface(self, app, gameCharacter):
        # draw bottom bar
        drawRect(0, app.height - 50, app.width, 50, fill='grey', opacity=30)
        # draw level
        drawLabel(f"Lv. {gameCharacter.stat['level']}", 50, app.height - 25, fill = 'white', bold=True, size=30)
        # draw hp
        drawRect(150, app.height - 40, gameCharacter.stat['hpCap'], 30, fill='crimson', opacity=20)
        if app.freeze and not app.popUpWindow and not app.popUpHelpWindow: 
            drawRect(155, app.height - 35, 1, 20, fill='crimson', visible=False)
        else:
            drawRect(155, app.height - 35, gameCharacter.stat['hp'], 20, fill='crimson', visible=True)
        drawLabel('HP', 150, app.height - 25, align = 'center', fill = 'white', bold=True)
        # draw mp
        drawRect(470, app.height - 40, gameCharacter.stat['mpCap'], 30, fill='deepSkyBlue', opacity=20)
        drawRect(475, app.height - 35, gameCharacter.stat['mp'], 20, fill='deepSkyBlue')
        drawLabel('MP', 470, app.height - 25, align = 'center', fill = 'white', bold=True)
        # draw exp
        drawRect(800, app.height - 40, gameCharacter.stat['expCap'], 30, fill='gold', opacity=20)
        drawRect(800, app.height - 35, gameCharacter.stat['exp'], 20, fill='gold')
        drawLabel('EXP', 800, app.height - 25, align = 'center', fill = 'white', bold=True)
        # draw point
        drawCircle(app.width - 120, app.height - 25, 15, fill='silver')
        drawLabel(gameCharacter.stat['skillPoint'], app.width - 120, app.height - 25, align = 'center', fill='slateGray', bold=True, size=20)
        # draw health button
        drawRect(self.buttons['help'].x, self.buttons['help'].y, self.buttons['help'].w, self.buttons['help'].h, fill='crimson')
        drawLabel('?', app.width - 25, app.height - 25, align = 'center', fill = 'white', size=20, bold=True)
        # draw skill button
        drawRect(self.buttons['skill'].x, self.buttons['skill'].y, self.buttons['skill'].w, self.buttons['skill'].h, fill='deepSkyBlue')
        drawLabel('S', app.width - 65, app.height - 25, align = 'center', fill = 'white', size=20, bold=True)
    
    def drawFreezeWindow(self, app):
        if app.freeze and not app.popUpWindow and not app.popUpHelpWindow:
            toggle = True
        else: toggle = False
        drawRect(0, 0, app.width, app.height, fill='black', opacity=30, visible=toggle)
        counter = app.freezeCounter//10
        #Image source: https://www.pinterest.com/pin/game-over-clipart-vector-game-over-glitch-text-effect-play-player-retro-png-image-for-free-download--634233560028781376/
        drawImage(CMUImage(Image.open("images/window/gimp/gameover_200x150.png")), app.width/2, app.height/2-50, align='center', visible=toggle)
        drawLabel(f"Game Resume in... {20 - counter}", app.width/2, app.height/2 + 50, align='center',fill='gainsboro', size=20, bold=True, italic=True, visible=toggle)
    
    def drawPopUpWindow(self, app, charac):
        drawRect(0, 0, app.width, app.height, fill='black', opacity=10)
        windowCornerX, windowCornerY = app.width-app.width/2-100, app.height-app.height/2-150
        #Skill set box
        drawRect(windowCornerX, windowCornerY, 200, 300, fill='white', opacity=80)
        #Skille set ribbon bar
        drawRect(windowCornerX, windowCornerY-20, 200, 20, fill='black', opacity=30)
        #Buttons
        #closing button 'x'
        drawRect(self.buttons['closeWindow'].x, self.buttons['closeWindow'].y, self.buttons['closeWindow'].w, self.buttons['closeWindow'].h, fill='black', opacity=0)
        drawLabel('X', windowCornerX, windowCornerY-20, fill='white', bold=True, align='top-left', size=25)
        #Skill cards
        skillsName = ['blink', 'final', 'flame', 'lightning']
        for i in range(len(self.skillsCards)):
            # skill card image
            drawImage(self.skillsCards[i], windowCornerX + 10, windowCornerY + 70*i + 25, align='left-top')
            # skill label
            drawLabel(skillsName[i].upper(), windowCornerX + 10, windowCornerY + 70*i + 10, align='top-left', size=10)

            #trainButton
            drawRect(self.buttons[f'{skillsName[i]}tField'].x,
                     self.buttons[f'{skillsName[i]}tField'].y, 
                     self.buttons[f'{skillsName[i]}tField'].w, 
                     self.buttons[f'{skillsName[i]}tField'].h, 
                     fill='black', opacity=40, border=self.buttons[f'{skillsName[i]}tField'].toggle)
            drawLabel("T", windowCornerX + 105, windowCornerY + 70*i + 25, fill='black', 
                      align='center', size=15, opacity = 30)              
            drawLabel(charac.skill[skillsName[i]]['train'], 
                      windowCornerX + 105, windowCornerY + 70*i + 45, fill='black', 
                      align='center', size=20)          

            #powerButton
            drawRect(self.buttons[f'{skillsName[i]}pField'].x, 
                     self.buttons[f'{skillsName[i]}pField'].y, 
                     self.buttons[f'{skillsName[i]}pField'].w, 
                     self.buttons[f'{skillsName[i]}pField'].h, 
                     fill='black', opacity=40, border=self.buttons[f'{skillsName[i]}pField'].toggle)
            drawLabel("P", windowCornerX + 130, windowCornerY + 70*i + 25, fill='black', 
                      align='center', size=15, opacity = 30)      
            drawLabel(charac.skill[skillsName[i]]['power'], 
                      windowCornerX + 130, windowCornerY + 70*i + 45, fill='black', 
                      align='center', size=20)
            
            #plusButton
            drawRect(self.buttons[f'{skillsName[i]}Plus'].x, 
                     self.buttons[f'{skillsName[i]}Plus'].y, 
                     self.buttons[f'{skillsName[i]}Plus'].w, 
                     self.buttons[f'{skillsName[i]}Plus'].h, fill='black', opacity=40)
            drawLabel('+', windowCornerX + 155, windowCornerY + 70*i + 45, fill='red', 
                      bold=True, align='center', size=20)
            
            #minusButton
            drawRect(self.buttons[f'{skillsName[i]}Minus'].x, 
                     self.buttons[f'{skillsName[i]}Minus'].y, 
                     self.buttons[f'{skillsName[i]}Minus'].w, 
                     self.buttons[f'{skillsName[i]}Minus'].h, fill='black', opacity=40)
            drawLabel('-', windowCornerX + 180, windowCornerY + 70*i + 45, fill='blue', 
                      bold=True, align='center', size=20)
    
    def drawPopUpHelpWindow(self, app):
        drawRect(0, 0, app.width, app.height, fill='black', opacity=10)
        drawRect(self.buttons['closeHelpWindow'].x, self.buttons['closeHelpWindow'].y, 600, 20, fill='black', opacity=40)
        drawRect(self.buttons['closeHelpWindow'].x, self.buttons['closeHelpWindow'].y-20, 
                 600, 550, fill='white', opacity=20)
        drawRect(self.buttons['closeHelpWindow'].x, self.buttons['closeHelpWindow'].y, 
                 self.buttons['closeHelpWindow'].w, self.buttons['closeHelpWindow'].h, fill='black', opacity=0)
        drawLabel('X', self.buttons['closeHelpWindow'].x, self.buttons['closeHelpWindow'].y, 
                  fill='white', bold=True, align='top-left', size=25)
        #Skill icon source: https://maplestory.nexon.net/micro-site/59387
        #Player source: https://www.spriters-resource.com/pc_computer/maplestory/sheet/36606/
        guide = CMUImage(Image.open("images/window/gimp/helpWindow.png"))
        drawImage(guide, self.buttons['closeHelpWindow'].x+50, self.buttons['closeHelpWindow'].y+50,align='left-top',opacity=80)

    def loadSkillCardImages(self):
        #Image source: https://maplestory.nexon.net/micro-site/59387
        card1 = CMUImage(Image.open("images/player/gimp/blink_36x36.png"))
        card2 = CMUImage(Image.open("images/player/gimp/finalAttack_36x36.png"))
        card3 = CMUImage(Image.open("images/player/gimp/flame_36x36.png"))
        card4 = CMUImage(Image.open("images/player/gimp/lighteningAttack_36x36.png"))
        return [card1, card2, card3, card4]

    def mousePressMotion(self, mouseX, mouseY, charac):
        for button in self.buttons.values():
            buttonMidX = button.x + (button.w / 2)
            buttonMidY = button.y + (button.h / 2)
            if distance(mouseX, mouseY, buttonMidX, buttonMidY) <= button.w / 2:
                self.buttonclick.play()
                if button.label == 'skillWindow':
                    app.freeze = True
                    app.popUpWindow = True
                elif button.label == 'closeWindow':
                    app.freeze = False
                    app.popUpWindow = False
                elif button.label == 'helpWindow':
                    app.freeze = True
                    app.popUpHelpWindow = True
                elif button.label == 'closeHelpWindow':
                    app.freeze = False
                    app.popUpHelpWindow = False
                elif 'Field' in button.label:
                    if not self.selectedBtn:
                        button.toggle = 'cyan'
                        self.selectedBtn = True
                    else: 
                        button.toggle = None
                        self.selectedBtn = False
                # This means that button is selected
                # and the user clicked plus button
                elif 'Plus' in button.label:
                    skillName = button.label.split('P')[0]
                    if self.buttons[skillName+'pField'].toggle != None:
                        if charac.stat['skillPoint'] > 0:
                            charac.skill[skillName]['power'] += 1
                            charac.stat['skillPoint'] -= 1
                        # turn button to unselected state
                        self.buttons[skillName+'pField'].toggle = None
                        self.selectedBtn = False         
                    elif self.buttons[skillName+'tField'].toggle != None:
                        # turn button to unselected state
                        if charac.stat['skillPoint'] > 0:             
                            charac.skill[skillName]['train'] += 1
                            charac.stat['skillPoint'] -= 1
                        self.buttons[skillName+'tField'].toggle = None
                        self.selectedBtn = False                                    
                # This means that button is selected
                # and the user clicked minus button
                elif 'Minus' in button.label:
                    skillName = button.label.split('M')[0]
                    if self.buttons[skillName+'pField'].toggle != None:
                        minusResult = charac.skill[skillName]['power']
                        if minusResult > 0:
                            charac.skill[skillName]['power'] -= 1
                            charac.stat['skillPoint'] += 1 
                        self.buttons[skillName+'pField'].toggle = None
                        self.selectedBtn = False                                            
                    elif self.buttons[skillName+'tField'].toggle != None:
                        minusResult = charac.skill[skillName]['power']
                        if minusResult > 0:
                            charac.skill[skillName]['train'] -= 1
                            charac.stat['skillPoint'] += 1                        
                        self.buttons[skillName+'tField'].toggle = None
                        self.selectedBtn = False
    
    #Referenced Mike's Sound demo file
    def loadSound(self, relativePath):
        absolutePath = os.path.abspath(relativePath)
        url = pathlib.Path(absolutePath).as_uri()
        return Sound(url)

class Button:
    def __init__(self, label, topLeftX, topLeftY, width, height):
        self.label = label
        self.x = topLeftX
        self.y = topLeftY
        self.w = width
        self.h = height
        self.toggle = None