import time
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from bs4 import BeautifulSoup
import requests
import re
from database.LinkModel import LinkModel
from database.VideoModel import VideoModel
from DownloadThread import DownloadThread


class ScanThread(QObject, Thread):

    status_msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.scanning = True
        self.start_qdate = None


    def run(self):

        while self.scanning:

            for link_row in LinkModel.get():
                if 'VIDEOS' == link_row['link_type']:
                    self.scan_link_videos(link_row)
                # if 'PLAYLISTS' == link_row['link_type']:
                #     self.scan_link_playlist(link_row)

                time.sleep(30)


    def scan_link_videos(self, link_row):
        self.status_msg.emit('Пошук оновлень videos за ' + link_row['link'])
        v_ids = self.scrape_videos_videoids(link_row['link'])
        v_ids = v_ids[::4]
        v_ids = self.remove_existing_videoids(link_id=link_row['id'], v_ids=v_ids)
        v_ids = self.filterby_date_videoids(v_ids)
        VideoModel.store_new_videoids(link_id=link_row['id'], v_ids=v_ids)


    def scan_link_playlist(self, link_row):
        self.status_msg.emit('Пошук оновлень playlist за ' + link_row['link'])
        v_ids = self.scrape_playlists_videoids(link_row['link'])
        v_ids = v_ids[::3]
        v_ids = v_ids[:-2]
        v_ids = self.remove_existing_videoids(link_id=link_row['id'], v_ids=v_ids)
        VideoModel.store_new_videoids(link_id=link_row['id'], v_ids=v_ids)


    @staticmethod
    def scrape_videos_videoids(link):

        # return ['uvvAtwtPM00', 'vv8wu967eUk', 'zHUtTV9WkG4']

        req = requests.get(link)
        send = BeautifulSoup(req.text, "html.parser")
        search = send.find_all("script")
        key = '"videoId":"'
        data = re.findall(key + r"([^*]{11})", str(search))

        return data



    @staticmethod
    def scrape_playlists_videoids(link):
        req = requests.get(link)
        send = BeautifulSoup(req.text, "html.parser")
        search = send.find_all("script")
        key = '"playlistId":"'
        data = re.findall(key + r"([^*]{34})", str(search))

        return data


    @staticmethod
    def remove_existing_videoids(link_id, v_ids) -> list:
        existing_v_ids = []

        for row in VideoModel.get_by_linkid(link_id):
            existing_v_ids.append(row['v_id'])

        return list(set(v_ids) - set(existing_v_ids))


    def filterby_date_videoids(self, v_ids) -> list:
        if not self.start_qdate:
            return v_ids

        start_date = None
        filtered_v_ids = []
        try:
            start_date = time.strptime(self.start_qdate.toString(QtCore.Qt.ISODate), '%Y-%m-%d')
        except ValueError:
            pass

        if not start_date:
            return v_ids

        for v_id in v_ids:
            videoinfo = DownloadThread.get_youtube_videoinfo(url=('https://www.youtube.com/watch?v=' + v_id))
            if not videoinfo or not videoinfo['upload_date']:
                continue

            try:
                upload_date = time.strptime(videoinfo['upload_date'], '%Y%m%d')
            except ValueError:
                upload_date = None

            if not upload_date:
                continue

            if start_date <= upload_date:
                filtered_v_ids.append(v_id)

            time.sleep(2)

        return filtered_v_ids
