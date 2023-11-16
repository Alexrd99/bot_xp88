from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess

class FunctionHandler:
    def __init__(self, ui):
        self.ui = ui
        self.update_menu_kiri = {}
        self.devices_selected = False
        self.buttons_selected = False

    def cb_device(self, state, device):
        if device not in self.update_menu_kiri:
            print(f"Device {device} not found in menu_kiri dictionary.")
            return

        print(f"Before Update - {device} Checkbox State: {self.update_menu_kiri[device].isChecked()}")
        self.update_menu_kiri[device].setChecked(state)
        self.update_status()

    def rb_script(self, nama_fungsi):
        checkbox_attr = getattr(self.ui, f"b_{nama_fungsi.lower()}")
        self.buttons_selected = checkbox_attr.isChecked()
        self.update_status()

    def update_status(self):
        self.devices_selected = any(checkbox.isChecked() for checkbox in self.update_menu_kiri.values())
        self.buttons_selected = any(getattr(self.ui, f"b_{nama_fungsi.lower()}").isChecked() for nama_fungsi in ["Reboot", "GetSim", "Bersih", "Meninjau", "Backup", "Captcha", "Regist"])

        # Menampilkan informasi di status bar
        selected_devices = [f"Device {index + 1}" for index, (device, checkbox) in enumerate(self.update_menu_kiri.items()) if checkbox.isChecked()]
        print(f"After Update - Checkbox States: {[checkbox.isChecked() for checkbox in self.update_menu_kiri.values()]}")
        print(f"Selected Devices: {', '.join(selected_devices)}")
        self.ui.statusBar().showMessage(f"Selected Devices: {', '.join(selected_devices)}")

    def run(self):
        print(f"Devices Selected: {self.devices_selected}")
        print(f"Buttons Selected: {self.buttons_selected}")

        if self.devices_selected and self.buttons_selected:
            print("Run button clicked")
            self.ui.statusBar().showMessage("Run Button Clicked")
        else:
            print("Devices or buttons not selected")
            msg = QMessageBox()
            msg.setWindowTitle("Warning!!!")
            msg.setText("Pilih Device dan Fungsi dulu Bolo!!!")
            icon = QIcon("img/Warning.png")
            msg.setWindowIcon(icon)
            msg.exec_()
    
    def runall(self):
        file_path = 'AllDevice.txt'
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
                print(f"Isi file {file_path}:\n{file_content}")
                self.ui.statusBar().showMessage(f"Isi file {file_path}:\n{file_content}")
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                file.write("Running All Device.....")
                print(f"File baru berhasil dibuat: {file_path}")
                self.ui.statusBar().showMessage(f"File baru berhasil dibuat: {file_path}")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            self.ui.statusBar().showMessage(f"Terjadi kesalahan: {e}")
