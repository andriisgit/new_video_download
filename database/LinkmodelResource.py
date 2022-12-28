from os import path
import sqlite3


class LinkmodelResource:

    @staticmethod
    def get():
        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)

        cursor = conn.cursor()
        cursor.execute('SELECT `id`,`link`,`link_type` FROM `links`')
        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def store(data={}):
        if len(data) == 0:
            return False

        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)

        cursor = conn.cursor()
        fields = []
        values = []
        places = []

        for field in data:
            fields.append(field)
            values.append(data[field])
            places.append('?')

        fields = ','.join(fields)
        places = ','.join(places)
        query = 'INSERT INTO `links` (' + fields + ') VALUES (' + places + ')'
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return True
