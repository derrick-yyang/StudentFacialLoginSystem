# -*- coding: utf-8 -*-

import os
import sys
import cv2
import mysql.connector

from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from PyQt5.QtGui import QIcon, QImage, QMovie, QPixmap, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QWidget
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog


# MainGUI class
class MainGUI(QWidget):
    
    # ~~~~~~~~ constructor ~~~~~~~~
    def __init__(self):
        super().__init__()
        self.init_UI()
        
        return
    
    # ~~~~~~~~ initialize ui ~~~~~~~~
    def init_UI(self):
        # set properties
        self.setStyleSheet('QWidget {background-color: #ffffff;}')
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.setWindowTitle('App Title')
        
        # create widgets
        # -- connect device button --
        # -- used to connect camera
        self.btn_conn = QPushButton('Connect Device')
        self.btn_conn.setMinimumHeight(40)
        self.btn_conn_style_0 = 'QPushButton {background-color: #00a86c; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        self.btn_conn_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 16px;}'
        self.btn_conn.setStyleSheet(self.btn_conn_style_0)
        
        # -- select directory textbox --
        # -- display the selected save dir
        self.filepath = QLineEdit()
        self.filepath.setMinimumSize(250, 30)
        self.filepath.setReadOnly(True)
        self.filepath.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.filepath.setPlaceholderText(os.getcwd())
        
        # -- select directory button --
        # -- select dir by file explorer
        self.btn_path = QPushButton('Select Directory')
        self.btn_path.setMinimumSize(150, 30)
        self.btn_path_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_path_style_1 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_path.setStyleSheet(self.btn_path_style_0)
        
        # -- control recording textbox --
        # -- this program has a record func and this specify the filename of recorded video
        self.filename = QLineEdit()
        self.filename.setMinimumSize(250, 30)
        self.filename.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.filename.setPlaceholderText('Enter filename...')
        
        # -- control recording button --
        self.btn_recd = QPushButton('Start Recording')
        self.btn_recd.setMinimumSize(150, 30)
        self.btn_recd_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_recd_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_recd.setStyleSheet(self.btn_recd_style_0)

        # -- login username textbox --
        self.username = QLineEdit()
        self.username.setMinimumSize(150, 30)
        self.username.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.username.setPlaceholderText('Enter username')

        # -- login password textbox --
        self.password = QLineEdit()
        self.password.setMinimumSize(150, 30)
        self.password.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.password.setPlaceholderText('Enter password')
        
        # -- control recording button --
        self.btn_login = QPushButton('Log in')
        self.btn_login.setMinimumSize(100, 30)
        self.btn_login_style_0 = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_login_style_1 = 'QPushButton {background-color: #ff6464; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_login.setStyleSheet(self.btn_login_style_0)

        # -- mysql code textbox --
        self.queryCode = QLineEdit()
        self.queryCode.setMinimumSize(300, 30)
        self.queryCode.setStyleSheet('QLineEdit {border: 1px solid #c8c8c8; font-family: ubuntu, arial; font-size: 14px;}')
        self.queryCode.setPlaceholderText('Enter query')
        
        # -- execute code button --
        self.btn_exec = QPushButton('Execute')
        self.btn_exec.setMinimumSize(100, 30)
        self.btn_exec_style = 'QPushButton {background-color: #64a0ff; border: none; color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}'
        self.btn_exec.setStyleSheet(self.btn_exec_style)

        # -- possible label --
        # -- except button and textbox, we can also use label in gui
        # -- label can be filled with text, animation, image and so on
        # -- camera feed --
        self.cam_feed = QLabel()
        self.cam_feed.setMinimumSize(640, 480)
        self.cam_feed.setAlignment(Qt.AlignCenter)
        self.cam_feed.setFrameStyle(QFrame.StyledPanel)
        self.cam_feed.setStyleSheet('QLabel {background-color: #000000;}')

        # -- cmd window --
        self.cmd_window = QLabel()
        self.cmd_window.setMinimumWidth(300)
        self.cmd_window.setFrameStyle(QFrame.StyledPanel)
        self.cmd_window.setStyleSheet('QLabel {background-color: #000000; color: #ffffff;}')
        
        # -- animation --
        self.movie = QMovie('assets/anim.gif')
        self.animation = QLabel()
        self.animation.setMinimumWidth(300)
        self.animation.setAlignment(Qt.AlignCenter)
        self.animation.setStyleSheet('QLabel {background-color: #ffffff;}')
        self.animation.setMovie(self.movie)
        self.movie.start()
        
        # -- control animation button --
        self.btn_anim = QPushButton()
        self.btn_anim.setFixedSize(20, 20)
        self.btn_anim.setStyleSheet('QPushButton {background-color: none; border: none;}')
        self.btn_anim.setIcon(QIcon('assets/button_anim.png'))
        self.btn_anim.setIconSize(QSize(20, 20))
        self.btn_anim.setToolTip('Toggle animation')
        
        # -- button --
        self.btn_repo = QPushButton()
        self.btn_repo.setFixedSize(20, 20)
        self.btn_repo.setStyleSheet('QPushButton {background-color: none; border: none;}')
        self.btn_repo.setIcon(QIcon('assets/button_repo.png'))
        self.btn_repo.setIconSize(QSize(20, 20))
        
        # -- copyright --
        self.copyright = QLabel('\u00A9 HKU COMP3278A 2023')
        self.copyright.setFixedHeight(20)
        self.copyright.setAlignment(Qt.AlignCenter)
        self.copyright.setStyleSheet('QLabel {background-color: #ffffff; font-family: ubuntu, arial; font-size: 14px;}')
        
        # create layouts
        # create some horizontal box
        h_box_conn = QHBoxLayout()
        h_box_conn.addWidget(self.btn_conn)
        
        h_box_path = QHBoxLayout()
        h_box_path.addWidget(self.filepath)
        h_box_path.addWidget(self.btn_path)
        
        h_box_recd = QHBoxLayout()
        h_box_recd.addWidget(self.filename)
        h_box_recd.addWidget(self.btn_recd)

        h_box_login = QHBoxLayout()
        h_box_login.addWidget(self.username)
        h_box_login.addWidget(self.password)
        h_box_login.addWidget(self.btn_login)

        h_box_exec = QHBoxLayout()
        h_box_exec.addWidget(self.queryCode)
        h_box_exec.addWidget(self.btn_exec)

        h_box_cmd = QHBoxLayout()
        h_box_cmd.addWidget(self.cmd_window)
        
        h_box_anim = QHBoxLayout()
        h_box_anim.addWidget(self.animation)
        
        h_box_copyright = QHBoxLayout()
        h_box_copyright.addWidget(self.btn_anim)
        h_box_copyright.addWidget(self.copyright)
        h_box_copyright.addWidget(self.btn_repo)
        
        # create vertical box
        # arrange horizontal boxes vertically
        v_box1 = QVBoxLayout()
        v_box1.addLayout(h_box_conn)
        v_box1.addLayout(h_box_path)
        v_box1.addLayout(h_box_recd)
        v_box1.addLayout(h_box_login)
        v_box1.addLayout(h_box_exec)
        v_box1.addStretch()
        v_box1.addLayout(h_box_cmd)
        v_box1.addLayout(h_box_anim)
        v_box1.addLayout(h_box_copyright)
        
        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.cam_feed)
        
        # create grid with boxes created
        g_box0 = QGridLayout()
        g_box0.addLayout(v_box1, 0, 0, -1, 2)
        g_box0.addLayout(v_box2, 0, 2, -1, 4)
        
        self.setLayout(g_box0)

        # set slots for signals
        self.flg_conn = False
        self.flg_recd = False
        self.flg_plot = False
        self.flg_login = False
        self.flg_anim = True
        self.device = None
        self.videoWriter = None
        self.conn = None
        
        # connect buttons with functions
        self.btn_conn.clicked.connect(self.connect)
        self.btn_path.clicked.connect(self.selectDirectory)
        self.btn_recd.clicked.connect(self.record)
        self.btn_login.clicked.connect(self.login)
        self.btn_exec.clicked.connect(self.execQuery)
        self.btn_anim.clicked.connect(self.toggleAnimation)
        self.btn_repo.clicked.connect(self.openRepo)
        
        return
    
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


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = MainGUI()
    gui.show()
    gui.moveWindowToCenter()
    gui.setFixedSize(1100, 600)
    sys.exit(app.exec_())
