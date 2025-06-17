# Name: Anish Jain
# AndrewID: anishjai
# Section K
# @version: 12.6.24
# 
# All graphics in main.py are either CMU graphics or designed in Canva, using Canva Pro
# On the instructions page, hold'em hands image: https://www.pokerharder.com/img/p/3/pokerhands_big.jpg 

from cmu_graphics import *
from Card import *
from Deck import *
import math
import os

def getImagePath(filename):
    """Get the correct path for image files from the images folder"""
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'images', filename)

handLabels = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush"
    ]

def onAppStart(app):
    app.width = 600
    app.height = 800
    app.selectedPlayer = 0
    app.playerTypes = ['None', 'Scared', 'Neutral', 'Risky', 'Random']
    app.playerExists = [2] * 4 + [0] * 2
    app.playerNames = [f'Player {i+1}' for i in range(6)]
    app.screen = 'selection'
    app.curText = []
    app.textPos = 0
    app.showingInstructions = False

# Moving from selection screen to actual game
def startGame(app):
    app.stepsPerSecond = 0.3
    app.numPlayers = app.playerExists.index(0) if 0 in app.playerExists else 6
    app.width = 1500
    app.height = 1000
    app.buyInBet = 10
    app.deck = Deck()
    app.starterPlayer = -1
    app.allPlayers = [Player(app.playerNames[i], 1000, app.playerTypes[app.playerExists[i]]) for i in range(app.numPlayers)]
    app.showProbabilities = True
    app.screen = 'game'
    newRound(app)
    app.winner = 0
   

# at the start of every round, must reset variables to default
def newRound(app):
    app.createDelay = False
    app.delayCount = 0
    app.deck.resetDeck()
    for i in range(len(app.allPlayers)):
        app.deck.dealHand(2, app.allPlayers[i])
        if i == 0:
            app.allPlayers[i].cards[0].flipCard()
            app.allPlayers[i].cards[1].flipCard()
        app.allPlayers[i].isFolded = False
        app.allPlayers[i].lastBet = 0
    app.probabilities = app.allPlayers[0].simulateOutcomes([], 5000)
    app.fullFlopOut = False
    app.flop = app.deck.dealFlop()
    app.isPromptingRaise = False
    app.starterPlayer += 1
    app.starterPlayer %= len(app.allPlayers)
    addToCurText(app, f'{app.allPlayers[app.starterPlayer].name} will begin this round')
    app.currentPlayer = app.starterPlayer
    app.highestBetOfRound = app.buyInBet
    app.currentMinBet = app.buyInBet
    app.handsOut = False
    app.currentInput = ''
    app.currentPot = 0
    # app.playersRemaining = []
    app.handLabels = []
    app.numPlayersIn = app.numPlayers
    app.winnerLabel = False
    # app.matchedMax = [False] * numPlayers


def nextPlayer(app):
    if app.numPlayersIn == 1:
        declareWinner(app)
    else:
        for i in range(1, app.numPlayers):
            app.currentPlayer = (app.currentPlayer + 1) % app.numPlayers
            if (app.currentPlayer == app.starterPlayer):
                app.hadOneEach = True
            if not app.allPlayers[app.currentPlayer].isFolded:
                return
        print('Couldnt find another player...')


# tell who won the round by either finding the only remaining player or comparing hands
def declareWinner(app):
    app.winner = None
    if app.numPlayersIn == 1:
        for i in range(app.numPlayers):
            if not app.allPlayers[i].isFolded:
                addToCurText(app, f'{app.allPlayers[i].name} won! Next Round.')
                app.winner = i
    else:
        curBestPlayer = None
        curBestHand = None
        for i in range(app.numPlayers):
            if not app.allPlayers[i].isFolded:
                bestForPlayer = Player.chooseBestHand(app.allPlayers[i].cards, app.flop)
                app.handLabels.append(Player.assignRankingToHand(bestForPlayer))
                if curBestPlayer == None or Player.betterHand(curBestHand, bestForPlayer) == bestForPlayer:
                    curBestPlayer = i
                    curBestHand = bestForPlayer
        addToCurText(app, f'{app.allPlayers[curBestPlayer].name} won! Next Round.')
        app.winner = curBestPlayer

    app.allPlayers[app.winner].amount += app.currentPot
    # if(app.winner == 0):

    newRound(app)

