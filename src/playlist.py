from src.channel import BuildObject
from src.video import Video
import datetime


class PlayList(BuildObject):
    def __init__(self, playlist_id: str):
        """
        playlist_id - id плейлиста.
        url - ссылка на плейлист.
        title - название плейлиста.
        videos_info - информация о видео из плейлиста.
        total_duration - общее длительность видео плейлиста.
        best_video - лучшее видео по количеству лайков.
        """
        self.playlist_id = playlist_id
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        self.title = self.build_youtube().playlists().list(id=self.playlist_id,
                                                           part='snippet',
                                                           maxResults=50,
                                                           ).execute()['items'][0]['snippet']['title']

        self.videos_info = self.build_youtube().playlistItems().list(playlistId=self.playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        self._total_duration = datetime.timedelta(0)
        self.best_video = ''
        counter = 0
        # За один цикл обхожу все видео и собираю у них длительность видео и количество лайков.
        for element in self.videos_info['items']:
            self._total_duration += Video(element['contentDetails']['videoId']).duration
            if Video(element['contentDetails']['videoId']).like_count > counter:
                self.best_video = 'https://youtu.be/' + element['contentDetails']['videoId']

    @property
    def total_duration(self):
        return self._total_duration

    def show_best_video(self):
        return self.best_video