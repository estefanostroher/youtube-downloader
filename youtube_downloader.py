import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

import yt_dlp

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Cria com o QWebEngineView um display para a URl do vídeo.
        self.view = QWebEngineView(self)
        self.view.load(QUrl('https://www.youtube.com/'))

        # Uso do QLineEdit pro usuário entrar com a URL.
        self.url_edit = QLineEdit(self)

        # Cria o botão de download.
        download_button = QPushButton('Download', self)
        download_button.clicked.connect(self.download)

        # Usa do QComboBox a opção de selecionar a resolução que deseja baixar.
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItem('144p')
        self.resolution_combo.addItem('240p')
        self.resolution_combo.addItem('360p')
        self.resolution_combo.addItem('480p')
        self.resolution_combo.addItem('720p')
        self.resolution_combo.addItem('1080p')

        # Cria um botão para selecionar onde deseja salvar o vídeo baixado.
        save_location_button = QPushButton('Salvar Vídeo', self)
        save_location_button.clicked.connect(self.selectSaveLocation)

        # Cria o layout.
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.url_edit)
        layout.addWidget(save_location_button)
        layout.addWidget(self.resolution_combo)
        layout.addWidget(download_button)

        self.setLayout(layout)
        self.setWindowTitle('YouTube Downloader')

        # Faz com que a interface tenha sempre o mesmo tamanaho de 720x480.
        self.setGeometry(0, 0, 720, 480)
        self.setMaximumHeight(480)
        self.setMaximumWidth(720)
        self.setMinimumHeight(480)
        self.setMinimumWidth(720)

    def selectSaveLocation(self):
        # Usa o QFileDialog para selecionar o local do vídeo a ser salvo.
        save_location_button = QFileDialog.getSaveFileName(self, 'Save Video', '/', 'MP4 Files (*.mp4)')[0]
        self.save_location_button = save_location_button

    def download(self):
        # Pega a URL do vídeo do QLineEdit
        url = self.url_edit.text()

        # Pega a resolução do vídeo selecionada do QComboBox
        resolution = self.resolution_combo.currentText()

        # Seta o formato da resolução baseado no que foi selecionado.
        if resolution == '144p':
            height = 144
        if resolution == '240p':
            height = 240
        if resolution == '360p':
            height = 360
        if resolution == '480p':
            height = 480
        if resolution == '720p':
            height = 720
        elif resolution == '1080p':
            height = 1080

        # Usando opções do youtube-dl
        ydl_opts = {
            # Usa o formato especificado pelo usuário com a extensão .mp4
            'format': f'bestvideo[height={height}][ext=mp4]+bestaudio[ext=mp4a]/best[height={height}][ext=mp4]/',

            # Salva o vídeo no local especificado.
            'outtmpl': self.save_location_button,
        }

        # Se caso não for possível baixar o vídeo, uma mensagem de erro aparecerá.
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, 'Sucesso', 'Vídeo baixado com sucesso!')
        except yt_dlp.utils.DownloadError as e:
            QMessageBox.warning(self, 'Erro', 'Erro ao baixar o vídeo!: ' + str(e))
        except yt_dlp.utils.ContentTooShortError as e:
            QMessageBox.warning(self, 'Erro', 'Erro ao baixar o vídeo: ' + str(e))
        except FileNotFoundError as e:
            QMessageBox.warning(self, 'Erro', 'Erro ao salvar o vídeo!: ' + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = YouTubeDownloader()
    downloader.show()
    sys.exit(app.exec_())