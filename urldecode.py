import sys
import urllib.parse
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox

class UrlDecodeTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("URL 解码工具")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        self.input_text = QTextEdit(self)
        layout.addWidget(self.input_text)

        decode_button_layout = QHBoxLayout()
        self.decode_button = QPushButton("URL 解码", self)
        self.decode_button.clicked.connect(self.decode_text)
        decode_button_layout.addWidget(self.decode_button)

        layout.addLayout(decode_button_layout)

        self.output_label = QLabel(self)
        layout.addWidget(self.output_label)

        copy_button = QPushButton("复制结果", self)
        copy_button.clicked.connect(self.copy_result)
        layout.addWidget(copy_button)

        main_widget.setLayout(layout)

    def decode_text(self):
        input_text = self.input_text.toPlainText()
        decoded_text = urllib.parse.unquote(input_text)
        self.output_label.setText("解码结果:\n" + decoded_text)

    def copy_result(self):
        result = self.output_label.text().split('\n', 1)[1]  # Get the result part
        clipboard = QApplication.clipboard()
        clipboard.setText(result)
        QMessageBox.information(self, "复制成功", "结果已复制到剪贴板！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UrlDecodeTool()
    window.show()
    sys.exit(app.exec_())
