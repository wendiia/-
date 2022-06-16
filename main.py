from PyQt5 import QtWidgets, QtGui
from OrderSystem import OrderSystem


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # QtGui.QFontDatabase.addApplicationFont('./GuiApp/Fonts/Microsoft_YaHei_UI_Light.ttc')
    # QtGui.QFontDatabase.addApplicationFont('./GuiApp/Fonts/Rozovii_Chulok.ttf')
    # QtGui.QFontDatabase.addApplicationFont('./GuiApp/Fonts/Segoe_Script.ttf')
    ui = OrderSystem()
    sys.exit(app.exec_())
