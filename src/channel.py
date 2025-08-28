import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.build_object = build(serviceName='youtube', version='v3', developerKey=os.getenv('API_KEY'))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = json.dumps(self.build_object.channels().list(id=self.channel_id, part='snippet,statistics').execute(),
                             indent=2, ensure_ascii=False)
        print(channel)
