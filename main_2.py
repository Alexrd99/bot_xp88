from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QCheckBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from fungsi_2 import FunctionHandler
import sys
import subprocess

class UiXP(QMainWindow):
    def __init__(self):
        super(UiXP, self).__init__()
        loadUi("ui/new_simple.ui", self)
        self.setWindowIcon(QIcon("img/icon.png"))
        self.pi_logo.setPixmap(QtGui.QPixmap("img/logo.png"))

        self.function_handler = FunctionHandler(self)
        self.setup_menu_kanan()
        self.setup_perintah()

        self.menu_kiri_dict = {}

        self.populate_menu_kiri()

        layout = QVBoxLayout(self.device_select)

        for device, checkbox in self.menu_kiri_dict.items():
            layout.addWidget(checkbox)

        self.update_menu_kiri()

    def is_device_connected(self, device):
        process = QtCore.QProcess()
        process.start("adb", ["devices"])

        # Membaca output dari perintah adb secara asinkron
        process.waitForFinished()
        result = process.readAllStandardOutput().data().decode("utf-8")

        return device in result

    def update_menu_kiri(self):
        for device, checkbox in self.menu_kiri_dict.items():
            checkbox.stateChanged.connect(lambda state, d=device: self.function_handler.cb_device(state, d.split('_')[1]))

    def populate_menu_kiri(self):
        output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
        lines = output.split('\n')[1:]
        devices = [line.split('\t')[0] for line in lines if line.strip() != '']

        for index, device in enumerate(devices):
            checkbox = QCheckBox(f"{index + 1}")
            self.menu_kiri_dict[f"device_{device}"] = checkbox

    def setup_menu_kanan(self):
        fungsi_tombol = {
            self.b_reboot: "Reboot",
            self.b_getsim: "GetSim",
            self.b_bersih: "Bersih",
            self.b_meninjau: "Meninjau",
            self.b_backup: "Backup",
            self.b_captcha: "Captcha",
            self.b_regist: "Regist",
        }

        for tombol, nama_fungsi in fungsi_tombol.items():
            tombol.clicked.connect(lambda _, nama=nama_fungsi: self.function_handler.rb_script(nama))

    def setup_perintah(self):
        self.b_run.clicked.connect(self.function_handler.run)
        self.b_runall.clicked.connect(self.function_handler.runall)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UiXP()
    ui.show()
    sys.exit(app.exec_())
