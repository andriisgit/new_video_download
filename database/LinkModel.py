from PyQt5 import QtCore
from database.LinkmodelResource import LinkmodelResource


class LinkModel(QtCore.QAbstractListModel):

    def __init__(self, *args, **kwargs):
        super(LinkModel, self).__init__(*args, **kwargs)
        self.load()


    def data(self, index, role=None):
        if role == QtCore.Qt.DisplayRole:
            row = self.links[index.row()]

            return row['link']


    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.links)


    def load(self):
       self.links = self.get()


    @staticmethod
    def get():
        return LinkmodelResource.get()


    @staticmethod
    def store(data={}):
        return LinkmodelResource.store(data)
