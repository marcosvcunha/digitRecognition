import numpy as np
from numpy import loadtxt
from joblib import dump, load
import matplotlib.pyplot as plt
import random
import tensorflow.keras.datasets.mnist as mnist
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

class Model():
    """
        Classe que organiza o modelo de ML usado, seleciona os dados a serem usados para treino e para teste.
    """
    def __init__(self, trainSize=60000, testSize=10000, trainOnCustomData=True, forceTrain=False):
        """Classe que gerencia o treino e os testes do modelo de predição.

        Args:
            trainSize (int, optional): Se trainOnCustomData=False, utiliza trainSize como número de amostras de treino. Defaults to 60000.
            testSize (int, optional): Se trainOnCustomData=False, utiliza test como número de amostras de teste. Defaults to 10000.
            trainOnCustomData (bool, optional): Se True, traina com um dataset gerado por mim, armazenado em testdata.npy, bem menor que o mnist, 
                porém funciona melhor para os dados digitados no DigitClassifier. Se False, treina com os dados do mnist. Defaults to True.
            forceTrain (bool, optional): Se True, força o modelo a retreinar, se False, primeiro tenta carregar o modelo salvo. Defaults to False.
        """
        self.trainSize = trainSize
        self.testSize = testSize
        self.trainOnCustomData = trainOnCustomData
        self.forceTrain = forceTrain

    def loadDigits(self):
        """
            Se trainOnCustomData = False, carrega os dados do dataset mnist para treino e teste,
            caso contrario utiliza os dados gravados em testdata.npy como treino e teste.
        """
        if(not self.trainOnCustomData):
            (X_train, y_train), (X_test, y_test) = mnist.load_data()
            X_train = np.reshape(X_train, (60000, 28*28))
            X_train[X_train > 0] = 255 # todos os elementos maiores que 0 são 255
            X_test = np.reshape(X_test, (10000, 28*28))
            X_test[X_test > 0] = 255
            X_train = X_train[:self.trainSize]
            y_train = y_train[:self.trainSize]
            X_test = X_test[:self.testSize]
            y_test = y_test[:self.testSize]
            self.X_train = X_train
            self.y_train = y_train
            self.X_test = X_test
            self.y_test = y_test
        else:
            (testData, testLabels) = self.loadCustomTestData()
            cut = int(testData.shape[0] * 0.9)
            self.X_train = testData[:cut]
            self.y_train = testLabels[:cut]
            self.X_test = testData[cut:]
            self.y_test = testLabels[cut:]
    
    def trainRFC(self):
        """Treina o modelo com o algoritmo RandomForestClassifier
        """
        self.loadDigits()
        if(not self.forceTrain):
            try:
                self.clf = load('rfcmodel.joblib')
                print('RFC Carregado!')
                return
            except:
                pass
        print('Treinando RFC')
        self.clf = RandomForestClassifier(random_state=42, n_estimators=100)
        self.clf.fit(self.X_train, self.y_train)
        dump(self.clf, 'rfcmodel.joblib')
        print('RFC Treinado')

    def trainSVM(self):
        """Treina o modelo com o algoritmo Suport Vector Machine
        """
        self.loadDigits()
        if(not self.forceTrain):
            try:
                self.clf = load('svmmodel.joblib')
                print('SVM Carregado!')
                return
            except:
                pass
        print('Treinando SVM')
        self.clf = svm.SVC()
        self.clf.fit(self.X_train, self.y_train)
        dump(self.clf, 'svmmodel.joblib')
        print('RFC Treinado')
    def getScore(self):
        score = self.clf.score(self.X_test, self.y_test)
        print('Pontuação do modelo:', score)

    def testAndDisplay(self, numDisplay=5):
        """
            Seleciona aleatoriamente numDisplay imagens do dataset de teste,
            gera as predições e mostra as imagens.
        Args:
            numDisplay (int): [Número de exemplos que serão mostrados]. Defaults to 5.
        """
        indexes = random.sample(range(self.X_test.shape[0]), numDisplay)
        X_test = [self.X_test[i] for i in indexes]
        y_test = [self.y_test[i] for i in indexes]
        pred = self.clf.predict(X_test)
        for i in range(numDisplay):
            plt.title('Numero: ' + str(y_test[i])  + ' Número previsto:' +  str(pred[i]))
            plt.imshow(np.reshape(X_test[i], (28,28)), cmap='Greys')
            plt.show()
    
    def predictSingleDigit(self, digit):
        pred = self.clf.predict([digit])
        return pred[0]
    
    def loadCustomTestData(self):
        data = np.load('testdata.npy', allow_pickle=True)
        testData = np.array([data[0][i] for i in range(data[0].shape[0])])
        testLabels = np.asarray(data[1], dtype=np.uint8)
        return (testData, testLabels)
    


        
if __name__ == '__main__':
    model = Model(trainOnCustomData=True)
    model.trainRFC()
    model.getScore()