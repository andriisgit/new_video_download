from datetime import datetime
from os import path
from threading import Thread
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from database.VideoModel import VideoModel
import youtube_dl


class DownloadThread(QObject, Thread):

    status_msg = QtCore.pyqtSignal(str)
    update_video_list = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.downloading = True


    def run(self):
        while self.downloading:

            for v in VideoModel.get_nondownloaded_videos():
                videoinfo = self.get_youtube_videoinfo(url=('https://www.youtube.com/watch?v=' + v['v_id']))
                if not videoinfo:
                    self.status_msg.emit('Помилка отримання інф про відео ' + v['v_id'])
                    sleep(2)
                    continue

                self.status_msg.emit('Скачування відео ' + v['v_id'])

                if not self.download_video(videoinfo):
                    sleep(2)
                    continue

                VideoModel.update({
                    'id': v['id'],
                    'name': videoinfo['title'],
                    'pulled_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'file_name': v['v_id'] + '.' + videoinfo['ext']
                })

                self.update_video_list.emit(v['link_id'])

                sleep(60)

            sleep(2)


    @staticmethod
    def get_youtube_videoinfo(url):
        ydl = youtube_dl.YoutubeDL()
        try:
            result = ydl.extract_info(url, download=False)

            if 'entries' in result:
                videoinfo = result['entries'][0]
            else:
                videoinfo = result

            # videoinfo[
            #   'id': 'ubmwoptjFBc',
            #   'title': str,
            #   'description': str,
            #   'thumbnail': [],
            #   'webpage_url',
            #   'upload_date': '20221112',
            #   'webpage_url': 'https://www.youtube.com/watch?v=ubmwoptjFBc',
            #   'ext': 'mp4'
            # ]

            return videoinfo
        except Exception as error:
            print(error)

            return None


    def download_video(self, video):
        ydl_options = {'format': 'best', 'outtmpl': path.join('Videos', video['id'] + '.' + video['ext'])}
        try:
            with youtube_dl.YoutubeDL(ydl_options) as ydl:
                ydl.download([video['webpage_url']])

            return True
        except Exception as error:
            self.status_msg.emit('Сталась помилка youtube_dl')

            return False
