from PyQt5 import QtWidgets
from OrderSystem import OrderSystem


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = OrderSystem()
    sys.exit(app.exec_())
