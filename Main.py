from PyQt5 import QtWidgets
from OrderSystem import OrderSystem
import asyncio
import sys
from asyncqt import QEventLoop


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    ui = OrderSystem()
    with loop:
        sys.exit(loop.run_forever())
