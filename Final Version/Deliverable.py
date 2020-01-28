import os,sys,inspect, shutil
import numpy as np
import pickle
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import Leap

from pygameWindow_Del03 import PYGAME_WINDOW
from constants import pygameWindowWidth, pygameWindowDepth

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

controller = Leap.Controller()

# ======================================================================================================================

class DELIVERABLE:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.xMin = 1000
        self.xMax = -1000
        self.yMin = 1000
        self.yMax = -1000
        self.currentNumberOfHands = 0
        self.previousNumberOfHands = 0
        self.gestureData = np.zeros((5, 4, 6), dtype='f')
        self.fileIndex = 0
        self.Recreate_userData_Directory()

    # ==================================================================================================================

    def Recreate_userData_Directory(self):
        path = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 3/userData"
        shutil.rmtree(path)
        os.mkdir(path)

    # ==================================================================================================================

    def Scale(self, origVal, leapLo, leapHi, pygameLo, pygameHi):
        if leapLo != leapHi:
            return ((abs(pygameHi - pygameLo)) * (abs(leapLo - origVal))) / (abs(leapHi - leapLo))
        else:
            return abs(pygameHi - pygameLo) / 2

    # ==================================================================================================================

    def Handle_Vector_From_Leap(self, v):
        global xMin, xMax, yMin, yMax
        x = int(v[0])
        y = int(v[2])
        if (x < xMin):
            xMin = x
        if (x > xMax):
            xMax = x
        if (y < yMin):
            yMin = y
        if (y > yMax):
            yMax = y
        x = self.Scale(x, xMin, xMax, 0, pygameWindowWidth)
        y = self.Scale(y, yMin, yMax, 0, pygameWindowDepth)
        return (x, y)

    # ==================================================================================================================

    def Recording_Is_Ending(self):
        if (self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2):
            return True

    # ==================================================================================================================

    def Handle_Bone(self, bone, boneWidth, i, j):
        base = bone.prev_joint
        tip = bone.next_joint

        if self.Recording_Is_Ending():
            self.gestureData[i, j, 0] = base[0]
            self.gestureData[i, j, 1] = base[1]
            self.gestureData[i, j, 2] = base[2]
            self.gestureData[i, j, 3] = tip[0]
            self.gestureData[i, j, 4] = tip[1]
            self.gestureData[i, j, 5] = tip[2]

        (xBase, yBase) = self.Handle_Vector_From_Leap(base)
        (xTip, yTip) = self.Handle_Vector_From_Leap(tip)
        r = 0
        g = 250
        b = 0
        if (self.currentNumberOfHands == 2):
            r = 200
            g = 0
            b = 0
        PYGAME_WINDOW.Draw_Line(pygameWindow, xBase, yBase, xTip, yTip, boneWidth, r, g, b)

    # ==================================================================================================================

    def Handle_Finger(self, finger, i):
        for j in range(4):
            boneWidth = 0
            if (j == 0):
                boneWidth = 6
            elif (j == 1):
                boneWidth = 4
            elif (j == 2):
                boneWidth = 3
            elif (j == 3):
                boneWidth = 2
            self.Handle_Bone(finger.bone(j), boneWidth, i, j)

    # ==================================================================================================================

    def Handle_Frame(self, frame):
        global x, y
        global xMin, xMax, yMin, yMax
        hand = frame.hands[0]
        fingers = hand.fingers
        for i in range(5):
            self.Handle_Finger(fingers[i], i)
        if self.Recording_Is_Ending():
            self.Save_Gesture()

    # ==================================================================================================================

    def Save_Gesture(self):
        file_string = os.getcwd() + "/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/Del 3/userData/gesture" + str(self.fileIndex) + ".p"
        self.fileIndex += 1
        pickle_out = open(file_string, "wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()

    # ==================================================================================================================

    def Run_Once(self):
        pygameWindow.Prepare()
        frame = controller.frame()
        if (len(frame.hands) == 1):
            self.currentNumberOfHands = 1
        elif (len(frame.hands) == 2):
            self.currentNumberOfHands = 2
        else:
            self.currentNumberOfHands = 0

        if (len(frame.hands) > 0):
            self.Handle_Frame(frame)

        if len(frame.hands) == 1:
            self.previousNumberOfHands = 1
        elif len(frame.hands) == 2:
            self.previousNumberOfHands = 2
        else:
            self.previousNumberOfHands = 0
        pygameWindow.Reveal()

    # ==================================================================================================================

    def Run_Forever(self):
        while True:
            self.Run_Once()

