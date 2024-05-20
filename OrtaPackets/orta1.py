from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QBrush
import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFrame
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QApplication
from orta import AnaSayfa
from PyQt5.QtCore import QEvent


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super(ClickableLabel, self).__init__(text, parent)
        self.setStyleSheet("font-size: 10pt; color: black; cursor: pointer;")  

    def mousePressEvent(self, event):
        self.clicked.emit()

class VideoPage(QWidget):
    def __init__(self, title, video_path, ana_sayfa):
        super().__init__()
        self.video_visible = False
        self.ana_sayfa = ana_sayfa
        self.initUI(title, video_path)

    def initUI(self, title, video_path):
        layout = QVBoxLayout()

        self.title_label = ClickableLabel(title, self)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        self.title_label.clicked.connect(self.toggle_video_visibility)

        self.video_widget = QVideoWidget(self)
        self.video_widget.hide()
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.player.setVideoOutput(self.video_widget)
        self.video_widget.setFixedSize(540, 540)  
        layout.addWidget(self.video_widget)

        self.play_pause_button = QPushButton("Başlat", self)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        self.play_pause_button.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #848094; border-radius: 10px; padding: 10px; transition: background-color 0.3s; }"
            "QPushButton:hover { background-color: #5CDB95; }"
        )  
        layout.addWidget(self.play_pause_button)
        
        
        self.geri_button = QPushButton("Geri Dön", self)
        self.geri_button.clicked.connect(self.go_back)
        layout.addWidget(self.geri_button)
        self.geri_button.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #848094; border-radius: 10px; padding: 10px; transition: background-color 0.3s; }"
            "QPushButton:hover { background-color: #5CDB95; }"
        )  
        self.setLayout(layout)

    def toggle_play_pause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_pause_button.setText("Başlat")
        else:
            self.player.play()
            self.play_pause_button.setText("Durdur")

    def toggle_video_visibility(self):
        self.video_visible = not self.video_visible
        self.video_widget.setVisible(self.video_visible)
        if self.video_visible:
            self.play_pause_button.setText("Başlat")
        else:
            self.player.pause()
            self.play_pause_button.setText("Durdur")

    def go_back(self):
        self.close()  # VideoPage penceresini kapat
        ana_sayfa = AnaSayfa()
        ana_sayfa.show()  # Yeni AnaSayfa penceresini aç

class BaslangicPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ana_sayfa = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Orta 1 Paketi")
        self.setGeometry(400, 200, 900, 650) 

        pixmap = QPixmap("Photos/background.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        self.setStyleSheet("font-family: 'Arial'; font-size: 12pt; color: white;")  
        
        layout = QVBoxLayout()
        self.top_stacked_widget = QStackedWidget(self)
        bottom_button_layout = QHBoxLayout()
        self.bottom_stacked_widget = QStackedWidget(self)

        button_style = "QPushButton { font-size: 10pt; background-color: #804f57; border-radius: 10px; padding: 10px; transition: background-color 0.3s; }" \
                       "QPushButton:hover { background-color: #5CDB95; }"

        titles = ["Isınma", "Üst Vücut", "Alt Vücut", "Karın"]
        video_paths = [os.path.abspath(f"videos/Orta/Orta1/{title}.mp4") for title in titles]

        for i in range(4):
            video_page = VideoPage(titles[i], video_paths[i],self.ana_sayfa)
            self.bottom_stacked_widget.addWidget(video_page)
            bottom_button = QPushButton(titles[i], self)
            bottom_button.setStyleSheet(button_style)
            bottom_button.setFixedSize(130, 50)  
            bottom_button_layout.addWidget(bottom_button)
            bottom_button.clicked.connect(lambda _, index=i: self.change_bottom_page(index))

        layout.addLayout(bottom_button_layout)
        layout.addWidget(self.bottom_stacked_widget)

        self.setLayout(layout)

    def change_bottom_page(self, index):
        self.bottom_stacked_widget.setCurrentIndex(index)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ana_sayfa = AnaSayfa()
    baslangic_page = BaslangicPage()
    baslangic_page.ana_sayfa = ana_sayfa
    baslangic_page.show()  # Sonra başlangıç sayfasını göster
    sys.exit(app.exec_())
