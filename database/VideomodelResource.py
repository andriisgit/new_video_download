from os import path
import sqlite3


class VideomodelResource():

    @staticmethod
    def get_by_linkid(link_id):
        if not link_id:
            return list()

        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)
        cursor = conn.cursor()

        query = 'SELECT `id`,`link_id`,`v_id`,`name`,`pulled_at` FROM `videos` '
        query += 'WHERE `link_id`=' + str(link_id)

        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def get_nontrashed(link_id):
        if not link_id:
            return list()

        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)
        cursor = conn.cursor()

        query = 'SELECT `id`,`link_id`,`v_id`,`name`,`file_name`,`pulled_at` FROM `videos` '
        query += 'WHERE `trashed_at` IS NULL AND `link_id`=' + str(link_id)
        query += ' ORDER BY `pulled_at` DESC'

        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def get_nondownloaded_videos():
        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)
        cursor = conn.cursor()

        query = 'SELECT `id`,`link_id`,`v_id` FROM `videos` WHERE `trashed_at` IS NULL AND `pulled_at` IS NULL'
        cursor.execute(query)
        data = cursor.fetchall()

        conn.close()

        return data


    @staticmethod
    def store_new_videoids(link_id, v_ids):
        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)
        cursor = conn.cursor()

        query = """INSERT INTO `videos` (`link_id`, `v_id`)
            SELECT :link_id, :v_id
            WHERE NOT EXISTS (
                SELECT `id`
                FROM `videos`
                WHERE `link_id`= :link_id AND v_id= :v_id
            )"""
        values = []
        for v_id in v_ids:
            values.append({'link_id': link_id, 'v_id': v_id})

        cursor.executemany(query, values)
        conn.commit()

        conn.close()


    @staticmethod
    def update(data={}):
        conn = sqlite3.connect(path.join('database', 'database.sqlite3'))
        conn.row_factory = sqlite3.Row
        # conn.set_trace_callback(print)
        cursor = conn.cursor()

        update_set = []
        for field in data:
            if field != 'id':
                update_set.append(" `" + field + "` = '" + str(data[field]) + "' ")

        update_set = ','.join(update_set)
        query = 'UPDATE `videos` SET ' + update_set + ' WHERE `id` = ' + str(data['id'])

        cursor.execute(query)
        conn.commit()
        conn.close()
