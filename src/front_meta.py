import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QGridLayout, QWidget, QPushButton



WINDOW_TITLES = [
    "My App",
    "Generative AI Assistant",
    "Post Session Helper",
]



# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(800, 600))
        self.STATES = ["main_menu", "generate", "session_helper"]
        self.cur_state = "main_menu"
        self.MENU_STATE(self.cur_state)

    def MENU_STATE(self, state):
        self.setWindowTitle(WINDOW_TITLES[self.STATES.index(state)])
        if state == self.STATES[0]:
            self.MAIN_MENU()
        elif state == self.STATES[1]:
            self.GEN_MENU()
        elif state == self.STATES[2]:
            self.SESSION_HELPER_MENU()



    def MAIN_MENU(self):
        # Clear the screen if needed
        if self.centralWidget():
            for widget in self.centralWidget().children():
                widget.deleteLater()

        self.GenButton = QPushButton("Generate")
        self.SHButton = QPushButton("Session Helper")

        self.GenButton.clicked.connect(lambda: self.MENU_STATE("generate"))
        self.SHButton.clicked.connect(lambda: self.MENU_STATE("session_helper"))

        layout = QGridLayout()
        layout.addWidget(self.GenButton, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.SHButton, 0, 1, Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


        

    def GEN_MENU(self):
        # Clear the screen
        if self.centralWidget():
            for widget in self.centralWidget().children():
                widget.deleteLater()
        
        layout = QGridLayout()


        label = QLabel("Generate Menu")
        layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        ###########################################################




        ############################################################

        backButton = QPushButton("Back to Main Menu")
        backButton.clicked.connect(lambda: self.MENU_STATE("main_menu"))
        layout.addWidget(backButton, 3, 0, Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def SESSION_HELPER_MENU(self):
        # Clear the screen
        if self.centralWidget():
            for widget in self.centralWidget().children():
                widget.deleteLater()

        layout = QGridLayout()
        
        label = QLabel("Session Helper Menu")
        layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        ###########################################################



        ###########################################################

        backButton = QPushButton("Back to Main Menu")
        backButton.clicked.connect(lambda: self.MENU_STATE("main_menu"))
        layout.addWidget(backButton, 3, 0, Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()