import pygame
from constants import pygameWindowWidth, pygameWindowDepth

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth, pygameWindowDepth))

    def Prepare(self):
        self.screen.fill((255, 255, 255))
        pygame.event.get()

    def Reveal(self):
        pygame.display.update()

    def drawBlackCircle(self, x, y):
        # import platform
        # print(platform.architecture())
        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 10)

    def Draw_Black_Line(self, xBase, yBase, xTip, yTip, boneWidth):
        pygame.draw.line(self.screen, (0, 0, 0), (xBase, yBase), (xTip, yTip), boneWidth)

    def Draw_Green_Line(self, xBase, yBase, xTip, yTip, boneWidth):
        pygame.draw.line(self.screen, (0, 200, 0), (xBase, yBase), (xTip, yTip), boneWidth)