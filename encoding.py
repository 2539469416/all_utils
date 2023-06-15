import base64
import sys
import urllib.parse
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, \
    QMessageBox, QComboBox


class Transcoder(QWidget):
    def __init__(self):
        super().__init__()
        self.now_option = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('转码工具')

        # 创建垂直布局
        layout = QVBoxLayout()

        combobox = QComboBox()
        combobox.addItem('请选择转码类型')
        combobox.addItem('Hex转字符串')
        combobox.addItem('url解码')
        combobox.addItem('base64解码')
        combobox.addItem('base64编码')
        combobox.currentIndexChanged.connect(self.onComboBoxIndexChanged)

        # 创建文本编辑框
        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)

        self.input_text_edit = QTextEdit()
        self.input_text_edit.textChanged.connect(self.onTextChanged)
        # 将布局添加到主布局中
        layout.addWidget(self.input_text_edit)
        layout.addWidget(combobox)
        layout.addWidget(self.result_text_edit)
        self.setLayout(layout)
        self.now_option = 0

    def defult(self):
        input_text = self.input_text_edit.toPlainText()
        return input_text

    def urlEncode(self):
        print('url解码')
        input_text = self.input_text_edit.toPlainText()
        encoded_text = urllib.parse.quote(input_text)
        return encoded_text

    def hexToString(self):
        print('hex转字符串')
        input_text = self.input_text_edit.toPlainText()
        try:
            decoded_text = bytes.fromhex(input_text).decode('utf-8')
            return decoded_text
        except ValueError:
            return '无效的 Hex 字符串'

    def base64ToString(self):
        print('base64转String')
        try:
            input_text = self.input_text_edit.toPlainText()
            res = base64.b64decode(input_text).decode('utf-8')
            return res
        except Exception as e:
            return "错误的base64编码格式"

    def StringTobase64(self):
        input_text = self.input_text_edit.toPlainText()
        res = base64.b64encode(input_text.encode('utf-8')).decode('utf-8')
        return res

    def show_result(self, result):
        print('result')
        self.result_text_edit.setText(result)

    def onTextChanged(self):
        self.onComboBoxIndexChanged(self.now_option)

    def onComboBoxIndexChanged(self, option):
        try:
            self.now_option = option
            if 0 == option:
                res = self.defult()
                self.show_result(res)
            if 1 == option:
                res = self.hexToString()
                self.show_result(res)
            if 2 == option:
                res = self.urlEncode()
                self.show_result(res)
            if 3 == option:
                res = self.base64ToString()
                self.show_result(res)
            if 4 == option:
                res = self.StringTobase64()
                self.show_result(res)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        window = Transcoder()
    except Exception as e:
        print(e)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
