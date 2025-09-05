from src.channel import build, os
import isodate


class Video:
    def __init__(self, video_id: str) -> None:
        """
        video_id - id видео.
        build_youtube - объект для работы с Youtube API.
        json_dict - словарь со всеми данными о видео.
        video_name - название видео.
        url_video - ссылка на видео.
        view_count - количество просмотров.
        like_count - количество лайков.
        """
        self.video_id = video_id
        self.build_youtube = build(serviceName='youtube', version='v3', developerKey=os.getenv('API_KEY'))
        self.json_dict = self.build_youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.video_id).execute()
        try:
            self.title = self.json_dict['items'][0]['snippet']['localized']['title']
        except IndexError:
            self.title = None
            self.url_video = None
            self.view_count = None
            self.like_count = None
            self.duration = None
        else:
            self.url_video = 'https://youtu.be/' + self.video_id
            self.view_count = self.json_dict['items'][0]['statistics']['viewCount']
            self.like_count = int(self.json_dict['items'][0]['statistics']['likeCount'])
            self.duration = isodate.parse_duration(self.json_dict['items'][0]['contentDetails']['duration'])

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        playlist_id - id плейлиста
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
