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
    conn = sql.connect("youtube.db")
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    conn.close()
    print("Video added to the database! ;D")
