import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import Leap
import pickle
import numpy as np
import pygame
import time
import random
import math

from pygameWindow import PYGAME_WINDOW
from constants import pygameWindowWidth, pygameWindowDepth

# ======================================================================================================================

path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 9/"
clf = pickle.load(open(path + "userData/classifier.p", 'rb'))
global programState
programState = 0
global testData
testData = np.zeros((1, 30), dtype = 'f')
global controller
controller = Leap.Controller()
global frame
frame = controller.frame()
global success
success = False
global aslNum
aslNum = random.randint(0, 9)
global predictedClass
predictedClass = -2
global database
database = pickle.load(open(path + 'userData/database.p', 'rb'))
global userName
global userRecord
global loops
loops = 0
global currentLoops
currentLoops = 0
global myFont
global firstRun
firstRun = True
global startTime
# startTime = time.time()
global elapsedTime
global expired
expired = False
global numCorrectThisSession
numCorrectThisSession = 0
global numCorrectLastSession
numCorrectLastSession = 0
global currentlySigningCurrectly
currentlySigningCurrectly = False
global firstTry
firstTry = True
global startTime2
startTime2 = 0
global mathMode
mathMode = False
global equation
equation = ""

# ======================================================================================================================

x = 400
y = 400

xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

pygameX = 0
pygameY = 0

pygameWindow = PYGAME_WINDOW()

# ======================================================================================================================

def login():
    global numCorrectLastSession
    global mathMode
    global equation

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    userName = raw_input('Please enter your name: ')
    mathModeInput = raw_input('Would you like to enable Math Mode? (Y or N) ')
    if (mathModeInput == 'Y'):
        mathMode = True
        a = random.randint(0, aslNum)
        b = aslNum - a
        equation = str(a) + " + " + str(b) + " = ?"
    else:
        mathMode = False
    if userName in database:
        print('welcome back ' + userName + '.')
        database[userName][0] = "logins: " + str(int(database.get(userName)[0][8:]) + 1)
        numCorrectLastSession = int(database.get(userName)[21][15:])
        database[userName][21] = "Total Correct: " + str(0)
    else:
        database[userName] = {}
        print('welcome ' + userName + '.')
        database[userName] = ["logins: " + str(1), "0 Attempted: 0", "1 Attempted: 0",
                              "2 Attempted: 0", "3 Attempted: 0", "4 Attempted: 0", "5 Attempted: 0", "6 Attempted: 0",
                              "7 Attempted: 0", "8 Attempted: 0", "9 Attempted: 0", "0 Success: 0", "1 Success: 0", "2 Success: 0", "3 Success: 0", "4 Success: 0", "5 Success: 0", "6 Success: 0", "7 Success: 0", "8 Success: 0", "9 Success: 0", "Total Correct: 0"]

    return userName

# ======================================================================================================================

def Scale(origVal, leapLo, leapHi, pygameLo, pygameHi):
    if leapLo != leapHi:
        return ((abs(pygameHi - pygameLo)) * (abs(leapLo - origVal))) / (abs(leapHi - leapLo))
    else:
        return abs(pygameHi - pygameLo) / 2

# ======================================================================================================================

def CenterData(testData):
    xCoords = testData[0, ::3]
    xMean = xCoords.mean()
    testData[0, ::3] = xCoords - xMean

    yCoords = testData[0, 1::3]
    yMean = yCoords.mean()
    testData[0, 1::3] = yCoords - yMean

    zCoords = testData[0, 2::3]
    zMean = zCoords.mean()
    testData[0, 2::3] = zCoords - zMean

    return testData

# ======================================================================================================================

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax

    x = int(v[0])
    y = int(v[2])

    if ( x < xMin ):
        xMin = x
    if ( x > xMax ):
        xMax = x
    if ( y < yMin ):
        yMin = y
    if ( y > yMax ):
        yMax = y

    x = Scale(x, xMin, xMax, 0, pygameWindowWidth/2)
    y = Scale(y, yMin, yMax, 0, pygameWindowDepth/2)

    return (x, y)

# ======================================================================================================================

def Handle_Bone(bone, boneWidth):
    global xTip, yTip, zTip
    global currentlySigningCurrectly

    base = bone.prev_joint
    tip = bone.next_joint

    (xBase, yBase) = Handle_Vector_From_Leap(base)
    (xTip, yTip) = Handle_Vector_From_Leap(tip)

    if (currentlySigningCurrectly == True):
        PYGAME_WINDOW.Draw_Green_Line(pygameWindow, xBase, yBase, xTip, yTip, boneWidth)
    else:
        PYGAME_WINDOW.Draw_Black_Line(pygameWindow, xBase, yBase, xTip, yTip, boneWidth)

