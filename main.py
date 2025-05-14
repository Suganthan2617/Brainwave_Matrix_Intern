from db import connect_db
from gui import start_gui

if __name__ == "__main__":
    connect_db()  # Initialize DB
    start_gui()   # Start GUI
