import sys
from windows import *
from PyQt5 import QtWidgets


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.name = ''
        self.file = ''
        self.file_text = ''
        self.number = 0
        self.i = 1
        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.next)
        self.ui.pushButton_2.clicked.connect(self.load)

    # при нажатии на кнопку
    def next(self):
        self.file = open('Результаты теста.txt', 'a')
        if self.ui.radioButton.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[4 + 6 * (self.i - 1)][1] + '\n')
        elif self.ui.radioButton_2.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[5 + 6 * (self.i - 1)][1] + '\n')
        elif self.ui.radioButton_3.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[6 + 6 * (self.i - 1)][1] + '\n')
        elif self.ui.radioButton_4.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[7 + 6 * (self.i - 1)][1] + '\n')
        self.file.close()
        self.i += 1
        self.ui.label_5.setText(str(self.i) + ' из ' + str(self.number))
        if self.i <= self.number:
            self.ui.label_2.setText(self.file_text[2 + 6 * (self.i - 1)])
            self.ui.label_3.setText(self.file_text[3 + 6 * (self.i - 1)])
            self.file_text[4 + 6 * (self.i - 1)] = self.file_text[4 + 6 * (self.i - 1)].split('&')
            self.ui.radioButton.setText(self.file_text[4 + 6 * (self.i - 1)][0])
            self.file_text[5 + 6 * (self.i - 1)] = self.file_text[5 + 6 * (self.i - 1)].split('&')
            self.ui.radioButton_2.setText(self.file_text[5 + 6 * (self.i - 1)][0])
            self.file_text[6 + 6 * (self.i - 1)] = self.file_text[6 + 6 * (self.i - 1)].split('&')
            self.ui.radioButton_3.setText(self.file_text[6 + 6 * (self.i - 1)][0])
            self.file_text[7 + 6 * (self.i - 1)] = self.file_text[7 + 6 * (self.i - 1)].split('&')
            self.ui.radioButton_4.setText(self.file_text[7 + 6 * (self.i - 1)][0])
        else:
            self.close()

    def load(self):
        if self.ui.lineEdit.text() != '':
            self.file = open('Результаты теста.txt', 'a')
            self.file.write(self.ui.lineEdit.text() + '\n')
            self.file.close()

            self.name = self.ui.lineEdit.text()
            self.ui.pushButton.setEnabled(True)
            self.ui.radioButton.setEnabled(True)
            self.ui.radioButton_2.setEnabled(True)
            self.ui.radioButton_3.setEnabled(True)
            self.ui.radioButton_4.setEnabled(True)
            self.ui.label.setEnabled(True)
            self.ui.label_2.setEnabled(True)
            self.ui.label_3.setEnabled(True)
            self.ui.lineEdit.setEnabled(False)
            self.ui.label_4.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)

            self.file = open('test.txt', 'rt')
            self.file_text = self.file.read()
            self.file.close()
            self.file_text = self.file_text.split('\n')

            self.ui.label.setText(self.file_text[0])
            self.number = int(self.file_text[1])
            self.ui.label_5.setText(str(self.i) + ' из ' + str(self.number))
            self.ui.label_2.setText(self.file_text[2])
            self.ui.label_3.setText(self.file_text[3])
            self.file_text[4] = self.file_text[4].split('&')
            self.ui.radioButton.setText(self.file_text[4][0])
            self.file_text[5] = self.file_text[5].split('&')
            self.ui.radioButton_2.setText(self.file_text[5][0])
            self.file_text[6] = self.file_text[6].split('&')
            self.ui.radioButton_3.setText(self.file_text[6][0])
            self.file_text[7] = self.file_text[7].split('&')
            self.ui.radioButton_4.setText(self.file_text[7][0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