# handles all 3 of bet, raise, and fold which are potential player moves
def handleUserPlayerMove(app, key):
    if key == 'b' and app.currentInput != '' and app.currentInput.isdigit():
        value = finalizeRaise(app)
    elif key == 'b':
        app.isPromptingRaise = False
        lastBet = app.allPlayers[app.currentPlayer].lastBet
        amountToAdd = app.currentMinBet - lastBet
        if app.allPlayers[app.currentPlayer].amount >= amountToAdd: 
            app.allPlayers[app.currentPlayer].bet(amountToAdd)
            app.currentPot += amountToAdd
            app.allPlayers[app.currentPlayer].lastBet = app.currentMinBet
            addToCurText(app, f'You matched the current bet of {app.currentMinBet}')
        else:
            addToCurText(app, "Sorry! You don't have enough to bet that much. You'll have to fold.")
            app.allPlayers[app.currentPlayer].fold()
            app.numPlayersIn -= 1
    elif key == 'f':
        addToCurText(app, 'You folded.')
        app.allPlayers[app.currentPlayer].fold()
        app.numPlayersIn -= 1

# handles ai player move by simulating and calculating probabilities
def handleAIPlayerMove(app):
    betAmount = app.allPlayers[app.currentPlayer].makeAIBet(app.currentMinBet, app.flop)
    if betAmount == -1:
        app.allPlayers[app.currentPlayer].fold()
        addToCurText(app, f'{app.allPlayers[app.currentPlayer].name} folded.')
        app.numPlayersIn -= 1
    else:
        lastBet = app.allPlayers[app.currentPlayer].lastBet
        amountToAdd = betAmount - lastBet
        if app.allPlayers[app.currentPlayer].amount >= amountToAdd: 
            app.allPlayers[app.currentPlayer].bet(amountToAdd)
            app.currentPot += amountToAdd
            app.allPlayers[app.currentPlayer].lastBet = betAmount
            if betAmount == app.currentMinBet:
                addToCurText(app, f'{app.allPlayers[app.currentPlayer].name} matched the current bet of {app.currentMinBet}.')
            else:
                app.currentMinBet = betAmount
                addToCurText(app, f'{app.allPlayers[app.currentPlayer].name} raised to {app.currentMinBet}.') 
        else:
            app.allPlayers[app.currentPlayer].fold()
            addToCurText(app, f'{app.allPlayers[app.currentPlayer].name} folded.')
            app.numPlayersIn -= 1

def revealNextCardFlop(app):
    if app.flop[0].isHidden:
        app.flop[0].flipCard()
        app.flop[1].flipCard()
        app.flop[2].flipCard()
        addToCurText(app, 'The Flop has come out!')

    elif app.flop[3].isHidden:
        app.flop[3].flipCard()
        addToCurText(app, 'The Fourth Street has arrived!')

    elif app.flop[4].isHidden:
        app.flop[4].flipCard()
        addToCurText(app, 'The River is official!')
        app.fullFlopOut = True
    else:
        declareWinner(app)
    
    app.currentMinBet = app.buyInBet

    passFlop = []
    for c in app.flop:
        if not c.isHidden:
            passFlop.append(c)
    app.probabilities = app.allPlayers[0].simulateOutcomes(passFlop, 10000)

    for i in range(app.numPlayers):
        app.allPlayers[i].lastBet = 0

def drawSelectionScreen(app):
    drawImage(getImagePath('introScreen.png'), 0, 0, width=app.width, height=app.height)
    for i in range(6):
        label = f'{app.playerTypes[app.playerExists[i]]}' if i != 0 else 'This is You'
        drawLabel(label, 437, 210 + i*65,  align='center', size=20, bold=True)
        fillCol = 'white' if i == app.selectedPlayer else 'black'
        drawLabel(f'{app.playerNames[i]}', 170, 210 + i*65,  align='center', size=20, bold=True, fill=fillCol)

# redraws the entire app based on what screen is being displayed
def redrawAll(app):
    if app.screen == 'selection':
        drawSelectionScreen(app)
        return
    
    if app.showingInstructions:
        drawImage(getImagePath('instructions.png'), 0, 0, width=app.width, height=app.height)
        return
    
    drawImage(getImagePath('poker_table.png'), 0, 0, width=app.width, height=app.height)
    drawFlop(app)
    drawCurrentText(app)
    drawPlayerCards(app)
    drawPot(app)
    if app.showProbabilities:
        showProbabilities(app, app.width-600, app.height-310)

    # if app.winnerLabel: 
    #     drawRect(app.width/2, app.height/2, 400, 200, fill=rgb(231, 171, 60), border='black', align='center')
    #     drawLabel(f"{app.allPlayers[app.winner].name} WON {app.currentPot} !!", app.width/2, app.height/2, size=30, align='center', bold=True)

    if app.isPromptingRaise:
        handCenterX = app.width / 2
        handCenterY = app.height / 2 + ((app.height - 450) / 2)

        drawRect(handCenterX - 120, handCenterY + 40, 240, 50, fill=rgb(231, 171, 60), border='black')
        drawLabel("Your Raise:", handCenterX, handCenterY + 50, size=14, align='center') 
        drawLabel(app.currentInput, handCenterX, handCenterY + 70, size=18, align='center') 


