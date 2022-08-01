from yt_dlp import YoutubeDL

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


def video_extractor(channel_url):
    ydl_opts = {
        'outtmpl': video_dir + '%(upload_date)s %(uploader)s %(title)s.%(ext)s',
        # 'restrictfilenames': True,
        'windowsfilenames': True,
        'format': 'bestvideo[height=1080]+bestaudio[ext=m4a]/bestvideo[height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        'download_archive': 'downloaded.txt',
        # 'match_filter': video_filter,
        'writethumbnail': True,
        'progress_hooks': [progress_hook]
        # 'logger': MyLogger()
    }
    ydl = YoutubeDL(ydl_opts)
    return ydl.extract_info(
                        channel_url,
                        download=True
                        )

if __name__ == '__main__':
    db.create_db()
    video_extractor(channels['agustin01 tutoriales'])

