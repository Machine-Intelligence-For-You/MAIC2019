from PyQt5 import QtGui


class Piece:
    def __init__(self, player_number, color):
        self.moveNumber = 0
        self.color = color
        self.player = player_number

        if color == "green":
            self.image_url = "pieces/CV.png"
        else:
            self.image_url = "pieces/CB.png"

    def getImage(self):
        pixmap = QtGui.QPixmap()
        pixmap.load(self.image_url)
        pixmap = pixmap.scaledToHeight(80)
        return pixmap

    def getColor(self):
        return self.color

    def getPlayer(self):
        return self.player

    def getMoveNumber(self):
        return self.moveNumber

    def nextMove(self):
        self.moveNumber += 1
