import retargeter
import retargeter_ui as ui
from Qt import QtWidgets

window = None

def show():

    global window

    if window is None:

        # Grab the maya application and the main maya window
        app = QtWidgets.QApplication.instance()
        mayaWindow = {o.objectName(): o for o in app.topLevelWidgets()}["MayaWindow"]

        # Create the window
        window = ui.RetargeterWindow(mayaWindow)

        # Connect window signals
        window.bindClicked.connect(retargeter.bindSelected)
        window.bakeClicked.connect(retargeter.bakeBindTargets)

        window.show()