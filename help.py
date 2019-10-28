# Created by HaroldKS at 21/08/2018
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtGui, QtCore
class Circle(QObject):
    ''' Represents a circle defined by the x and y
        coordinates of its center and its radius r. '''
    # Signal emitted when the circle is resized,
    # carrying its integer radius
    resized = pyqtSignal(int)
    # Signal emitted when the circle is moved, carrying
    # the x and y coordinates of its center.
    moved = pyqtSignal(int, int)

    def __init__(self, x, y, r):
        # Initialize the Circle as a QObject so it can emit signals
        QObject.__init__(self)

        # "Hide" the values and expose them via properties
        self._x = x
        self._y = y
        self._r = r

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        # After the center is moved, emit the
        # moved signal with the new coordinates
        self.moved.emit(new_x, self.y)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y):
        self._y = new_y
        # After the center is moved, emit the moved
        # signal with the new coordinates
        self.moved.emit(self.x, new_y)

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, new_r):
        self._r = new_r
        # After the radius is changed, emit the
        # resized signal with the new radius
        self.resized.emit(new_r)




# c = Circle(5, 5, 4)
#
# # Connect the Circle's signals to our simple slots
# c.moved.connect(Damso.on_moved)
# c.resized.connect(Damso.on_resized)
#
# # Move the circle one unit to the right
# c.x += 1
# c.r += 1

i, j = (0, 10)

a, b = 1, 2
a = []
print( not a )