import os
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QApplication

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
        self.setWindowTitle("Başlangıç Ana Sayfa")
        self.setGeometry(600, 400, 600, 500)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Yeşil arka plan */
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Hover için daha koyu yeşil */
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
            }
        """)

        layout = QVBoxLayout()

        baslangic1_button = QPushButton("Başlangıç 1 Paketi", self)
        baslangic1_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        layout.addWidget(baslangic1_button)

        # Yeni eklenen "Hareket Adı" ve "Önizle" butonu için horizontal layout
        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Squat", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)

        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Leg Lateral Raise", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)


        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Plank", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)
        
        baslangic2_button = QPushButton("Başlangıç 2 Paketi", self)
        baslangic2_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic2.py"))
        layout.addWidget(baslangic2_button)
        
        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Side Arm Raise", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)
        
        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Plie Squads", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)

        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Hip Raises", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox)     

        baslangic3_button = QPushButton("Başlangıç 3 Paketi", self)
        baslangic3_button.clicked.connect(lambda: self.open_baslangic(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic3.py"))
        layout.addWidget(baslangic3_button)


        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Leg Raises", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox) 

        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Bridge", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox) 

        hareket_hbox = QHBoxLayout()
        hareket_adi_label = QLabel("Hareket Adı: Scissors", self)
        hareket_hbox.addWidget(hareket_adi_label)

        onizle_button = QPushButton("Önizle", self)
        onizle_button.setFixedSize(100, 50)  # Buton boyutunu küçült
        onizle_button.clicked.connect(lambda: self.preview_hareket(r"C:\\Users\\Excalibur\\OneDrive\\Masaüstü\\FitCheck-App\\BaslangicPackets\\baslangic1.py"))
        hareket_hbox.addWidget(onizle_button)
        layout.addLayout(hareket_hbox) 


        
        self.setLayout(layout)

    def open_baslangic(self, script_path):
        os.system(f"python \"{script_path}\"")

    def preview_hareket(self, script_path):
        os.system(f"python \"{script_path}\"")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa()
    ana_sayfa.show()
    sys.exit(app.exec_())