def onStep(app):
    if app.screen == 'selection' or app.showingInstructions:
        return
    if app.createDelay: # create delay so players can see outcomes
        app.delayCount += 1
        app.winnerLabel = True
        if app.delayCount == 4:
            app.createDelay = False
            app.delayCount = 0
            app.winnerLabel = False
    else:
        moveOn = True
        for i in range(len(app.allPlayers)):
            if not (app.allPlayers[i].isFolded or app.allPlayers[i].lastBet == app.currentMinBet):
                moveOn = False
        if moveOn:
            if app.fullFlopOut and app.handsOut == False:
                revealAllHands(app)
                app.createDelay = True
                app.delayCount = 0
                app.handsOut = True
                return
            revealNextCardFlop(app)
            app.handsOut = False
            # moveOn = False
        else:
            if app.currentPlayer != 0:
                handleAIPlayerMove(app)
                nextPlayer(app)
                app.isPromptingRaise = False
            else:
                app.isPromptingRaise = True
    

def revealAllHands(app):
    for player in app.allPlayers:
        player.cards[0].isHidden = False
        player.cards[1].isHidden = False
    
# if player wants to raise, check if they have typed in a real number in the textbox
def finalizeRaise(app):
    if app.currentInput.isdigit():
        raiseAmount = int(app.currentInput)
        if raiseAmount > app.currentMinBet and raiseAmount <= app.allPlayers[app.currentPlayer].amount:
            app.currentMinBet = raiseAmount
            amountToAdd = raiseAmount - app.allPlayers[app.currentPlayer].lastBet
            app.allPlayers[app.currentPlayer].bet(amountToAdd)
            app.currentPot += amountToAdd
            app.allPlayers[app.currentPlayer].lastBet = app.currentMinBet
            addToCurText(app, f'You raised to {raiseAmount}.')
        else:
            addToCurText(app, "Invalid raise amount. It must be higher than the current bet and within your funds. You force match the bet.")
            handleUserPlayerMove(app, 'b')
    else:
        print("Invalid input.")
    app.isPromptingRaise = False
    app.currentInput = ''


def onMousePress(app, mouseX, mouseY):
    if app.screen == 'game' and not app.showingInstructions:
        if 615 < mouseX < 885 and 50 < mouseY < 100:
            app.showingInstructions = True
        return
    
    if app.showingInstructions:
        if 670 < mouseX < 830 and 425 < mouseY < 575: app.showingInstructions = False
        return

    if 200 < mouseX < 400 and 580 < mouseY < 630:
        startGame(app)
        return
    # print(f"Mouse pressed at ({mouseX}, {mouseY})")
    for i in range(6):
        if 340 < mouseX < 520 and ((185 + i*65) < mouseY < (235 + i*65)):
            app.playerExists[i] += 1
            app.playerExists[i] %= len(app.playerTypes)
            break
        elif 80 < mouseX < 260 and ((185 + i*65) < mouseY < (235 + i*65)):
            app.selectedPlayer = i



def onKeyPress(app, key):
    if app.showingInstructions:
        if key == 'esc':
            app.showingInstructions = False
        return
    if app.screen == 'selection':
        ind = app.selectedPlayer
        if key == 'backspace' and len(app.playerNames[ind]) > 0:
            app.playerNames[ind] = app.playerNames[ind][:-1]
        elif key.isdigit() or key.isalpha() and key != 'backspace':
            if app.playerNames[ind] == f'Player {ind+1}': app.playerNames[ind] = ''
            app.playerNames[ind] += key if key != 'space' else ' '
        return
    
    if app.isPromptingRaise:
        if key.isdigit():  
            app.currentInput += key
        elif key == 'backspace' and len(app.currentInput) > 0:
            app.currentInput = app.currentInput[:-1]

    if key == 'up':
        app.stepsPerSecond += 0.1
    if key == 'down' and app.stepsPerSecond > 0:
        app.stepsPerSecond -= 0.1
    
    if key == 'right' and app.textPos < len(app.curText)-1:
        app.textPos += 1
    
    if key == 'left' and app.textPos > 0:
        app.textPos -= 1

    if key == 'space':
        app.showProbabilities = not app.showProbabilities

    if key in ['b', 'f', 'r'] and app.currentPlayer == 0:
        handleUserPlayerMove(app, key)
        nextPlayer(app)


