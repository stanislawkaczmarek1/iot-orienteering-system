import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.db.models import Base
from desktop_ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    engine = create_engine("sqlite:///backend/db/test.db", echo=False)
    Base.metadata.create_all(engine)

    session = Session(engine)

    window = MainWindow(session)
    window.show()

    exit_code = app.exec()
    
    session.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()