import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from desktop_ui.main_window import MainWindow



def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    exit_code = app.exec()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()