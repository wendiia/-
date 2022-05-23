from OrderSystem import *

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = OrderSystem(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
