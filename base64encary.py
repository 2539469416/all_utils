import sys
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox

class Base64Tool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Base64 编码工具")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        self.input_text = QTextEdit(self)
        layout.addWidget(self.input_text)

        button_layout = QHBoxLayout()
        self.encode_button = QPushButton("编码", self)
        self.encode_button.clicked.connect(self.encode_text)
        button_layout.addWidget(self.encode_button)

        self.decode_button = QPushButton("解码", self)
        self.decode_button.clicked.connect(self.decode_text)
        button_layout.addWidget(self.decode_button)

        layout.addLayout(button_layout)

        self.output_label = QLabel(self)
        layout.addWidget(self.output_label)

        self.copy_button = QPushButton("复制结果", self)
        self.copy_button.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_button)

        main_widget.setLayout(layout)

    def encode_text(self):
        input_text = self.input_text.toPlainText()
        encoded_bytes = base64.b64encode(input_text.encode())
        encoded_text = encoded_bytes.decode()
        self.output_label.setText("编码结果:\n" + encoded_text)

    def decode_text(self):
        encoded_text = self.input_text.toPlainText()
        try:
            decoded_bytes = base64.b64decode(encoded_text)
            decoded_text = decoded_bytes.decode()
            self.output_label.setText("解码结果:\n" + decoded_text)
        except base64.binascii.Error as e:
            self.output_label.setText("解码失败: " + str(e))

    def copy_result(self):
        result = self.output_label.text().split('\n', 1)[1]  # Get the result part
        clipboard = QApplication.clipboard()
        clipboard.setText(result)
        QMessageBox.information(self, "复制成功", "结果已复制到剪贴板！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Base64Tool()
    window.show()
    sys.exit(app.exec_())
