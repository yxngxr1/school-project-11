import sys
import socket
import time
import threading
import random
from PyQt5.QtWidgets import QFileDialog

from design.design_server import Ui_MainWindow
from PyQt5 import QtWidgets


host = socket.gethostbyname(socket.gethostname())
port = random.randrange(9090, 13000)
print(host, port)

text = ''
clients = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
run = True
lock = threading.Lock()


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        global run
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_ip_port.setText(f'IP: {host}   PORT: {port}')
        self.ui.btn_test_file.clicked.connect(self.load_file)
        self.ui.btn_start.clicked.connect(self.start_test)
        self.ui.btn_stop.clicked.connect(self.stop_test)

    def load_file(self):
        global text
        file = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        try:
            if file[0].split('.')[-1] == 'txt':
                text = open(file[0], 'r', encoding="utf-8").read()
                self.ui.btn_test_file.setText(file[0].split('/')[-1])
                self.ui.btn_test_file.setEnabled(False)
                self.ui.btn_start.setEnabled(True)
        except Exception as e:
            print(e)

    def start_test(self):
        print('start')
        for client in clients:
            s.sendto(b'start' + text.encode(), client)
        self.ui.btn_start.setEnabled(False)
        self.ui.btn_stop.setEnabled(True)

    def stop_test(self):
        print('stop')
        global run
        for client in clients:
            s.sendto(b'stop', client)
        self.ui.btn_start.setEnabled(True)
        self.ui.btn_stop.setEnabled(False)

    def closeEvent(self, event):
        print('STOPPED')
        global run, s
        try:
            for client in clients:
                s.sendto(b'stop', client)
            s.shutdown(socket.SHUT_WR)
            run = False
        except Exception as e:
            print(1, e)


def receive():
    global run, s
    print('server started')
    while run:
        lock.acquire()
        try:
            data, addr = s.recvfrom(1024)
            text = data.decode('utf-8')
            if text == 'join':
                if addr not in clients:
                    clients.append(addr)
                s.sendto(b'join', addr)
            if text == 'leave':
                if addr in clients:
                    del clients[clients.index(addr)]
            if 'result' in text:
                name, text = text.split('\n')[0][6:], '\n'.join(text.split('\n')[1:])
                file = open(f'Результаты теста ({name}).txt', 'a', encoding="utf-8")
                file.write(text)
                file.close()
            ip_port = [f'{client[0]}:{client[1]}' for client in clients]
            users = '\n'.join(ip_port)
            myapp.ui.label_users.setText(users)

            print(data.decode('utf-8'))
        except Exception as e:
            print(e)
            run = False
        finally:
            lock.release()
    print('server stopped')
    s.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    r_t = threading.Thread(target=receive)
    r_t.start()
    sys.exit(app.exec_())
