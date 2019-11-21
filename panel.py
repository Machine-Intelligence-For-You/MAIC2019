# Created by HaroldKS at 21/08/2018
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *


class Panel(QWidget):

    def __init__(self, board, playersName, parent = None):
        super(Panel, self).__init__(parent)
        self.board = board
        self.playersName = playersName
        layout = QVBoxLayout()
        layout.addStretch()

        #Arrow 1
        horizontal1 = QHBoxLayout()
        horizontal1.addStretch()
        self.arrowBlack = QLabel(self)
        self.arrowBlack.setFixedSize(20, 20)
        self.arrowBlack.setScaledContents(True)
        horizontal1.addWidget(self.arrowBlack)
        horizontal1.addStretch()
        layout.addLayout(horizontal1)

        #Image 1
        horizontal2 = QHBoxLayout()
        horizontal2.addStretch()
        image1 = QLabel(self)
        image1.setAlignment(QtCore.Qt.AlignCenter)
        image1.setFixedSize(100,100)
        image1.setScaledContents(True)
        image1.setPixmap(QtGui.QPixmap("pieces/profile_black.png"))
        horizontal2.addWidget(image1)
        horizontal2.addStretch()
        layout.addLayout(horizontal2)

        #Player 1 Name

        self.name1 = QLabel(self.playersName[0], self)
        self.name1.setAlignment(QtCore.Qt.AlignCenter)
        self.name1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.name1)

        #Score Player 1
        self.score1 =QLabel("0[12]", self)
        self.score1.setAlignment(QtCore.Qt.AlignCenter)
        self.score1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.score1)

        #Lost By Player 1
        lostWhiteLayout = QGridLayout()
        layout.addLayout(lostWhiteLayout)

        #Arrow 2
        horizontal3 = QHBoxLayout()
        horizontal3.addStretch()
        self.arrowWhite = QLabel(self)
        self.arrowWhite.setFixedSize(20, 20)
        self.arrowWhite.setScaledContents(True)
        horizontal3.addWidget(self.arrowWhite)
        horizontal3.addStretch()
        layout.addLayout(horizontal3)

        #Image 2
        horizontal4 = QHBoxLayout()
        horizontal4.addStretch()
        image2 = QLabel(self)
        image2.setAlignment(QtCore.Qt.AlignCenter)
        image2.setFixedSize(100,100)
        image2.setScaledContents(True)
        image2.setPixmap(QtGui.QPixmap("pieces/profile_white.png"))
        horizontal4.addWidget(image2)
        horizontal4.addStretch()
        layout.addLayout(horizontal4)

        #Player 2 Name
        self.name2 = QLabel(self.playersName[1], self)
        self.name2.setAlignment(QtCore.Qt.AlignCenter)
        self.name2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.name2)

        #Score Player 2
        self.score2 =QLabel("0[12]", self)
        self.score2.setAlignment(QtCore.Qt.AlignCenter)
        self.score2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        layout.addWidget(self.score2)


        #Lost By Player 2
        lostBlackLayout = QGridLayout()
        layout.addLayout(lostBlackLayout)

        layout.addStretch()
        self.setLayout(layout)
        self.updateCurrentPlayer(0)
        
        
    def updatePlayersName(self,playerNames):
        self.name1.setText(playerNames[0])
        self.name2.setText(playerNames[1])
    def setCurrentPlayer(self, player):
        pass

    def updateCurrentPlayer(self,currentPlayer):
        empty = QtGui.QPixmap(0,0)
        arrow = QtGui.QPixmap('pieces/arrow.png')

        if currentPlayer == 1:
            self.arrowWhite.setPixmap(arrow)
            self.arrowBlack.setPixmap(empty)
        else:
            self.arrowBlack.setPixmap(arrow)
            self.arrowWhite.setPixmap(empty)

    def resetPanelPlayer(self):
        empty = QtGui.QPixmap(0,0)
        arrow = QtGui.QPixmap('pieces/arrow.png')
        self.arrowWhite.setPixmap(empty)
        self.arrowBlack.setPixmap(arrow)



    def updateScore(self, score,pieces_in_hands):
        self.score1.setText(str(score[0])+"["+str(pieces_in_hands[0])+"]")
        self.score2.setText(str(score[1])+"["+str(pieces_in_hands[1])+"]")
