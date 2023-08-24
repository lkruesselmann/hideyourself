import sys
import subprocess
import os
import random
import string
import time
from stem import Signal
from stem.control import Controller
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt


class HideYourself(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(generate_random_string(20))
        self.setGeometry(100, 100, 400, 100)

        # Tor Proxy Section
        self.tor_group = QGroupBox('Tor Proxy', self)
        self.tor_group.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel('Tor proxy is off', self)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.toggle_button = QPushButton('Toggle Tor Proxy', self)
        self.toggle_button.clicked.connect(self.toggleTorProxy)
        self.toggle_button.setFocusPolicy(Qt.NoFocus)
        
        self.new_server_button = QPushButton('Get New Relay', self)
        self.new_server_button.clicked.connect(self.getNewTorServer)
        self.new_server_button.setFocusPolicy(Qt.NoFocus)

        tor_layout = QVBoxLayout()
        tor_layout.addWidget(self.status_label)
        tor_layout.addWidget(self.toggle_button)
        tor_layout.addWidget(self.new_server_button)
        self.tor_group.setLayout(tor_layout)

        # MAC Address Section
        self.mac_group = QGroupBox('MAC Address', self)
        self.mac_group.setAlignment(Qt.AlignCenter)

        self.mac_label = QLabel(self.getCurrentMAC(), self)  # Initialize with current MAC
        self.mac_label.setAlignment(Qt.AlignCenter)

        self.mac_button = QPushButton('Spoof MAC', self)
        self.mac_button.clicked.connect(self.spoofMAC)
        self.mac_button.setFocusPolicy(Qt.NoFocus)

        self.reset_mac_button = QPushButton('Reset MAC', self)
        self.reset_mac_button.clicked.connect(self.resetMAC)
        self.reset_mac_button.setFocusPolicy(Qt.NoFocus)

        mac_layout = QVBoxLayout()
        mac_layout.addWidget(self.mac_label)
        mac_layout.addWidget(self.mac_button)
        mac_layout.addWidget(self.reset_mac_button)
        self.mac_group.setLayout(mac_layout)

        # Computer Name Section
        self.name_group = QGroupBox('Computer Name', self)
        self.name_group.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(self.getCurrentName(), self)  # Initialize with current name
        self.name_label.setAlignment(Qt.AlignCenter)

        self.name_button = QPushButton('Spoof Name', self)
        self.name_button.clicked.connect(self.spoofName)
        self.name_button.setFocusPolicy(Qt.NoFocus)

        self.reset_name_button = QPushButton('Reset Name', self)
        self.reset_name_button.clicked.connect(self.resetName)
        self.reset_name_button.setFocusPolicy(Qt.NoFocus)

        name_layout = QVBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_button)
        name_layout.addWidget(self.reset_name_button)
        self.name_group.setLayout(name_layout)

        # Main Layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tor_group)
        main_layout.addWidget(self.mac_group)
        main_layout.addWidget(self.name_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def toggleTorProxy(self):
        current_status = self.status_label.text()
        if 'on' in current_status:
            self.disableTorProxy()
        else:
            self.enableTorProxy()

    def enableTorProxy(self):
        try:
            subprocess.run(['sudo', 'networksetup', '-setwebproxy', 'Wi-Fi', '127.0.0.1', '9150', 'off'])
            subprocess.run(['sudo', 'networksetup', '-setsecurewebproxy', 'Wi-Fi', '127.0.0.1', '9150', 'off'])
            subprocess.run(['sudo', 'networksetup', '-setsocksfirewallproxy', 'Wi-Fi', '127.0.0.1', '9050', 'off'])
            subprocess.run(['sudo', 'networksetup', '-setsocksfirewallproxystate', 'Wi-Fi', 'on'])
            self.status_label.setText('Tor proxy is on')
        except Exception as e:
            print(f"An error occurred: {e}")

    def disableTorProxy(self):
        try:
            subprocess.run(['sudo', 'networksetup', '-setwebproxystate', 'Wi-Fi', 'off'])
            subprocess.run(['sudo', 'networksetup', '-setsecurewebproxystate', 'Wi-Fi', 'off'])
            subprocess.run(['sudo', 'networksetup', '-setsocksfirewallproxystate', 'Wi-Fi', 'off'])
            self.status_label.setText('Tor proxy is off')
        except Exception as e:
            print(f"An error occurred: {e}")

    def spoofName(self):
        new_name = generate_random_string(10)
        change_computer_name(new_name)
        self.name_label.setText(f'{new_name}')

    def resetName(self):
        change_computer_name("void")
        self.name_label.setText(f'{self.getCurrentName()}')

    def spoofMAC(self):
        spoof_mac_address(randomize=True)
        self.mac_label.setText(f'{self.getCurrentMAC()}')
        self.restartWifi()

    def resetMAC(self):
        spoof_mac_address(randomize=False)
        self.mac_label.setText(f'{self.getCurrentMAC()}')
        self.restartWifi()

    def getCurrentName(self):
        return os.uname()[1]

    def getCurrentMAC(self):
        try:
            output = subprocess.check_output(['ifconfig', 'en0']).decode()
            mac_index = output.find('ether ') + 6
            mac_address = output[mac_index:mac_index + 17]
            return mac_address
        except Exception as e:
            return 'Unknown'
    
    def restartWifi(self):
        try:
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'off'])
            time.sleep(2)  # Wait for 2 seconds
            subprocess.run(['networksetup', '-setairportpower', 'en0', 'on'])
        except Exception as e:
            print(f"Error restarting Wi-Fi: {e}")
    
    def getNewTorServer(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()

                # Send a signal to request a new identity (a new Tor circuit)
                controller.signal(Signal.NEWNYM)
        except Exception as e:
            print(f"An error occurred while getting a new Tor server: {e}")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def change_computer_name(new_name):
    try:
        os.system(f'sudo scutil --set ComputerName {new_name}')
        os.system(f'sudo scutil --set HostName {new_name}')
        os.system(f'sudo scutil --set LocalHostName {new_name}')
    except Exception as e:
        print(f"Error: {e}")

def spoof_mac_address(randomize=True):
    try:
        if randomize:
            os.system('sudo spoof-mac randomize en0') 
            print("MAC randomized")
        else:
            os.system('sudo spoof-mac reset en0') 
            print("MAC reset to original")
    except Exception as e:
        print(f"Error: {e}")

def main():
    app = QApplication(sys.argv)
    window = HideYourself()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()