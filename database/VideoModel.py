from PyQt5 import QtCore
from database.VideomodelResource import VideomodelResource

class VideoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, link_id=None, **kwargs):
        super(VideoModel, self).__init__(*args, **kwargs)
        self.videos = VideomodelResource.get_nontrashed(link_id)


    def data(self, index, role=None):
        if role == QtCore.Qt.DisplayRole:
            row = self.videos[index.row()]

            return (row['name'] if row['name'] else row['v_id'])


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.videos)


    @staticmethod
    def get_by_linkid(link_id):
        return VideomodelResource.get_by_linkid(link_id)


    @staticmethod
    def get_nondownloaded_videos():
        return VideomodelResource.get_nondownloaded_videos()


    @staticmethod
    def store_new_videoids(link_id, v_ids):
        VideomodelResource.store_new_videoids(link_id, v_ids)


    @staticmethod
    def update(data={}):
        if not data.get('id') or len(data) < 2:
            return False

        VideomodelResource.update(data)

        return True