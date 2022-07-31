from yt_dlp import YoutubeDL

channels = {
    'agustin01 tutoriales': 'https://www.youtube.com/channel/UCOARbH8Vn6aacb8JQgpfEaw',
    'agustin01 canciones': 'https://www.youtube.com/channel/UCq9r1AmRBIVTeIc3pP6Z0aA'
}

video_dir = 'videos/'

def video_extractor(channel_url):
    ydl_opts = {
        'outtmpl': video_dir + '%(upload_date)s %(uploader)s %(title)s.%(ext)s',
        'restrictfilenames': True,
        'format': 'bestvideo[height=1080]+bestaudio[ext=m4a]/bestvideo[height=720]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
        'download_archive': 'downloaded.txt'
    }
    ydl = YoutubeDL(ydl_opts)
    return ydl.extract_info(
                        channel_url,
                        download=True
                        )

if __name__ == '__main__':
    print(video_extractor(channels['agustin01 tutoriales']))

