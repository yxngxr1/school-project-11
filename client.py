import sys
import socket
import time
from threading import Thread

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap

from design.design_client import Ui_MainWindow
from PyQt5 import QtWidgets


host, port = socket.gethostbyname(socket.gethostname()), 0
shutdown = False
join = False
test_ended = False
server = ('127.0.0.1', 9090)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = ''
        self.file_text = ''
        self.number = 0
        self.name = ''
        self.i = 1
        self.result = ''

        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_start.clicked.connect(self.load)
        self.ui.btn_connect.clicked.connect(self.connect)
        self.ui.btn_send_res.clicked.connect(self.send_res)

    def connect(self):
        global join, s, server
        ip = self.ui.input_ip.text()
        port = self.ui.input_port.text()
        try:
            server = (ip, int(port))
            if not join:
                s.sendto(b"join", server)
            return
        except Exception as e:
            print(e)
            self.ui.label_connect_status.setText('Не удалось подключиться')

    def send_res(self):
        global join, server, shutdown
        try:
            res = b'result' + self.result.encode('utf-8')
            s.sendto(res, server)
        except Exception as e:
            print(e)
            print('Блять')
        time.sleep(1)
        s.sendto(b"leave", server)
        shutdown = True

        t_r.join()
        s.close()
        self.close()

    def next(self):
        self.file = open('Результаты теста.txt', 'a', encoding="utf-8")
        if self.ui.radioButton_1.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[3 + 5 * (self.i - 1)].split('&')[1] + '\n')
            self.result += str(self.i) + ') ' + self.file_text[3 + 5 * (self.i - 1)].split('&')[1] + '\n'
        elif self.ui.radioButton_2.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[4 + 5 * (self.i - 1)].split('&')[1] + '\n')
            self.result += str(self.i) + ') ' + self.file_text[4 + 5 * (self.i - 1)].split('&')[1] + '\n'
        elif self.ui.radioButton_3.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[5 + 5 * (self.i - 1)].split('&')[1] + '\n')
            self.result += str(self.i) + ') ' + self.file_text[5 + 5 * (self.i - 1)].split('&')[1] + '\n'
        elif self.ui.radioButton_4.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[6 + 5 * (self.i - 1)].split('&')[1] + '\n')
            self.result += str(self.i) + ') ' + self.file_text[6 + 5 * (self.i - 1)].split('&')[1] + '\n'
        self.file.close()
        self.i += 1
        self.ui.label_page.setText(str(self.i) + ' из ' + str(self.number))
        if self.i <= self.number:
            self.ui.label_question.setText(self.file_text[2 + 5 * (self.i - 1)].split('&')[0])
            self.ui.label_image.setPixmap(QPixmap(1, 0))
            if len(self.file_text[2 + 5 * (self.i - 1)].split('&')) > 1:
                pixmap = QPixmap(self.file_text[2 + 5 * (self.i - 1)].split('&')[1])
                pixmap = pixmap.scaled(self.width(), 200, Qt.KeepAspectRatio)
                self.ui.label_image.setPixmap(QPixmap(pixmap))
            self.ui.radioButton_1.setText(self.file_text[3 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_2.setText(self.file_text[4 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_3.setText(self.file_text[5 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_4.setText(self.file_text[6 + 5 * (self.i - 1)].split('&')[0])
        else:
            self.ui.btn_next.setEnabled(False)
            self.ui.btn_send_res.setEnabled(True)
            self.ui.radioButton_1.setEnabled(False)
            self.ui.radioButton_2.setEnabled(False)
            self.ui.radioButton_3.setEnabled(False)
            self.ui.radioButton_4.setEnabled(False)

    def load(self):
        if self.ui.input_name.text() != '' and self.file_text != '':
            self.file = open('Результаты теста.txt', 'a', encoding="utf-8")
            self.file.write(self.ui.input_name.text() + '\n')
            self.result += self.ui.input_name.text() + '\n'
            self.file.close()

            self.ui.btn_next.setEnabled(True)
            self.ui.radioButton_1.setEnabled(True)
            self.ui.radioButton_2.setEnabled(True)
            self.ui.radioButton_3.setEnabled(True)
            self.ui.radioButton_4.setEnabled(True)
            self.ui.label_test_name.setEnabled(True)
            self.ui.label_question.setEnabled(True)
            self.ui.input_name.setEnabled(False)
            self.ui.label_name.setEnabled(False)
            self.ui.btn_start.setEnabled(False)
            self.ui.btn_connect.setEnabled(False)

            self.ui.label_test_name.setText(self.file_text[0])
            self.number = int(self.file_text[1])
            self.ui.label_page.setText(str(self.i) + ' из ' + str(self.number))

            # set first position
            self.ui.label_question.setText(self.file_text[2].split('&')[0])
            if len(self.file_text[2].split('&')) > 1:
                pixmap = QPixmap(self.file_text[2].split('&')[1])
                pixmap = pixmap.scaled(self.width(), 200, Qt.KeepAspectRatio)
                self.ui.label_image.setPixmap(pixmap)

            self.ui.radioButton_1.setText(self.file_text[3].split('&')[0])
            self.ui.radioButton_2.setText(self.file_text[4].split('&')[0])
            self.ui.radioButton_3.setText(self.file_text[5].split('&')[0])
            self.ui.radioButton_4.setText(self.file_text[6].split('&')[0])

    def closeEvent(self, event):
        global shutdown
        try:
            s.sendto(b'leave', server)
        except Exception as e:
            print(e)
        shutdown = True
        exit()


def receive():
    global join, text
    while not shutdown:
        try:
            data, addr = s.recvfrom(10240)
            text = data.decode('utf-8')
            if text[:5] == 'start':
                myapp.file_text = text[5:].split('\n')
                myapp.ui.label_test_name.setText(myapp.file_text[0])
            if text == 'stop':
                print('stop')
            if text == 'join':
                join = True
                myapp.ui.label_connect_status.setText('Подключен к серверу')
        except:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    t_r = Thread(target=receive)
    t_r.start()
    sys.exit(app.exec_())
