# -*- coding: utf-8 -*-
import os
import platform
import sys
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMessageBox, QInputDialog, QDialog)
try:
    from database.LinkModel import LinkModel
    from database.VideoModel import VideoModel
    from DownloadThread import DownloadThread
    from ScanThread import ScanThread
    from window.DateDialog import DateDialog
except ImportError as err:
    print('Перевірте правильність установки та структуру каталогів')
    print(err)
    sys.exit(1)
from window.main import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start_qdate = None

        if self.check_dirs():
            self.set_start_date()
            self.link_model = LinkModel()
            self.links_view.setModel(self.link_model)

            self.menu_add_playlist.triggered.connect(self.handle_add_playlists)
            self.menu_add_video.triggered.connect(self.handle_add_videos)
            self.menu_quit.triggered.connect(self.handle_quit)
            self.links_view.clicked.connect(self.load_video_list)
            self.videos_view.doubleClicked.connect(self.show_file)

            self.start_scaner()
            self.start_downloader()
        else:
            sys.exit(1)


    def check_dirs(self) -> bool:
        err = []
        the_path = os.getcwd()

        check_path = os.path.join(the_path, 'database')
        if not os.path.exists(check_path):
            err.append('Не знайдено каталог даних database в ' + the_path)

        check_path = os.path.join(the_path, 'database', 'database.sqlite3')
        if not os.path.exists(check_path):
            err.append('Не знайдено файл для зберігання даних database.sqlite3')

        check_path = os.path.join(the_path, 'Videos')
        if not os.path.exists(check_path):
            err.append('Не знайдено каталог Videos для зберігання відео в ' + the_path)

        if err:
            self.msg_box(', '.join(err))
            return False
        else:
            return True


    def set_start_date(self):
        date_dlg = DateDialog()
        result = date_dlg.exec()
        if result == QtWidgets.QDialog.Accepted:
            self.start_qdate = date_dlg.ui.calendarWidget.selectedDate()


    def start_scaner(self):
        scaner = ScanThread()
        scaner.daemon = True
        scaner.status_msg.connect(self.status_msg)
        scaner.start_qdate = self.start_qdate
        scaner.start()


    def start_downloader(self):
        downloader = DownloadThread()
        downloader.daemon = True
        downloader.status_msg.connect(self.status_msg)
        downloader.update_video_list.connect(self.load_video_list)
        downloader.start()


    def update_video_list(self, list_id):
        self.videos_view.layoutChanged.emit()


    def status_msg(self, msg):
        self.statusbar.showMessage(msg)


    @staticmethod
    def msg_box(text=''):
        dialog = QMessageBox()
        dialog.setText(text)
        # dialog.setInformativeText("<i>Скопіюйте посилання на відео з адресного рядка браузера</i>")
        dialog.setWindowTitle("Відео")
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        dialog.exec_()


    def input(self, dlg_title='', dlg_prompt='') -> str:
        text, ok = QInputDialog.getText(self, dlg_title, dlg_prompt)
        if ok:
            users_input = str(text)
        else:
            users_input = ''

        return users_input


    def load_video_list(self):
        links_view_item = self.links_view.selectedIndexes()
        if not links_view_item:
            return

        links_view_item = links_view_item[0].row()
        link = self.link_model.links[links_view_item]

        self.video_model = VideoModel(link_id=link['id'])
        self.videos_view.setModel(self.video_model)


    def show_file(self):
        item = self.videos_view.selectedIndexes()
        if not item:
            return

        item = item[0].row()
        video = self.video_model.videos[item]

        if not video['file_name']:
            self.msg_box("Невідоме і'мя файла. Можливо, ще не скачено")
            return

        dir_path = os.getcwd()
        the_file = os.path.join(dir_path, 'Videos', video['file_name'])
        if not os.path.exists(the_file):
            self.msg_box('Файл не знайдено ' + the_file)
            return

        if platform.system() == 'Windows':
            os.startfile(the_file)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', the_file])
        else:
            subprocess.Popen(['xdg-open', the_file])


    def handle_add_videos(self):
        url = self.input(dlg_title='Додати перелік Відео', dlg_prompt='Введіть посилання на перелік <b>Відео канала</b>, наприклад <pre>https://www.youtube.com/@IrynaFarion/videos</pre>')
        if url:
            if self.link_model.store({'link_type': 'VIDEOS', 'link': url}):
                #self.link_model.links.append({'link_type': 'VIDEOS', 'link': url})
                self.link_model.load()
                self.link_model.layoutChanged.emit()


    def handle_add_playlists(self):
        url = self.input(dlg_title='Додати Плейліст', dlg_prompt='Введіть посилання на перелік Плейліст канала')
        print(url)
        if url:
            if self.link_model.store({'link_type': 'PLAYLISTS', 'link': url}):
                #self.link_model.links.append({'link_type': 'VIDEOS', 'link': url})
                self.link_model.load()
                self.link_model.layoutChanged.emit()


    def handle_quit(self):
        self.status_msg(msg='Вихід')
        # self.worker.scanning = False
        # self.worker.downloading = False
        QtWidgets.QApplication.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
