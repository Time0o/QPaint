#!/usr/bin/env python3

from sys import argv, exit
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets


class DrawAreaView(QtWidgets.QGraphicsView):
    ZOOM_FACTOR = 1.25

    def __init__(self):
        super().__init__()

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event: QtGui.QWheelEvent):
        if not event.modifiers() & QtCore.Qt.ControlModifier:
           return

        delta = event.angleDelta().y()

        if delta > 0:
            zoomFactor = self.ZOOM_FACTOR
        else:
            zoomFactor = 1. / self.ZOOM_FACTOR

        self.scale(zoomFactor, zoomFactor)


class ToolsDockWidget(QtWidgets.QDockWidget):
    class Tool:
        def __init__(self,
                     name: str,
                     icon: str,
                     shortcut: str = None,
                     helptext: str = None):

            self._name = name

            self._icon = QtGui.QIcon(icon)

            self._shortcut = QtGui.QKeySequence(shortcut) if shortcut else None

            self._toolTip = self._name

            if shortcut is not None:
                self._toolTip += '\nShortcut key: ' + self._shortcut.toString()

            if helptext is not None:
                self._toolTip += '\n\n' + helptext

        def name(self) -> str:
            return self._name

        def icon(self) -> QtGui.QIcon:
            return self._icon

        def shortcut(self) -> Optional[QtGui.QKeySequence]:
            return self._shortcut

        def toolTip(self) -> str:
            return self._toolTip

    class ToolButtonAreaWidget(QtWidgets.QWidget):
        BUTTON_SIZE = QtCore.QSize(30, 30)

        def __init__(self):
            super().__init__()

            self._layout = QtWidgets.QVBoxLayout()
            self._layout.setAlignment(QtCore.Qt.AlignTop)
            self.setLayout(self._layout)

        def addTool(self, tool):
            toolButton = QtWidgets.QToolButton()
            toolButton.setText('X')  # TODO
            #toolButton.setIcon(tool.icon())
            toolButton.setToolTip(tool.toolTip())
            toolButton.setFixedSize(self.BUTTON_SIZE)
            self._layout.addWidget(toolButton)

    WINDOW_TITLE = 'Tools'

    AVAILABLE_TOOLS = {
        'brush': Tool('Paintbrush', '', 'B', 'Left click to draw.'),
        'eraser': Tool('Eraser', '', 'E', 'Left click to erase.'),
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        self._toolButtonAreaWidget = self.ToolButtonAreaWidget()
        self.setWidget(self._toolButtonAreaWidget)

        for tool in self.AVAILABLE_TOOLS.values():
            self._toolButtonAreaWidget.addTool(tool)


class PaletteDockWidget(QtWidgets.QDockWidget):
    class ColorGridWidget(QtWidgets.QWidget):
        CELL_WIDTH = 20
        CELL_HEIGHT = 20

        DEFAULT_COLORS = [
            ['#FFFFFF', '#000000'],
            ['#808080', '#404040']
        ]

        def __init__(self):
            super().__init__()

            self._layout = QtWidgets.QGridLayout()
            self._layout.setAlignment(QtCore.Qt.AlignTop)
            self._layout.setSpacing(0)
            self.setLayout(self._layout)

            for r, row in enumerate(self.DEFAULT_COLORS):
                for c, color in enumerate(row):
                    colorCell = QtWidgets.QPushButton()

                    style = 'background-color: {}; border: 0px;'.format(color)
                    colorCell.setStyleSheet(style)

                    colorCell.setFixedSize(self.CELL_WIDTH, self.CELL_HEIGHT)

                    self._layout.addWidget(colorCell, r, c)

    WINDOW_TITLE = 'Palette'

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)

        self._colorGridWidget = self.ColorGridWidget()
        self.setWidget(self._colorGridWidget)


class EditorWindow(QtWidgets.QMainWindow):
    def __init__(self, loadImage: str = None):
        super().__init__()

        self._drawAreaView = DrawAreaView()
        self.setCentralWidget(self._drawAreaView)

        self._drawAreaScene = QtWidgets.QGraphicsScene()
        self._drawAreaView.setScene(self._drawAreaScene)

        self._toolsDockWidget = ToolsDockWidget()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._toolsDockWidget)

        self._paletteDockWidget = PaletteDockWidget()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._paletteDockWidget)

        if loadImage is not None:
            pixmap = QtGui.QPixmap(loadImage)
            self._drawAreaScene.addPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)

    editorWindow = EditorWindow('test/images/lenna.png')
    editorWindow.show()
    exit(app.exec())
