import  sys
from PyQt6 import QtWidgets

from anapencere import Anapencere


app=QtWidgets.QApplication(sys.argv)

main=Anapencere()

sys.exit(app.exec())