# ======================================================================================================================

def Handle_Finger(finger):
    global k
    global bone
    global boneWidth
    global testData

    for b in range(4):
        bone = finger.bone(b)
        base = bone.prev_joint
        tip = bone.next_joint
        xTip = int(tip[0])
        yTip = int(tip[1])
        zTip = int(tip[2])
        boneWidth = 0
        if (b == 0):
            boneWidth = 6
        elif (b == 1):
            boneWidth = 4
        elif (b == 2):
            boneWidth = 3
        elif (b == 3):
            boneWidth = 2
        Handle_Bone(finger.bone(b), boneWidth)
        if ((b == 0) or (b == 3)):
            testData[0, k] = xTip
            testData[0, k + 1] = yTip
            testData[0, k + 2] = zTip
            k = k + 3

# ======================================================================================================================

def Handle_Frame(frame):
    global predictedClass
    global k
    global testData
    global x, y
    global xMin, xMax, yMin, yMax
    k = 0
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)
    # print(testData)
    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)
    # print(predictedClass)

# ======================================================================================================================

def handlePosition():
    global aslNum
    global database
    global userName
    global userRecord
    global loops
    global currentLoops
    global myFont
    global numCorrectThisSession
    global numCorrectLastSession
    global mathMode
    global equation

    base = bone.prev_joint

    # ------------------------------------------------------------------------------------------------------------------

    pygame.draw.rect(pygameWindow.screen, (0, 0, 0), pygame.Rect(70, 530, 300, 50), 10)
    textsurface = myFont.render('# Correct digits this session: ' + str(numCorrectThisSession), False, (0, 0, 0))
    pygameWindow.screen.blit(textsurface, (25, 430))
    textsurface = myFont.render('# Correct digits last session: ' + str(numCorrectLastSession), False, (0, 0, 0))
    pygameWindow.screen.blit(textsurface, (25, 470))
    if (numCorrectLastSession != 0 and 300 * (numCorrectThisSession / float(numCorrectLastSession)) <= 300):
        pygame.draw.rect(pygameWindow.screen, (0, 200, 0), pygame.Rect(73, 534, (300 * (numCorrectThisSession / float(numCorrectLastSession))) - 6, 40))
    else:
        pygame.draw.rect(pygameWindow.screen, (0, 200, 0), pygame.Rect(73, 534, 300 - 6, 40))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    userNm = userName
    highestNumTimes = 0
    for key in database:
        if ((int(database.get(key)[aslNum + 11][11:]) >= highestNumTimes) and (userName != key)):
            highestNumTimes = int(database.get(key)[aslNum + 11][11:])
            userNm = key
    if (mathMode == True):
        textsurface = myFont.render("Max Times Other Users Signed \'" + "?" + "\':", False, (0, 0, 0))
    else:
        textsurface = myFont.render("Max Times Other Users Signed \'" + str(aslNum) + "\':", False, (0, 0, 0))
    textsurface2 = ""
    textsurface2 = myFont.render(str(int(database.get(userNm)[aslNum + 11][11:])) + " (" + userNm + ")", False, (0, 0, 0))
    pygameWindow.screen.blit(textsurface, (10, 630))
    pygameWindow.screen.blit(textsurface2, (10, 670))
    if (mathMode == True):
        textsurface = myFont.render("Max Times You Have Signed \'" + "?" + "\':", False, (0, 0, 0))
    else:
        textsurface = myFont.render("Max Times You Have Signed \'" + str(aslNum) + "\':", False, (0, 0, 0))
    textsurface2 = myFont.render(str(int(database.get(userName)[aslNum + 11][11:])) + " (You)", False, (0, 0, 0))
    pygameWindow.screen.blit(textsurface, (10, 710))
    pygameWindow.screen.blit(textsurface2, (10, 750))
    if ((highestNumTimes >= int(database.get(userName)[aslNum + 11][11:])) and highestNumTimes != 0):
        pygame.draw.rect(pygameWindow.screen, (50, 50, 50), pygame.Rect(150, 662, 250, 40))
        pygame.draw.rect(pygameWindow.screen, (50, 50, 50), pygame.Rect(150, 742, 250 * (int(database.get(userName)[aslNum + 11][11:]) / float(highestNumTimes)), 40))
    elif ((highestNumTimes < int(database.get(userName)[aslNum + 11][11:])) and int(database.get(userName)[aslNum + 11][11:]) != 0):
        pygame.draw.rect(pygameWindow.screen, (50, 50, 50), pygame.Rect(150, 662, 250 * (int(database.get(userNm)[aslNum + 11][11:]) / float(database.get(userName)[aslNum + 11][11:])), 40))
        pygame.draw.rect(pygameWindow.screen, (50, 50, 50), pygame.Rect(150, 742, 250, 40))

    # ------------------------------------------------------------------------------------------------------------------

    if (base[0] < -125 ) and (base[2] > 125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/upRight.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[0] < -125) and (base[2] < -125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/downRight.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[0] > 125) and (base[2] > 125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/upLeft.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[0] > 125) and (base[2] < -125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/downLeft.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[0] < -125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/right.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[0] > 125 and success == False):
        pygameWindow.screen.blit(pygame.image.load(path + "images/left.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[2] > 125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/up.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    elif (base[2] < -125) and success == False:
        pygameWindow.screen.blit(pygame.image.load(path + "images/down.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))

    # ------------------------------------------------------------------------------------------------------------------

    if (aslNum == 0 and mathMode != True):
        if (int(database.get(userName)[11][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/zero.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/zeroPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][1] = "0 Attempted: " + str(int(database.get(userName)[1][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[1][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 1 and mathMode != True):
        if (int(database.get(userName)[12][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/one.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/onePro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][2] = "1 Attempted: " + str(int(database.get(userName)[2][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[2][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 2 and mathMode != True):
        if (int(database.get(userName)[13][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/two.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/twoPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][3] = "2 Attempted: " + str(int(database.get(userName)[3][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[3][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 3 and mathMode != True):
        if (int(database.get(userName)[14][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/three.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/threePro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][4] = "3 Attempted: " + str(int(database.get(userName)[4][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[4][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 4 and mathMode != True):
        if (int(database.get(userName)[15][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/four.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/fourPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][5] = "4 Attempted: " + str(int(database.get(userName)[5][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[5][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 5 and mathMode != True):
        if (int(database.get(userName)[16][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/five.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 16, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/fivePro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 16, 420))
        if (currentLoops == loops):
            database[userName][6] = "5 Attempted: " + str(int(database.get(userName)[6][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[6][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 6 and mathMode != True):
        if (int(database.get(userName)[17][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/six.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/sixPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][7] = "6 Attempted: " + str(int(database.get(userName)[7][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[7][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 7 and mathMode != True):
        if (int(database.get(userName)[18][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/seven.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/sevenPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][8] = "7 Attempted: " + str(int(database.get(userName)[8][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[8][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 8 and mathMode != True):
        if (int(database.get(userName)[19][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/eight.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/eightPro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][9] = "8 Attempted: " + str(int(database.get(userName)[9][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[9][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    elif (aslNum == 9 and mathMode != True):
        if (int(database.get(userName)[20][11:]) < 1):
            pygameWindow.screen.blit(pygame.image.load(path + "images/nine.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        else:
            pygameWindow.screen.blit(pygame.image.load(path + "images/ninePro.png"),
                                     ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 420))
        if (currentLoops == loops):
            database[userName][10] = "9 Attempted: " + str(int(database.get(userName)[10][13:]) + 1)
        textsurface = myFont.render('Times Attempted: ' + str(database.get(userName)[10][13:]), False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 750))

    # ------------------------------------------------------------------------------------------------------------------

    if (mathMode == True):
        textsurface = myFont.render("Please sign answer:", False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface, (500, 650))
        textsurface2 = myFont.render(equation, False, (0, 0, 0))
        pygameWindow.screen.blit(textsurface2, (480, 690))

    # ------------------------------------------------------------------------------------------------------------------

    currentLoops += 1

# ======================================================================================================================

def HandleState0():
    global programState
    global startTime
    startUpImg = pygame.image.load(path + "images/leapGirl.jpg")
    pygameWindow.screen.blit(startUpImg, ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
    if (len(frame.hands) > 0):
        programState = 1

# ======================================================================================================================

def HandleState1():
    global programState
    global startTime

    # handlePosition()

    if (len(frame.hands) == 0):
        programState = 0
    elif (len(frame.hands) > 0):
        programState = 2
        if (int(database.get(userName)[aslNum + 11][11:]) >= 1):
            startTime = time.time()


# ======================================================================================================================

def HandleState2():
    global programState
    global success
    global aslNum
    global predictedClass
    global loops
    global currentLoops
    global firstRun
    global database
    global userName
    global startTime
    global elapsedTime
    global expired
    global numCorrectThisSession
    global currentlySigningCurrectly
    global bone
    global boneWidth
    global frame
    global startTime2
    global firstTry
    global equation
    global mathMode

    # ------------------------------------------------------------------------------------------------------------------

    if (len(frame.hands) == 0):
        programState = 0

    handlePosition()

    # ------------------------------------------------------------------------------------------------------------------

    if (aslNum == predictedClass or aslNum == 8):
        if (firstTry == True):
            firstTry = False
            startTime2 = time.time()
            currentlySigningCurrectly = True
        if ((time.time() - startTime2) > 2):
            success = True
        predictedClass = clf.Predict(testData)
        if (aslNum != predictedClass):
            success = False
            currentlySigningCurrectly = False
            firstTry = True
        if (aslNum == 8):
            success = True
            currentlySigningCurrectly = True
            time.sleep(1)
    else:
        success = False
        currentlySigningCurrectly = False
        firstTry = True
        if (int(database.get(userName)[aslNum + 11][11:]) >= 1):
            elapsedTime = time.time() - startTime
            if (elapsedTime > 5 and mathMode == False):
                pygameWindow.screen.blit(pygame.image.load(path + "images/x.png"),
                                         ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
                textsurface = myFont.render('Time EXPIRED', False, (200, 0, 0))
                textsurface2 = myFont.render('5 Seconds are up!', False, (200, 0, 0))
                pygameWindow.screen.blit(textsurface, (550, 370))
                pygameWindow.screen.blit(textsurface2, (530, 410))
                aslNum = aslNum + 1
                if (aslNum == 10):
                    aslNum = 0
                expired = True

    # ------------------------------------------------------------------------------------------------------------------

    if (success == True):
        numCorrectThisSession = numCorrectThisSession + 1
        database[userName][aslNum + 11] = str(aslNum) + " Success: " + str(int(database.get(userName)[aslNum + 11][11:]) + 1)
        database[userName][21] = "Total Correct: " + str(int(database.get(userName)[21][15:]) + 1)
        highSuccessNum = 0

        for i in range(11, 21):
            if (int(database.get(userName)[i][11:]) > highSuccessNum):
                highSuccessNum = int(database.get(userName)[i][11:])
        lowSuccessNum = highSuccessNum
        lowSuccessNumIndex = 20
        for i in range(11, 21):
            if (int(database.get(userName)[i][11:]) < lowSuccessNum):
                lowSuccessNum = int(database.get(userName)[i][11:])
                lowSuccessNumIndex = i
        aslNum = int(database.get(userName)[lowSuccessNumIndex][0])
        if (mathMode == True):
            a = random.randint(0, aslNum)
            b = aslNum - a
            if (numCorrectThisSession < 3):
                equation = str(a) + " + " + str(b) + " = ?"
            elif (numCorrectThisSession >= 3 and numCorrectThisSession < 6):
                equation = "a = " + str(a) + ", b = " + str(b) + " + a, b = ?"
            else:
                equation = "a = " + str(a) + ", b = " + str(b) + " - a, b + 2a = ?"
        programState = 3
        pygameWindow.screen.blit(pygame.image.load(path + "images/check.png"),
                                 ((pygameWindowWidth / 2) + (pygameWindowWidth) / 8, 30))
        loops += 1
        currentLoops = loops

# ======================================================================================================================

def HandleState3():
    global success
    global programState
    global startTime
    global elapsedTime
    global currentlySigningCurrectly
    global firstTry

    programState = 1
    success = False
    currentlySigningCurrectly = False
    firstTry = True
    time.sleep(3)

# ======================================================================================================================

# global controller
# controller = Leap.Controller()
# global frame

global database
global userName
global myFont
global startTime
global expired

userName = login()

# myFont = pygame.font.SysFont('None', 30)
myFont = pygame.font.Font('freesansbold.ttf', 26)
pygame.font.init()

# ----------------------------------------------------------------------------------------------------------------------

while True:
    pygameWindow.Prepare()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    if (programState == 0):
        HandleState0()
    elif (programState == 1):
        HandleState1()
    elif (programState == 2):
        if (expired == True):
            time.sleep(5)
            if (int(database.get(userName)[aslNum + 11][11:]) >= 1):
                startTime = time.time()
            expired = False
        HandleState2()
    elif (programState == 3):
        HandleState3()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
    pygameWindow.Reveal()

    pickle.dump(database, open(path + 'userData/database.p', 'wb'))