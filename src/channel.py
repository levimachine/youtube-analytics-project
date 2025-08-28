import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.build_object = build(serviceName='youtube', version='v3', developerKey=os.getenv('API_KEY'))
        self.json_dict = json.loads(json.dumps(
            self.build_object.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2,
            ensure_ascii=False))
        self.id = self.json_dict['items'][0]['id']
        self.title = self.json_dict['items'][0]['snippet']['title']
        self.description = self.json_dict['items'][0]['snippet']['description'][:-1]
        self.url = 'https://www.youtube.com/' + self.json_dict['items'][0]['snippet']['customUrl']
        self.subscriber_count = self.json_dict['items'][0]['statistics']['subscriberCount']
        self.video_count = self.json_dict['items'][0]['statistics']['videoCount']
        self.view_count = self.json_dict['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = json.dumps(self.build_object.channels().list(id=self.channel_id, part='snippet,statistics').execute(),
                             indent=2, ensure_ascii=False)
        print(channel)

    @classmethod
    def get_service(cls) :
        """Класс метод возвращает объект для работы с YouTube API"""
        return build(serviceName='youtube', version='v3', developerKey=os.getenv('API_KEY'))

    def to_json(self, file_path: str) -> None:
        """
        Метод сохраняет все данные о канале в json файл.
        :param file_path: Имя файла, куда будем сохранять данные.
        """
        json_dict = {
            'id': self.json_dict['items'][0]['id'],
            'title': self.json_dict['items'][0]['snippet']['title'],
            'description': self.json_dict['items'][0]['snippet']['description'][:-1],
            'url': 'https://www.youtube.com/' + self.json_dict['items'][0]['snippet']['customUrl'],
            'subscriber_count': self.json_dict['items'][0]['statistics']['subscriberCount'],
            'video_count': self.json_dict['items'][0]['statistics']['videoCount'],
            'view_count': self.json_dict['items'][0]['statistics']['viewCount'],
        }
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(fp=json_file, obj=json_dict, ensure_ascii=False, indent=3)
