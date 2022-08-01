import sqlite3 as sql


def create_db():
    conn = sql.connect("youtube.db")
    cursor = conn.cursor()
    cursor.executescript(
        '''CREATE TABLE IF NOT EXISTS channels (
            id TEXT,
            name TEXT,
            url TEXT,
            thumbnail_url TEXT,
            added_date TEXT
            );
            CREATE TABLE IF NOT EXISTS videos (
            channel_id TEXT,
            id TEXT,
            upload_date INT,
            title TEXT,
            description TEXT,
            views INT,
            likes INT,
            downloaded INT,
            modified_date TEXT
            );
            '''
    )
    conn.commit()
    conn.close()
    print("Database created! :D")


def insert_video(data: tuple):
    query = 'INSERT INTO videos VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
    query_data(query,data)
    print("Video added to the database! ;D")

def insert_channel(data: tuple):
    query = 'INSERT INTO channels VALUES(?, ?, ?, ?, ?)'
    query_data(query, data)
    print("Channel added to the database! ;D")


def query_data(query, data):
    conn = sql.connect("youtube.db")
    cursor = conn.cursor()
    cursor.execute(query,data)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def query_downloaded(id_data):
    id = {"id": id_data}
    query= 'SELECT downloaded FROM videos WHERE id = :id'
    return query_data(query,id)


def query_channel(id_data):
    id = {"id": id_data}
    query= 'SELECT * FROM channels WHERE id = :id'
    return query_data(query,id)