# Draws all the cards of the players, ensuring player 1 is centered at the bottom
def drawPlayerCards(app):
    tableCenterX = app.width / 2
    tableCenterY = app.height / 2
    # radiusX = (app.width - 300)/2
    # radiusY = (app.height - 450)/2
    radiusX = (app.width - 400)/2
    radiusY = (app.height - 550)/2

    for i in range(len(app.allPlayers)):
        player = app.allPlayers[i]
        angle = (360 / app.numPlayers) * i + 90 
        angleRad = math.radians(angle)
        handCenterX = tableCenterX + radiusX * math.cos(angleRad)
        handCenterY = tableCenterY + radiusY * math.sin(angleRad)
        for j in range(len(player.cards)):
            card = player.cards[j]
            x = handCenterX + (j - len(player.cards) / 2) * 80 
            y = handCenterY - 70
            if not player.isFolded:
                card.depict(x, y, width=70, height=100)
            else:
                drawRect(x, y, 70, 100, fill="gray", border="black", opacity=25, dashes=True)
        drawLabel(f'{player.name} - {player.amount}', handCenterX, handCenterY-85, size=16, bold=True, align='center')
        stillPlaying = 'Folded' if player.isFolded else 'Playing'
        colPlaying = 'red' if player.isFolded else 'blue'
        drawLabel(stillPlaying, handCenterX, handCenterY + 45, size=16, fill=colPlaying, align='center', bold=True)

# draws the active log of all previous moves
def drawCurrentText(app):
    rectWidth = 500
    rectHeight = 50
    rectX = (app.width - rectWidth) / 2
    rectY = app.height / 2 - 150
    drawRect(rectX, rectY, rectWidth, rectHeight, fill='white', border='black')
    drawLabel(app.curText[app.textPos], rectX + rectWidth / 2, rectY + rectHeight / 1.5, size=17, align='center', bold=True, fill='black')
    if app.textPos >= 1:
        drawLabel(app.curText[app.textPos-1], rectX + rectWidth / 2, rectY + rectHeight / 3, size=11, align='center', bold=True, fill='gray')


def drawFlop(app):
    flopLen = 5
    width = 70
    height = 100
    gapX = 20
    totFlopWidth = flopLen * width + (flopLen - 1) * gapX
    sx = (app.width - totFlopWidth) / 2 
    sy = app.height / 2 - height / 2
    for i in range(len(app.flop)):
        x = sx + i * (width + gapX)
        y = sy
        app.flop[i].depict(x, y, width, height)

def drawPot(app):
    flopLen = 5
    width = 70
    gapX = 20
    totFlopWidth = flopLen * width + (flopLen - 1) * gapX
    sx = (app.width - totFlopWidth) / 2
    sy = app.height / 2 - 50
    potX = sx + totFlopWidth / 2
    potY = sy + 130 
    drawLabel(f"Current Pot: ${app.currentPot}", potX, potY, size=20, bold=True, align="center")


def showProbabilities(app, xs, ys):
    cw = 150  
    ch = 30   
    nc = 2    

    headings = ["Hand Type", "Probability"]
    for col in range(nc):
        drawRect(xs + col * cw, ys, cw, ch, fill='lightgray', border='black')
        drawLabel(headings[col], xs + col * cw + cw / 2, ys + ch / 2, align='center', size=12, bold=True)

    # Draws data rows, uses variables definedabove
    for row in range(len(app.probabilities)):
        value = app.probabilities[row]
        handType = handLabels[row]  
        prob = f"{value * 100:.3f}%"  # Convert to percentage with 3 decimal places
        for col, cellValue in enumerate([handType, prob]):
            y_position = ys + (row + 1) * ch
            x_position = xs + col * cw
            drawRect(x_position, y_position, cw, ch, fill='white', border='black')
            colorVal = 'blue' if value > 0.1 else 'black'
            boldVal = value > 0.05
            drawLabel(cellValue, x_position + cw / 2, y_position + ch / 2, align='center', size=12, fill=colorVal, bold=boldVal)

# adds to log and prints in terminal
def addToCurText(app, text):
    print(text)
    app.textPos = len(app.curText)
    app.curText.append(text)

def main():
    runApp()
    

main()

# app.run()