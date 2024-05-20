from pywinauto.application import Application
import pywinauto
from pywinauto import Desktop
desktop = Desktop(backend="win32")
dlg = desktop.window(title_re=".*向日葵远程控制.*")

# 打印控件标识符
dlg.print_control_identifiers()
# 启动应用程序
app = Application().start("D:/xiangrikui/SunloginClient/SunloginClient.exe")
oray_ui_controls = dlg.child_window(class_name="OrayUI")
print(oray_ui_controls)

