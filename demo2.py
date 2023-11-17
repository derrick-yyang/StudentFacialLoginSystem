import sys
import os
import cv2
import mysql.connector
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QTabWidget, QStatusBar, QFileDialog, QFrame, QGridLayout, QDesktopWidget

class MainGUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_UI()
    
    def init_UI(self):
        self.setWindowTitle('New App Title')
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setStyleSheet('''
            QWidget { background-color: #f2f2f2; font-family: Arial; }
            QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; }
            QPushButton:hover { background-color: #45a049; }
            QLineEdit { border: 1px solid #c0c0c0; padding: 5px; }
            QLabel { color: #555; }
            QTabWidget::tab-bar { alignment: center; }
            QStatusBar { background-color: #e0e0e0; }
        ''')

        # Main layout
        mainLayout = QVBoxLayout(self)

        # Tab Widget
        tabWidget = QTabWidget(self)
        cameraTab = QWidget()
        databaseTab = QWidget()
        settingsTab = QWidget()
        tabWidget.addTab(cameraTab, "Camera Control")
        tabWidget.addTab(databaseTab, "Login")
        tabWidget.addTab(settingsTab, "Directory/Query")
        mainLayout.addWidget(tabWidget)

        # Camera Tab Layout
        self.setupCameraTab(cameraTab)

        # Database Tab Layout
        self.setupDatabaseTab(databaseTab)

        # Settings & Info Tab
        self.setupSettingsTab(settingsTab)

        # Status Bar
        self.statusBar = QStatusBar()
        mainLayout.addWidget(self.statusBar)

        self.setLayout(mainLayout)
        self.resize(1100, 600)
        self.moveWindowToCenter()

        # Additional Attributes
        self.flg_conn = False
        self.flg_recd = False
        self.flg_login = False
        self.device = None
        self.videoWriter = None
        self.conn = None

    def setupCameraTab(self, tab):
        layout = QVBoxLayout(tab)

        # Camera Feed
        self.cam_feed = QLabel()
        self.cam_feed.setMinimumSize(640, 480)
        self.cam_feed.setAlignment(Qt.AlignCenter)
        self.cam_feed.setFrameStyle(QFrame.StyledPanel)
        layout.addWidget(self.cam_feed)

        # Connect Device Button
        self.btn_conn = QPushButton('Connect Device')
        self.btn_conn.setFixedHeight(50)
   
        self.btn_conn.clicked.connect(self.connect)
        layout.addWidget(self.btn_conn)
        


    def setupDatabaseTab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)  # Reduce the spacing between widgets
        layout.setContentsMargins(20, 20, 20, 300)  # Set margins (left, top, right, bottom)


        # Database Operations
        self.username = QLineEdit()
        self.username.setPlaceholderText('Enter username')
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText('Enter password')
        layout.addWidget(self.password)

        self.btn_login = QPushButton('Log in')
        self.btn_login.setFixedWidth(200)
        self.btn_login.setFixedHeight(30)

        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)


    def setupSettingsTab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)  # Reduce the spacing between widgets
        layout.setContentsMargins(20, 20, 20, 300)  # Set margins (left, top, right, bottom)

        # Directory and Query
        self.filepath = QLineEdit()
        self.filepath.setPlaceholderText('Select Directory...')
        self.filepath.setReadOnly(True)
        layout.addWidget(self.filepath)

        self.btn_path = QPushButton('Select Directory')
        self.btn_path.setFixedWidth(200)
        self.btn_path.setFixedHeight(30)
        self.btn_path.clicked.connect(self.selectDirectory)
        layout.addWidget(self.btn_path)

        # -- mysql code textbox --
        self.queryCode = QLineEdit()
        self.queryCode.setPlaceholderText('Enter Query')
        layout.addWidget(self.queryCode)
        
        # -- execute code button --
        self.btn_exec = QPushButton('Execute')
        self.btn_exec.setFixedWidth(200)
        self.btn_exec.setFixedHeight(30)
        layout.addWidget(self.btn_exec)
    
    # ~~~~~~~~ window centering ~~~~~~~~
    def moveWindowToCenter(self):
        window_rect = self.frameGeometry()
        screen_cent = QDesktopWidget().availableGeometry().center()
        window_rect.moveCenter(screen_cent)
        self.move(window_rect.topLeft())
        
        return
    
    # ~~~~~~~~ connect device ~~~~~~~~
    def connect(self):
        if self.flg_recd:
            self.record()
        self.flg_conn = not self.flg_conn
        if self.flg_conn:
            self.btn_conn.setStyleSheet(self.btn_conn_style_1)
            self.btn_conn.setText('Disconnect Device')
            if self.device is None:
                self.device = cv2.VideoCapture(0)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.start(50)
        else:
            self.btn_conn.setStyleSheet(self.btn_conn_style_0)
            self.btn_conn.setText('Connect Device')
            if self.device is not None:
                self.device.release()
                self.device = None
            self.cam_feed.clear()
            self.timer.stop()
        
        return

    # ~~~~~~~~ update ~~~~~~~~
    def update(self):
        _, frame = self.device.read()
        Qframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Qframe = QImage(Qframe, Qframe.shape[1], Qframe.shape[0], Qframe.strides[0], QImage.Format_RGB888)
        self.cam_feed.setPixmap(QPixmap.fromImage(Qframe))

        if self.flg_recd and frame is not None and self.videoWriter is not None:
            self.videoWriter.write(frame)

        return

    # ~~~~~~~~ select directory ~~~~~~~~
    def selectDirectory(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if path:
            self.filepath.setText(os.path.normpath(path))

        return
    
    # ~~~~~~~~ record ~~~~~~~~
    def record(self):
        if not self.flg_conn:
            if self.videoWriter is not None:
                self.videoWriter.release()

            return

        self.flg_recd = not self.flg_recd
        
        if self.flg_recd:
            if not self.filename.text():
                self.filename.setText('temp')
            if self.filepath.text() == '':
                self.filepath.setText(os.getcwd())
                
            self.save_path = os.path.join(self.filepath.text(), '%s.avi' % self.filename.text())
            if self.videoWriter is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.videoWriter = cv2.VideoWriter(self.save_path, fourcc, 30.0, (640, 480))

            self.btn_recd.setStyleSheet(self.btn_recd_style_1)
            self.btn_recd.setText('Stop Recording')
        else:
            if self.videoWriter is not None:
                self.videoWriter.release()
                self.videoWriter = None
            self.btn_recd.setStyleSheet(self.btn_recd_style_0)
            self.btn_recd.setText('Start Recording')
            
        return

    # ~~~~~~~~ login ~~~~~~~~
    def login(self):
        self.flg_login = not self.flg_login
        if self.flg_login:
            if not self.username.text():
                self.username.setText('root')
            if self.password.text() == '':
                self.password.setText('1203')

            if self.conn is None:
                self.conn = mysql.connector.connect(host="localhost", port=3306, 
                    user=self.username.text(), passwd=self.password.text())
            self.btn_login.setStyleSheet(self.btn_login_style_1)
            self.btn_login.setText('Log out')
        else:
            if self.conn is not None:
                self.conn = None
            self.btn_login.setStyleSheet(self.btn_login_style_0)
            self.btn_login.setText('Log in')

    # ~~~~~~~~ execute code ~~~~~~~~
    def execQuery(self):
        if not self.flg_login:
            return

        if self.queryCode.text() == '':
            self.queryCode.setText('SHOW TABLES FROM sql_challenge')
        
        mycursor = self.conn.cursor()
        mycursor.execute(self.queryCode.text())
        data = ''
        for line in mycursor.fetchall():
            data += '%s\n' % str(line)
        self.cmd_window.setText(data)

    # ~~~~~~~~ toggle animation ~~~~~~~~
    def toggleAnimation(self):
        self.flg_anim = not self.flg_anim
        if self.flg_anim:
            self.animation.setMovie(self.movie)
            self.movie.start()
        else:
            self.movie.stop()
            self.animation.clear()
        
        return

    # ~~~~~~~~ toggle animation ~~~~~~~~
    def openRepo(self):
        QDesktopServices.openUrl(QUrl('http://localhost:8002'))


    # ... (Add other function implementations here)

# Main Function
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainGUI()
    gui.show()
    sys.exit(app.exec_())
