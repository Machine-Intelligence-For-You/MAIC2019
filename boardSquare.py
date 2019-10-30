
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *


class BoardSquare(QLabel, QWidget, QtCore.QObject):

    def __init__(self, col, row, parent = None):
        super(BoardSquare, self).__init__(parent)
        #Dimensions
        self.setMinimumSize(100, 100)
        self.setScaledContents(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.trigger = QtCore.pyqtSignal(int, int)
        self.col = col
        self.row = row

        #In Game
        self.piece = None
        self.active = False
        self.setStatusTip(self.toNotation())
        #SquareColor
        if col%2 == 0:
            if row%2 == 0:
                self.__setColor(1)
                self.backgroundColor = "grey"
            else:
                self.__setColor(0)
                self.backgroundColor = "white"
        else:
            if row%2 == 0:
                self.__setColor(0)
                self.backgroundColor = "white"
            else:
                self.__setColor(1)
                self.backgroundColor = "grey"

    def Active(self, active):
        self.active = active
        self.setStyleSheet('QLabel { background-color : ' + self.backgroundColor + '; }')


    def setActive(self, color):
        if(type(color)==str):
            self.active = True
            self.setStyleSheet('QLabel { background-color : ' + color + '; }')
        elif(type(color)==bool):
            self.active = color
            self.setStyleSheet('QLabel { background-color : ' + self.backgroundColor + '; }')


    def isPiece(self):
        if self.piece == None:
            return False
        return True

    def isActive(self):
        return self.active

    def getPiece(self):
        return self.piece

    def setPiece(self, piece):
        self.piece = piece
        self.setPixmap(piece.getImage())
        self.setStatusTip(self.toNotation() + " - " + self.piece.color)


    def removePiece(self):
        self.piece = None
        empty = QtGui.QPixmap(0, 0)
        self.setPixmap(empty)
        self.setStatusTip(self.toNotation())


    def __setColor(self, color):

        if color == 0:
            self.setStyleSheet("""QLabel { background-color : white; } """)
        elif color == 1:
            self.setStyleSheet("""QLabel { background-color : grey; } """)
        else:
            raise Exception("Incorrect chess square color")
        self.color = color

    def setBackgroundColor(self, color):
        self.backgroundColor = color
        self.setStyleSheet('QLabel { background-color : ' + color + '; }')

    def toNotation(self):
        coordinates = str()
        x = self.col + 49
        y = self.row + 65
        if self.col>=0 and self.col<self.col and self.row>=0 and self.row<self.row:
            coordinates += str(str(x) + " ")
            coordinates += str(str(y) + " ")
        return coordinates
