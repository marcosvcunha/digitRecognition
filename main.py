import pygame
from board import Board
from button import Button
from model import Model
from textField import TextField

class DigitClassifier():
    def __init__(self, createData=False):
        """
            Cria a interface, inicia o board para fazer o desenho e integra tudo com o classifier.
        Args:
            createData (bool, optional): Deve ser setado para True para utilizar o sistema para
                gerar novos dados para treino e teste. Defaults to False.
        """
        pygame.init()
        pygame.font.init()
        self.createData = createData
        self.win = pygame.display.set_mode((760, 560))
        self.board = Board(height=560, width=560, createData=self.createData)
        self.objs = []
        self.guessNum = ''
        if(not self.createData):
            self.model = Model(trainOnCustomData=True)
            self.model.trainRFC()
            # self.model.trainRFC(forceTrain=True)
            self.objs.append(Button(pygame, self.win, x=660, y=350, height=50,
                                    width=120, onPressed=self.doPrediction, text='Salvar'))
        else:
            self.objs.append(Button(pygame, self.win, x=660, y=350, height=50,
                                    width=120, onPressed=self.board.getNewNumber, text='Enviar'))

        self.objs.append(Button(pygame, self.win, x=660, y=280, height=50,
                                    width=120, onPressed=self.board.clearBoard, text='Apagar'))

    def doPrediction(self):
        self.guessNum = self.model.predictSingleDigit(self.board.getBoard())


    def drawObjs(self):
        self.board.draw(pygame, self.win)
        for obj in self.objs:
            obj.draw()
        if(self.createData):
            ## Mostra o digito que a pessoa deve escrever
            textField = TextField(pygame, self.win, 660, 140, text=str(self.board.numberToDraw), fontSize=32)
            textField.draw()
        else:
            textField = TextField(pygame, self.win, 660, 100, text=str('Predição: '), fontSize=32)
            textField.draw()
            textField = TextField(pygame, self.win, 660, 140, text=str(self.guessNum), fontSize=32)
            textField.draw()

    def clicks(self, x, y):
        for obj in self.objs:
            obj.click(x, y)

    def run(self):
        pygame.display.set_caption('My Game')
        mousePressed = False
        gameOver = False

        while not gameOver:
            self.win.fill((0x4D, 0x49, 0xff))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    mousePressed = True
                    self.clicks(event.dict['pos'][0], event.dict['pos'][1])
                    if(event.dict['pos'][0] < 560):
                        self.board.setSquare(
                            event.dict['pos'][0], event.dict['pos'][1])
                if(event.type == pygame.MOUSEBUTTONUP):
                    mousePressed = False
                if(event.type == pygame.MOUSEMOTION):
                    if(mousePressed and event.dict['pos'][0] < 560):
                        self.board.setSquare(
                            event.dict['pos'][0], event.dict['pos'][1])
            self.drawObjs()
            pygame.display.update()


if __name__ == '__main__':
    game = DigitClassifier()
    game.run()
