#import pygame

class Button():
    def __init__(self, pygame, win, onPressed=None, x=0, y=0, height=0, width=0, text = ''):
        self.onPressed = onPressed
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.pygame = pygame
        self.win = win
        self.myFont = self.pygame.font.SysFont('Comic Sans MS', 18)
        self.text = self.myFont.render(text, False, (0,0,0), (255,255,255))
        if(self.width < self.text.get_width()):
            self.width = self.text.get_width()
    def draw(self):
        self.pygame.draw.rect(self.win, (255,255,255), (self.x - self.width/2, self.y - self.height/2, self.width, self.height))
        # self.win.blit(text,(self.x, self.y))
        self.win.blit(self.text, (self.x - self.text.get_width()/2, self.y - self.text.get_height()/2))

    def click(self, x, y):
        if(x > self.x - self.width/2 and x < self.x + self.width/2 and y > self.y - self.height/2 and y < self.y + self.height/2):
            if(self.onPressed != None):
                self.onPressed()