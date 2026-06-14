import sys
import os
import subprocess
import re
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout

class SrsUeConfigApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("srsUE 5G Manager")
        self.resize(450, 250)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.imsi_input = QLineEdit()
        self.imsi_input.setText("901700000000001")
        
        self.k_input = QLineEdit()
        self.k_input.setText("465B5CE8B199B49FAA5F0A2EE238A6BC")

        self.opc_input = QLineEdit()
        self.opc_input.setText("E8ED289DEBA952E4283B54E88E6183CA")

        self.apn_input = QLineEdit()
        self.apn_input.setText("internet") 

        form_layout.addRow("IMSI:", self.imsi_input)
        form_layout.addRow("Key (K):", self.k_input)
        form_layout.addRow("OPc:", self.opc_input)
        form_layout.addRow("APN:", self.apn_input)

        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("1. Save Config")
        self.save_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;")
        self.save_btn.clicked.connect(self.save_config)

        self.run_btn = QPushButton("2. Start srsUE")
        self.run_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.run_btn.clicked.connect(self.run_srsue)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.run_btn)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        self.srsue_process = None 

    def save_config(self):
        conf_path = "ue.conf"
        if not os.path.exists(conf_path):
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file ue.conf!")
            return

        try:
            with open(conf_path, 'r') as file:
                content = file.read()
            
            
            def update_val(key, val, text):
                pattern = rf'(?i)^\s*{key}\s*=.*'
                if re.search(pattern, text, re.MULTILINE):
                    return re.sub(pattern, f"{key} = {val}", text, flags=re.MULTILINE)
                else:
                    return re.sub(r'(?i)(\[usim\])', rf'\1\n{key} = {val}', text)
            content = update_val('imsi', self.imsi_input.text().strip(), content)
            content = update_val('k', self.k_input.text().strip(), content)
            content = update_val('opc', self.opc_input.text().strip(), content)
            
     
            content = update_val('algo', 'milenage', content)

            with open(conf_path, 'w') as file:
                file.write(content)
                
            QMessageBox.information(self, "Thành công", "Đã cập nhật ue.conf!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi ghi file: {str(e)}")


    def run_srsue(self):
  
        if self.srsue_process is not None and self.srsue_process.poll() is None:
            QMessageBox.warning(self, "Cảnh báo", "srsUE đang chạy!")
            return
            
        try:
            # Lệnh gọi ngầm dưới hệ thống
            self.srsue_process = subprocess.Popen(["sudo", "srsue", "ue.conf"])
            QMessageBox.information(self, "Đang kết nối", "Đã gửi lệnh chạy srsUE!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ Thống", f"Không thể khởi động srsUE: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SrsUeConfigApp()
    window.show()
    sys.exit(app.exec())