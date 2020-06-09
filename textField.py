class TextField():
    def __init__(self, pygame, win, x, y, text='', fontSize=18):
        self.pygame = pygame
        self.win = win
        self.x = x
        self.y = y
        self.text = text
        self.fontSize = fontSize

    def draw(self):
        self.myFont = self.pygame.font.SysFont('Comic Sans MS', self.fontSize)
        text = self.myFont.render(self.text, False, (0,0,0))
        self.win.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))
    
    def click(self):
        pass
