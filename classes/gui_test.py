import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QtGui.QDialog):
    def __init__(self, x_data, y_data, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

#         #Just some button connected to `plot` method
#         self.button = QtGui.QPushButton('Plot')
#         self.button.clicked.connect(self.plot)

        self.plot(x_data, y_data)


        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
#         layout.addWidget(self.button)
        self.setLayout(layout)



    def plot(self, x_data, y_data):

        # create an axis
#         ax = self.figure.add_subplot(111)
        ax = plt.subplot()

        # discards the old graph
        ax.hold(False)
        
        # plot a bar chart
        ax.bar(x_data, y_data)
        

        # refresh canvas
        self.canvas.draw()

