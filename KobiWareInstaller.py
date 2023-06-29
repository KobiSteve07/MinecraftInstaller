#  _  __     _     ___        __
# | |/ /___ | |__ (_) \      / /_ _ _ __ ___
# | ' // _ \| '_ \| |\ \ /\ / / _\`| '__/ _ \
# | . \ (_) | |_) | | \ V  V / (_| | | |  __/
# |_|\_\___/|_.__/|_|  \_/\_/ \__,_|_|  \___|
# (C) Copyright 2023 KobiWare, LLC.  All Rights Reserved.

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QRadioButton, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QProgressBar
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import sys
import os
import requests
import zipfile
if sys.platform == "win32":
    import winreg
    from win32com.client import Dispatch
    import shutil
import jdk
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class MinecraftSetup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Setup")
        self.setFixedSize(500, 360)
        self.center_window()

        self.step = 0
        self.paid = True
        self.username = ""

        self.title = QLabel("Welcome to the KobiWare Minecraft Client Installer!", parent=self)
        self.title.setGeometry(10, 20, 450, 25)
        self.title.setFont(QFont("Arial", 15))

        self.images = []
        self.images.append(QPixmap("image.jpg").scaled(500, 200))
        self.images.append(QPixmap("image(1).jpg").scaled(500, 200))
        self.images.append(QPixmap("image(2).jpg").scaled(500, 200))

        self.image_label = QLabel(parent=self)
        self.image_label.setGeometry(0, 100, 500, 200)
        self.image_label.setPixmap(self.images[0])  # Set initial pixmap

        self.desc = QLabel(
            "This KobiWare installer will install Minecraft and additional components onto your computer. This will enable you to play on the KobiWare Minecraft server or create singleplayer worlds.\n\n\nTo continue, click Next.",
            parent=self, alignment=Qt.AlignmentFlag.AlignTop)
        self.desc.setGeometry(10, 50, 450, 300)
        self.desc.setFont(QFont("Arial", 10))
        self.desc.setWordWrap(True)

        self.cancel = QPushButton("Cancel", parent=self)
        self.cancel.clicked.connect(self.handle_cancel_click)

        self.next_button = QPushButton("Next >", parent=self)
        self.next_button.clicked.connect(self.handle_next_click)

        self.back = QPushButton("< Back", parent=self)
        self.back.clicked.connect(self.handle_back_click)
        self.back.setDisabled(True)

        self.java = QRadioButton("I have an account", parent=self, checked=True)
        self.java.toggled.connect(lambda: self.btnstate(self.java))
        self.java.hide()

        self.cracked = QRadioButton("I don't have an account", parent=self)
        self.cracked.toggled.connect(lambda: self.btnstate(self.cracked))
        self.cracked.hide()

        self.username = QLineEdit(parent=self)
        self.username.setGeometry(10, 150, 200, 30)
        self.username.setDisabled(True)
        self.username.textChanged.connect(self.handle_text_edit)
        self.username.hide()

        self.takenText = QLabel("", parent=self)
        self.takenText.setGeometry(10, 180, 200, 30)
        self.takenText.hide()
        
        self.progress = QProgressBar(parent=self)
        self.progress.setFormat("Preparing to install...")
        self.progress.hide()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.back)
        self.buttons_layout.addWidget(self.cancel)
        self.buttons_layout.addWidget(self.next_button)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.desc)
        self.main_layout.addWidget(self.java)
        self.main_layout.addWidget(self.cracked)
        self.main_layout.addWidget(self.username)
        self.main_layout.addWidget(self.takenText)
        self.main_layout.addWidget(self.progress)
        self.main_layout.addLayout(self.buttons_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def center_window(self):
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def handle_text_edit(self):
        username = self.username.text()
        if not(username):
            self.takenText.setText("Enter a username.")
            self.next_button.setDisabled(True)
        elif len(username) > 16:
            self.takenText.setText("Username is too long.")
            self.next_button.setDisabled(True)
        elif len(username) < 3:
            self.takenText.setText("Username is too short.")
            self.next_button.setDisabled(True)
        elif any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_" for char in username):
            self.takenText.setText("Username contains invalid characters.")
            self.next_button.setDisabled(True)
        elif requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?"):
            self.takenText.setText("Username taken")
            self.next_button.setDisabled(True)
        else:
            self.takenText.setText("Username available")
            self.next_button.setDisabled(False)

    def handle_cancel_click(self):
        sys.exit()

    def handle_next_click(self):
        if self.step == 2:
            self.handle_cancel_click()
        else:
            self.step += 1
            self.step_change()

    def handle_back_click(self):
        self.step -= 1
        self.step_change()

    def step_change(self):
        if self.step == 0:
            self.back.setDisabled(True)
            self.desc.setText("This KobiWare installer will install Minecraft and additional components, some optional, onto your computer. This will enable you to play on the KobiWare Minecraft server or create singleplayer worlds.\n\n\nTo continue, click Next.")
            self.title.setText("Welcome to the KobiWare Minecraft Client Installer!")
            self.java.hide()
            self.cracked.hide()
            self.image_label.setPixmap(self.images[0])
            self.username.hide()
            self.takenText.hide()
        else:
            self.back.setDisabled(False)
            if self.step == 1:
                self.title.setText("Account type")
                self.desc.setText("If you have a preexisting Java account, you can set it up after the installation. If you don't, you will need to create a username in the box below.")
                self.java.show()
                self.cracked.show()
                self.image_label.setPixmap(self.images[1])
                self.username.show()
                self.takenText.show()

            else:
                if self.step == 2:
                    self.back.hide()
                    self.next_button.setText("Finish")
                    self.next_button.setDisabled(True)
                    self.image_label.setPixmap(self.images[2])
                    self.title.setText("Install")
                    self.desc.setText("Preparing to install...")
                    self.username.hide()
                    self.java.hide()
                    self.cracked.hide()
                    self.takenText.hide()
                    self.progress.show()
                    
                    if self.paid == True:
                        with zipfile.ZipFile("mmc-develop-win32.zip") as zf:
                            filesList = zf.namelist()
                            for idx, file in enumerate(filesList):
                                percent = round((idx / len(filesList))*100)
                                self.progress.setFormat("Installing Launcher... %d%%" % percent)
                                self.progress.setValue(percent)
                                zf.extract(file, "MultiMC")
                            self.progress.setFormat("Extracted Minecraft Launcher")
                            self.progress.setValue(100)
                    elif self.paid == False:
                        with zipfile.ZipFile("mmc-cracked-win32.zip") as zf:
                            filesList = zf.namelist()
                            for idx, file in enumerate(filesList):
                                percent = round((idx / len(filesList))*100)
                                self.progress.setFormat("Installing Launcher... %d%%" % percent)
                                self.progress.setValue(percent)
                                zf.extract(file, "UltimMC")
                            self.progress.setFormat("Extracted Minecraft Launcher")
                            self.progress.setValue(100)
                        
                    self.progress.setFormat("Installing Java dependencies...")
                    self.progress.setValue(0)
                    jdk.install('17')
                    self.progress.setFormat("Installed java dependencies")
                    self.progress.setValue(100)
                    
                    if sys.platform == "win32":
                        self.progress.setFormat("Installing launcher...")
                        self.progress.setValue(0)
                        if(self.paid):
                            shutil.move("./MultiMC", "C:/Windows/tracing/KobiWare")
                            path = os.path.join(os.path.expanduser("~"), "desktop", "MultiMC.lnk")
                            target = "C:/Windows/tracing/KobiWare/MultiMC/MultiMC.exe"
                            wDir = "C:/Windows/tracing/KobiWare/MultiMC"
                            icon = "C:/Windows/tracing/KobiWare/MultiMC/MultiMC.exe"
                            shell = Dispatch('WScript.Shell')
                        else:
                            shutil.move("./UltimMC", "C:/Windows/tracing/KobiWare")
                            path = os.path.join(os.path.expanduser("~"), "desktop", "UltimMC.lnk")
                            target = "C:/Windows/tracing/KobiWare/UltimMC/UltimMC.exe"
                            wDir = "C:/Windows/tracing/KobiWare/UltimMC"
                            icon = "C:/Windows/tracing/KobiWare/UltimMC/UltimMC.exe"
                            shell = Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(path)
                        shortcut.Targetpath = target
                        shortcut.WorkingDirectory = wDir
                        shortcut.IconLocation = icon
                        shortcut.save()
                        os.system(r'cmd /c "icacls C:\windows\tracing\KobiWare /grant Users:(OI)(CI)(F) /T"')
                        self.progress.setFormat("Launcher installed")
                        self.progress.setValue(100)
                        
                        ### DO NOT TOUCH, YOUR REGISTRY WILL EXPLODE ###
                        self.progress.setFormat("Editing your registry...")
                        self.progress.setValue(0)
                        # Specify the new value you want to set for the PATH variable
                        new_path_value = '%USERPROFILE%\\.jdk\\jdk-17.0.7+7\\bin'

                        # Open the registry key for the current user environment variables
                        key = winreg.OpenKey(
                            winreg.HKEY_CURRENT_USER,
                            r'Environment',
                            0,
                            winreg.KEY_ALL_ACCESS
                        )

                        # Get the current value of the PATH variable
                        current_path_value, _ = winreg.QueryValueEx(key, 'PATH')

                        # Check if the new value is already present in the PATH
                        if new_path_value not in current_path_value:
                            # Append the new value to the current PATH
                            new_path_value = current_path_value + ';' + new_path_value

                            # Set the updated value for the PATH variable
                            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path_value)

                        # Close the registry key
                        winreg.CloseKey(key)
                        self.progress.setFormat("Registry edited")
                        self.progress.setValue(100)
                    
                    self.progress.setFormat("Installation complete")
                    self.next_button.setDisabled(False)

    def btnstate(self, button):
        if button.text() == "I have an account":
            if button.isChecked():
                self.paid = True
                self.takenText.setText("")
                self.next_button.setDisabled(False)

        if button.text() == "I don't have an account":
            if button.isChecked():
                self.paid = False
                self.handle_text_edit()
        self.username.setDisabled(self.paid)


app = QApplication([])
window1 = MinecraftSetup()
app.exec()