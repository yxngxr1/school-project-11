import sys
from design.design import Ui_MainWindow
from PyQt5 import QtWidgets


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = ''
        self.file_text = ''
        self.number = 0
        self.i = 1  # страница

        self.ui.btn_next.clicked.connect(self.next)
        self.ui.btn_start.clicked.connect(self.load)

    def next(self):
        self.file = open('Результаты теста.txt', 'a')
        if self.ui.radioButton_1.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[3 + 5 * (self.i - 1)].split('&')[1] + '\n')
        elif self.ui.radioButton_2.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[4 + 5 * (self.i - 1)].split('&')[1] + '\n')
        elif self.ui.radioButton_3.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[5 + 5 * (self.i - 1)].split('&')[1] + '\n')
        elif self.ui.radioButton_4.isChecked():
            self.file.write(str(self.i) + ') ' + self.file_text[6 + 5 * (self.i - 1)].split('&')[1] + '\n')
        self.file.close()
        self.i += 1
        self.ui.label_page.setText(str(self.i) + ' из ' + str(self.number))
        if self.i <= self.number:
            self.ui.label_question.setText(self.file_text[2 + 5 * (self.i - 1)])
            self.ui.radioButton_1.setText(self.file_text[3 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_2.setText(self.file_text[4 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_3.setText(self.file_text[5 + 5 * (self.i - 1)].split('&')[0])
            self.ui.radioButton_4.setText(self.file_text[6 + 5 * (self.i - 1)].split('&')[0])
        else:
            self.close()

    def load(self):
        if self.ui.input_name.text() != '':
            self.file = open('Результаты теста.txt', 'a')
            self.file.write(self.ui.input_name.text() + '\n')
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

            self.file = open('test.txt', 'rt')
            self.file_text = self.file.read().split('\n')
            self.file.close()

            self.ui.label_test_name.setText(self.file_text[0])
            self.number = int(self.file_text[1])
            self.ui.label_page.setText(str(self.i) + ' из ' + str(self.number))

            # set first position
            self.ui.label_question.setText(self.file_text[2])
            self.ui.radioButton_1.setText(self.file_text[3].split('&')[0])
            self.ui.radioButton_2.setText(self.file_text[4].split('&')[0])
            self.ui.radioButton_3.setText(self.file_text[5].split('&')[0])
            self.ui.radioButton_4.setText(self.file_text[6].split('&')[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
