import pygame
import numpy as np
from numpy import savetxt
import random
import json

class Board:
    ROWS = COLS = 28
    squareSize = 20
    def __init__(self, height=0, width=0, createData=False):
        """[summary]

        Args:
            height (int, optional): [description]. Defaults to 0.
            width (int, optional): [description]. Defaults to 0.
            createData (bool, optional): Se True: Carrega o dataset armazenado localmente em 'testdata.npy', para que 
            quando a função getNewNumber seja chamada, o dado atual seja salvo junto aos antigos. Defaults to False.
        """
        self.data = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.x = 0
        self.y = 0
        self.height = height
        self.width = width
        self.numberToDraw = random.randint(0, 9)
        if(createData):
            try:
                self.loadCustomTestData()
            except:
                self.testData = []
                self.testLabels = []

    def setSquare(self, xClick, yClick):
        x = int(xClick / self.squareSize)
        y = int(yClick / self.squareSize)
        adjX = min([x+1, self.ROWS - 1])
        adjY = min([y+1, self.COLS - 1])
        self.data[x][y] = 255
        self.data[adjX][y] = 255
        self.data[adjX][adjY] = 255
        self.data[x][adjY] = 255

    def getNewNumber(self):
        """Adiciona o desenho atual e o label(número que a pessoa deve escrever) a lista de dados carregados e salva em testdata.npy
        """
        self.testData.append(np.array(np.reshape(np.transpose(self.data), 784), dtype=np.uint8))
        self.testLabels.append(self.numberToDraw)
        np.save('testdata.npy', np.asarray([self.testData, self.testLabels]))
        # with open('testdata.txt', 'w') as f:
        #     json.dump([self.testData, self.testLabels].toList(), f)
        self.numberToDraw = random.randint(0, 9)
        self.clearBoard()

    def loadCustomTestData(self):
        data = np.load('testdata.npy', allow_pickle=True)
        self.testData = list(data[0])
        self.testLabels = list(data[1])

    def draw(self, game, win):
        game.draw.rect(win, (125,125,125), (self.x, self.y, self.width, self.height))
        for x in range(self.COLS):
            for y in range(self.ROWS):
                pass
                if(self.data[x][y] == 255):
                    game.draw.rect(win, (0,0,0), (x * self.squareSize, y * self.squareSize, self.squareSize, self.squareSize))
    
    def saveData(self):
        """Utilizado para salvar um unico digito em data.csv para ser utilizado na predição em tempo real.
        """
        savetxt('data.csv', np.array(np.reshape(np.transpose(self.data), 784), dtype=np.uint8), delimiter=',')
    
    def getBoard(self):
        return np.array(np.reshape(np.transpose(self.data), 784), dtype=np.uint8)

    def clearBoard(self):
        self.data = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]