from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QProcess

class FunctionHandler:
    def __init__(self, ui):
        self.ui = ui
        self.devices_selected = False
        self.buttons_selected = False
        self.selected_devices_list = []

    def is_device_connected(self, device):
        process = QtCore.QProcess()
        process.start("adb", ["devices"])

        process.waitForFinished()
        result = process.readAllStandardOutput().data().decode("utf-8")

        return device in result

    def cb_device(self, state, device):
        if device not in self.ui.menu_kiri_dict:
            print(f"Device {device} not found in menu_kiri dictionary.")
            return

        print(f"Before Update - {device} Checkbox State: {self.ui.menu_kiri_dict[device].isChecked()}")
        self.ui.menu_kiri_dict[device].setChecked(state)
        
        if state:
            self.selected_devices_list.append(device)
        else:
            self.selected_devices_list.remove(device)

        self.update_status()

    def rb_script(self, nama_fungsi):
        checkbox_attr = getattr(self.ui, f"b_{nama_fungsi.lower()}")
        self.buttons_selected = checkbox_attr.isChecked()
        self.update_status()

    def update_status(self):
        self.ui.devices_selected = any(checkbox.isChecked() for checkbox in self.ui.menu_kiri_dict.values())
        self.ui.buttons_selected = any(getattr(self.ui, f"b_{nama_fungsi.lower()}").isChecked() for nama_fungsi in ["Reboot", "GetSim", "Bersih", "Meninjau", "Backup", "Captcha", "Regist"])

        # Menampilkan informasi di status bar
        selected_devices = [f"Device {index + 1}" for index, (device, checkbox) in enumerate(self.ui.menu_kiri_dict.items()) if checkbox.isChecked()]
        print(f"After Update - Checkbox States: {[checkbox.isChecked() for checkbox in self.ui.menu_kiri_dict.values()]}")
        print(f"Selected Devices: {', '.join(selected_devices)}")
        self.ui.statusBar().showMessage(f"Selected Devices: {', '.join(selected_devices)}")

        self.ui.devices_selected = self.selected_devices_list

    def run(self):
        print(f"Devices Selected: {self.selected_devices_list}")
        print(f"Buttons Selected: {self.buttons_selected}")

        if self.selected_devices_list and self.buttons_selected:
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
