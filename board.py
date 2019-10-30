TILES_COLOR = ["black", "white"]

from PyQt5.QtWidgets import *
from piece import Piece
from boardSquare import BoardSquare


class Board(QWidget):
    def __init__(self, row, col, parent = None):
        super(Board, self).__init__(parent)
        self.currentPlayer = 0
        self.color = ["black", "white"]
        self.score = [0, 0]
        self.setFixedSize(100 * col, 100 * row)
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)
        self.blackColor = "brown"
        self.whiteColor = "#E0EEF1"
        self.selectColor = "blue"
        self.attackColor = "red"
        self.squares = list()
        self.row=row
        self.col=col
        self.grid = [[None for _ in range(row)] for _ in range(col)]
        self.currentPlayer = 0
        for i in range(row):
            tempList = list()
            for j in range(col):
                square = BoardSquare(i, j)
                gridLayout.addWidget(square, row-i, j)
                tempList.append(square)
            self.squares.append(tempList)
        self.setDefaultColors()
        self.setLayout(gridLayout)


    def add_piece(self, cell, player_number):
        x,y=cell[0],cell[1]
        self.squares[x][y].setPiece(Piece(1, TILES_COLOR[player_number]))
        # self.grid[cell[0]][cell[1]]=TILES_COLOR[player_number]

    def move_piece(self, initial_cell, destination_cell, player_number):
        x, y = destination_cell[0],destination_cell[1]
        self.squares[x][y].setPiece(Piece(1, TILES_COLOR[player_number]))
        # self.add_tile(destination_cell)
        x,y=initial_cell[0],initial_cell[1]
        self.squares[x][y].removePiece()
        # self.remove_tile(initial_cell)

    def remove_piece(self, cell):
        x,y=cell[0],cell[1]
        self.squares[x][y].removePiece()

    def setDefaultColors(self):
        for i in range(self.row):
            for j in range(self.col):
                if i%2 == 0:
                    if j%2 == 0:
                        self.squares[i][j].setBackgroundColor(self.blackColor)
                    else:
                        self.squares[i][j].setBackgroundColor(self.whiteColor)
                else:
                    if j%2 == 0:
                        self.squares[i][j].setBackgroundColor(self.whiteColor)
                    else:
                        self.squares[i][j].setBackgroundColor(self.blackColor)

    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    def resetBoard(self):
        for i in range(self.row):
            for j in range(self.col):
                self.squares[i][j].removePiece()

    def activeAllSquares(self):
        for i in range(self.row):
            for j in range(self.col):
                self.squares[i][j].setActive(True)

    def desactiveAllSquares(self):
        for i in range(self.roc):
            for j in range(self.col):
                self.squares[i][j].setActive(False)

    def putListBoard(self, listBoard):
        for i in range(len(self.self.squares)):
            for j in range(len(self.self.squares[0])):
                if listBoard[i][j] == None:
                    self.squares[i][j].removePiece()
                elif listBoard[i][j] == "black":
                    self.squares[i][j].setPiece(Piece(0, "black"))
                elif listBoard[i][j] == "white":
                    self.squares[i][j].setPiece(Piece(1, "white"))

    def get_board_array(self):
        list_board = []
        for i in range(len(self.squares)):
            temp = []
            for j in range (len(self.squares[0])):
                if not self.squares[i][j].isPiece():
                    temp.append(None)
                else:
                    temp.append(self.squares[i][j].piece.getColor())
            list_board.append(temp)
        return list_board
