from yt_dlp import YoutubeDL
from datetime import datetime

import videodownloader.db as db

channels = {
    'agustin01 tutoriales': 'https://www.youtube.com/channel/UCOARbH8Vn6aacb8JQgpfEaw',
    'agustin01 canciones': 'https://www.youtube.com/channel/UCq9r1AmRBIVTeIc3pP6Z0aA'
}

video_dir = 'videos/'


def video_filter(info, *, incomplete):
    keyword = 'yes'
    title = info.get('title')
    if keyword.lower() not in title.lower():
        return f'The video does not contains {keyword}'


def video_data_collector(response):
    data = (response['id'], response['title'], response['description'])
    print('video_data_collector')
    print(data)


def progress_hook(response):
    if response['status'] == 'finished':
        print(f'You have downloaded {response["filename"]} :D')


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def video_info_extractor(channel_url):
    ydl_opts = {
        'outtmpl': video_dir + '%(upload_date)s %(uploader)s %(title)s.%(ext)s',
        # 'restrictfilenames': True,
        'windowsfilenames': True,
        'format': 'bestvideo[height=1080]+bestaudio[ext=m4a]/bestvideo[height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        # 'download_archive': 'downloaded.txt',
        # 'match_filter': video_filter,
        # 'writethumbnail': True,
        # 'progress_hooks': [progress_hook]
        # 'logger': MyLogger()
    }
    ydl = YoutubeDL(ydl_opts)
    return ydl.extract_info(
        channel_url,
        download=False
    )


def video_downloader(url):
    ydl_opts = {
        'outtmpl': video_dir + '%(upload_date)s %(uploader)s %(title)s %(id)s.%(ext)s',
        'windowsfilenames': True,
        'format': 'bestvideo[height=1080]+bestaudio[ext=m4a]/bestvideo[height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        # 'download_archive': 'downloaded.txt',
        # 'match_filter': video_filter,
        'writethumbnail': True,
        'writedescription': True,
        # 'progress_hooks': [progress_hook]
        # 'logger': MyLogger()
    }
    ydl = YoutubeDL(ydl_opts)
    return ydl.download(
        url
    )
# channel_id TEXT,
#             id TEXT,
#             upload_date INT,
#             title TEXT,
#             description TEXT,
#             views INT,
#             likes INT,
#             downloaded INT,
#             modified_date TEXT
def video_data_fetcher(entry):
    return (
        entry['channel_id'],
        entry['id'],
        entry['upload_date'],
        entry['title'],
        entry['description'],
        entry['view_count'],
        entry['like_count'],
        True,
        str(datetime.now())
    )

PREF_VIDEO_URL = 'https://www.youtube.com/watch?v='

# id
# TEXT,
# name
# TEXT,
# url
# TEXT,
# thumbnail_url
# TEXT,
# added_date
# TEXT

def channel_data_fetcher(entry):
    result = (
        str(entry['channel_id']),
        str(entry['channel']),
        str(entry['channel_url']),
        str(entry['thumbnails'][0]['url']),
        str(datetime.now())
    )
    print(result)
    return result

def channel_manager(channel_url):
    result = video_info_extractor(channel_url)
    if len(db.query_channel(result['channel_id']))==0:
        db.insert_channel(channel_data_fetcher(result))
    for entry in result['entries']:
        if len(db.query_downloaded(entry['id']))==0:
            url = PREF_VIDEO_URL + entry['id']
            video_downloader(url)
            db.insert_video(video_data_fetcher(entry))

def video_manager(url):
    result_video = video_info_extractor(url)
    if len(db.query_channel(result_video['channel_id'])) == 0:
        result = video_info_extractor(result_video['channel_url'])
        db.insert_channel(channel_data_fetcher(result))
    if len(db.query_downloaded(result_video['id'])) == 0:
        video_downloader(url)
        db.insert_video(video_data_fetcher(result_video))

if __name__ == '__main__':
    # db.create_db()
    # video_info_extractor(channels['agustin01 tutoriales'])
    # channel_manager(channels['agustin01 tutoriales'])
    url = 'https://www.youtube.com/watch?v=iAVqvHGi4Fk' #wtf video blue charles
    video_manager(url)