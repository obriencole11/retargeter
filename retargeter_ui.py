from Qt import QtWidgets, QtGui
from Qt.QtCore import Signal, Slot

class RetargeterWindow(QtWidgets.QMainWindow):

    bindClicked = Signal(bool, bool, bool, float)
    bakeClicked = Signal()
    selectNodesClicked = Signal()
    removeClicked = Signal()

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        ### Main ###

        # Set the window title
        self.setWindowTitle('Retargeter')

        # Create the main widget
        mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(mainWidget)

        # Create the mainlayout
        mainLayout = QtWidgets.QVBoxLayout()
        mainWidget.setLayout(mainLayout)


        ### Settings ###

        # Create a group box for the settings
        settingsBox = QtWidgets.QGroupBox('Settings', mainWidget)
        mainLayout.addWidget(settingsBox)

        # Create a form layout for setttings
        settingLayout = QtWidgets.QFormLayout()
        settingsBox.setLayout(settingLayout)

        # Bind translate setting
        self.bindTranslateBox = QtWidgets.QCheckBox(settingsBox)
        self.bindTranslateBox.setChecked(True)
        settingLayout.addRow('Bind Translate', self.bindTranslateBox)

        # Bind rotate setting
        self.bindRotateBox = QtWidgets.QCheckBox(settingsBox)
        self.bindRotateBox.setChecked(True)
        settingLayout.addRow('Bind Rotate', self.bindRotateBox)

        # Snap to target setting
        self.snapBox = QtWidgets.QCheckBox(settingsBox)
        self.snapBox.setChecked(True)
        settingLayout.addRow('Snap to Target', self.snapBox)

        # Node Scale setting
        self.scaleLine = QtWidgets.QLineEdit(settingsBox)
        self.scaleLine.setValidator(QtGui.QDoubleValidator(0, 100, 2, self))
        self.scaleLine.setText('1.0')
        settingLayout.addRow('Node Scale', self.scaleLine)


        ### Buttons ###

        # Bind button
        bindButton = QtWidgets.QPushButton('Bind', mainWidget)
        bindButton.clicked.connect(self.bindTarget)
        mainLayout.addWidget(bindButton)

        # Bake nodes button
        bakeButton = QtWidgets.QPushButton('Bake Bind Targets', mainWidget)
        bakeButton.clicked.connect(self.bakeClicked)
        mainLayout.addWidget(bakeButton)

        # Select nodes button
        selectButton = QtWidgets.QPushButton('Select Bind Nodes', mainWidget)
        selectButton.clicked.connect(self.selectNodesClicked)
        mainLayout.addWidget(selectButton)

        # Remove nodes button
        removeButton = QtWidgets.QPushButton('Remove Selected Nodes', mainWidget)
        removeButton.clicked.connect(self.removeClicked)
        mainLayout.addWidget(removeButton)

    @Slot()
    def bindTarget(self):

        # Emit all settings
        self.bindClicked.emit(self.bindTranslateBox.checkState(),
                              self.bindRotateBox.checkState(),
                              self.snapBox.checkState(),
                              float(self.scaleLine.text()))

window = None

def _testUI():

    # Create a reference to the application
    app = QtWidgets.QApplication([])

    # Create the window and show it
    window = RetargeterWindow()
    window.show()

    # Begin the event loop
    app.exec_()

if __name__ == '__main__':
    _testUI()