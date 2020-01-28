from pygameWindow import PYGAME_WINDOW
import random

x = 400
y = 400

pygameWindow = PYGAME_WINDOW()

def Perturb_Circle_Position():
    global x, y
    fourSidedDieRoll = random.randint(1, 4)
    if fourSidedDieRoll == 1:
        x = x - 1
    elif fourSidedDieRoll == 2:
        x = x + 1
    elif fourSidedDieRoll == 3:
        y = y - 1
    else:
        y = y + 1

while True:
    pygameWindow.Prepare()
    pygameWindow.drawBlackCircle(x, y)
    pygameWindow.Reveal()
    Perturb_Circle_Position()

print(pygameWindow)