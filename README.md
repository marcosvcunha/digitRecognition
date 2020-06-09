## digitRecognition
Este projeto desenvolvido em python consiste em uma interface que permite ao usuário escrever um digito e em um modelo de machine learning que classifica o digito escrito (0-9).

# A interface
A interface foi desenvolvida utilizado o modulo pygame e consiste em um quadro para desenhar um digito, e dois botoes: Apagar e Enviar. Ao clicar em enviar, o modelo de machine learning tenta prever o digito desenhado baseado no quadro atual.
Se o argumento 'createData' do DigitClassifier estiver setado para True, a interface funciona para gerar novos dados de treino que serão salvos em testedata.npy.
# Reconhecimento do digito
Para o reconhecimento do digito foi utilizada a classe Model, que gerencia o carregamento dos dados de treino e teste, faz o treinamento do modelo e faz a predição. 
Dois algoritmos de classificação são suportados: Suport Vector Machine e Random Forest Classifier.
# Dados de treino
Primeiramente foi usado o dataset mnist para o treinamento do modelo, porém o não mostrava bons resultados para predição dos dados gerados por este sistema.
Por fim, foram gerados dados neste mesmo sistema (digitados manualmente) para o treinamento. Os resultados foram bem superiores, portanto estes foram adotados como default.
