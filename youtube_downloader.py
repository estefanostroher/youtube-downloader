import sys, os

from PyQt5.QtCore import QUrl, QThread
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

import pytube

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
        self.setGeometry(0, 0, 720, 144)
        self.setMaximumHeight(144)
        self.setMaximumWidth(720)
        self.setMinimumHeight(144)
        self.setMinimumWidth(720)

    def selectSaveLocation(self):
        # Usa o QFileDialog para selecionar o local do vídeo a ser salvo.
        save_location_button = QFileDialog.getExistingDirectory(self, 'Save Video', '/', QFileDialog.ShowDirsOnly)
        self.save_location_button = save_location_button

    def download(self):
        # Pega a URL do vídeo do QLineEdit.
        url = self.url_edit.text()

        # Pega a resolução do vídeo selecionada do QComboBox.
        resolution = self.resolution_combo.currentText()

        # Seta o formato da resolução baseado no que foi selecionado.
        if resolution == '144p':
            resolution_video = '144p'
        if resolution == '240p':
            resolution_video = '240p'
        if resolution == '360p':
            resolution_video = '360p'
        if resolution == '480p':
            resolution_video = '480p'
        if resolution == '720p':
            resolution_video = '720p'
        elif resolution == '1080p':
            resolution_video = '1080p'

        # Usa o Pytube para obter o objeto do vídeo e definir a resolução a ser baixada.
        video = pytube.YouTube(url)
        stream = video.streams.filter(res = resolution_video).first()

        # Usa o QFileDialog para selecionar o diretório onde o vídeo será salvo.
        directory = QFileDialog.getExistingDirectory(self, 'Save Video', '/', QFileDialog.ShowDirsOnly)

        # Mostra a mensagem "Downloading" quando o vídeo começar a baixar.
        QMessageBox.information(self, 'Downloading', 'Download foi iniciado!')

        # Se caso não for possível baixar o vídeo, uma mensagem de erro aparecerá.
        try:
            # Usa Pytube para baixar o vídeo
            filename = video.title + ".mp4"
            file_path = os.path.join(directory, filename)
            stream.download(output_path = directory, filename = filename)
            QMessageBox.information(self, 'Sucesso', 'Vídeo baixado com sucesso!')
        except pytube.exceptions.VideoUnavailable as e:
            QMessageBox.warning(self, 'Erro', 'Erro ao baixar o vídeo!: ' + str(e))
        except OSError as e:
            QMessageBox.warning(self, 'Erro', 'Erro ao salvar o vídeo!: ' + str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = YouTubeDownloader()
    downloader.show()
    sys.exit(app.exec_())
