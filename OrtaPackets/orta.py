import os
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication

class AnaSayfa(QWidget):
    instance = None  # AnaSayfa örneğini saklamak için sınıf değişkeni

    def __init__(self):
        super().__init__()
        self.initUI()
        AnaSayfa.instance = self 
        
    @staticmethod    
    def get_instance():
        return AnaSayfa.instance

    def initUI(self):
        self.setWindowTitle("Orta Ana Sayfa")
        self.setGeometry(400, 200, 400, 300)

        layout = QVBoxLayout()

        baslangic1_button = QPushButton("Orta 1 Paketi", self)
        baslangic1_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\OrtaPackets\\orta1.py"))
        layout.addWidget(baslangic1_button)

        baslangic2_button = QPushButton("Orta 2 Paketi", self)
        baslangic2_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\OrtaPackets\\orta2.py"))
        layout.addWidget(baslangic2_button)

        baslangic3_button = QPushButton("Orta 3 Paketi", self)
        baslangic3_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\OrtaPackets\\orta3.py"))
        layout.addWidget(baslangic3_button)

        self.setLayout(layout)

    def open_baslangic(self, script_path):
        os.system(f"python \"{script_path}\"")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa()
    ana_sayfa.show()
    sys.exit(app.exec_())

