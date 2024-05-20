from PyQt5.QtWidgets import QApplication,QFrame, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import psycopg2
from psycopg2 import OperationalError
import sys

# İlgili modüllerin dahil edilmesi
from BaslangicPackets.baslangic import AnaSayfa as BaslangicAnaSayfa
from OrtaPackets.orta import AnaSayfa as OrtaAnaSayfa
from UzmanPackets.uzman import AnaSayfa as UzmanAnaSayfa

# Veritabanı bağlantı bilgileri
db_name = "FitCheck"
db_user = "postgres"
db_password = "123123"
db_host = "localhost"
db_port = "5432"

# Veritabanı bağlantısını yapacak fonksiyon
def create_connection(db_name, db_user, db_password, db_host, db_port):
    try:
        return psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except OperationalError as e:
        print(f"Hata oluştu: '{e}'")
        return None

# Veritabanından kullanıcının spor seviyesini alacak fonksiyon
def get_sport_level(user_mail, connection):
    try:
        with connection.cursor() as cursor:
            query = "SELECT sport_level FROM kullanicilar WHERE mail = %s;"
            cursor.execute(query, (user_mail,))
            sport_level = cursor.fetchone()
            return sport_level[0] if sport_level else "Bilgi bulunamadı"
    except Exception as e:
        print(f"Spor seviyesi alınırken hata oluştu: {e}")
        return "Hata"

connection = create_connection(db_name, db_user, db_password, db_host, db_port)

class FitCheckApp(QWidget):
    def __init__(self, user_mail):
        super().__init__()
        self.user_mail = user_mail
        self.sport_level = get_sport_level(user_mail, connection)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('FitCheck')
        self.setStyleSheet("""
            QWidget {
            background-color: #ffffff;  /* Beyaz arka plan */
            color: #333333;  /* Koyu gri yazı rengi */
        }
        QLabel {
            font-size: 16px;  /* Yazı boyutu güncellendi */
            font-family: 'Roboto', sans-serif;  /* Modern font eklendi */
            padding: 12px;  /* Daha fazla padding */
        }
        QPushButton {
            background-color: #4CAF50;  /* Daha canlı bir yeşil renk */
            color: #ffffff;
            border-radius: 15px;  /* Yuvarlak köşe yarıçapı artırıldı */
            padding: 15px 30px;  /* Buton paddingi artırıldı */
            font-size: 18px;  /* Buton yazı boyutu artırıldı */
            font-weight: bold;  /* Yazı kalınlaştırıldı */
            border: none;  /* Kenar çizgisi kaldırıldı */
        }
        QPushButton:hover {
            background-color: #45a049;  /* Hover durumu için renk değişikliği */
        }
        QMessageBox {
            background-color: #f0f0f0;  /* Mesaj kutusu arka plan rengi */
        }
        QFrame {
            background-color: #e0e1c2;  /* Frame arka plan rengi */
            border: 2px solid #cccccc;  /* Kenar çizgisi kalınlaştırıldı ve rengi değiştirildi */
            padding: 15px;  /* Frame paddingi artırıldı */
            border-radius: 10px;  /* Frame köşe yarıçapı eklendi */
        }
    """)

        layout = QVBoxLayout()

        welcome_label = QLabel('FitCheck Uygulamasına Hoş Geldiniz', self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(welcome_label)

        sport_level_label = QLabel(f'Spor Seviyeniz: {self.sport_level}', self)
        sport_level_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(sport_level_label)

        update_level_label = QLabel("Spor Seviyenizin doğru olmadığını düşünüyorsanız lütfen web sitemizden güncelleyin.", self)
        update_level_label.setAlignment(Qt.AlignCenter)
        update_level_label.setStyleSheet("color: #888;")
        layout.addWidget(update_level_label)

        health_warning_label = QLabel(
            "Sağlık Uyarısı ve Tavsiye Bildirimi\n\n"
            "Lütfen dikkat: Bu platformda paylaşılan spor hareketleri ve paketler sadece genel bilgilendirme amaçlıdır ve herhangi bir sağlık durumu veya kişisel ihtiyaç göz önünde bulundurularak hazırlanmamıştır. Sunulan içerikler, profesyonel tıbbi tavsiye, teşhis ya da tedavinin yerini tutmaz. Herhangi bir yeni egzersiz programına başlamadan önce, özellikle kronik bir sağlık sorununuz varsa veya sağlığınıza ilişkin herhangi bir endişeniz varsa, doktorunuz veya sağlık hizmeti sağlayıcınızla danışmanız şiddetle önerilir. Bu uyarıları dikkate alarak, egzersizleri kendi sorumluluğunuz altında uygulayınız.", self)
        health_warning_label.setWordWrap(True)
        layout.addWidget(health_warning_label)
        packages_frame = QFrame(self)
        packages_layout = QVBoxLayout(packages_frame)
        packages_label = QLabel("Mevcut Spor Paketlerimiz:\n1. Başlangıç Seviye Spor Paketi\n2. Orta Seviye Spor Paketi\n3. Uzman Seviye Spor Paketi", packages_frame)
        packages_label.setAlignment(Qt.AlignCenter)
        packages_layout.addWidget(packages_label)
        layout.addWidget(packages_frame)

        baslangic_button = QPushButton('Başlangıç Paketi', self)
        baslangic_button.clicked.connect(self.openBaslangicAnaSayfa)
        layout.addWidget(baslangic_button)

        orta_button = QPushButton('Orta Paketi', self)
        orta_button.clicked.connect(self.openOrtaAnaSayfa)
        layout.addWidget(orta_button)

        uzman_button = QPushButton('Uzman Paketi', self)
        uzman_button.clicked.connect(self.openUzmanAnaSayfa)
        layout.addWidget(uzman_button)

        # Button access control
        if self.sport_level == 'Başlangıç':
            orta_button.setDisabled(True)
            uzman_button.setDisabled(True)
        elif self.sport_level == 'Orta':
            uzman_button.setDisabled(True)

        self.setLayout(layout)

    def openBaslangicAnaSayfa(self):
        self.ana_sayfa = BaslangicAnaSayfa()
        self.ana_sayfa.show()

    def openOrtaAnaSayfa(self):
        self.orta_ana_sayfa = OrtaAnaSayfa()
        self.orta_ana_sayfa.show()

    def openUzmanAnaSayfa(self):
        self.uzman_ana_sayfa = UzmanAnaSayfa()
        self.uzman_ana_sayfa.show()

def main():
    app = QApplication(sys.argv)
    mainWindow = FitCheckApp('laranazbaki@gmail.com')
    mainWindow.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
