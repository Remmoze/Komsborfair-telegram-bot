import json
from pprint import pprint

class Product:
    def __init__(self):
        self.title = ""
        self.amount = ""
        self.file_id = ""
        self.is_file_a_photo = False
        self.short_discription = ""
        self.discription = ""
        self.identifier = ""

    def print(self):
        return f"""*{self.title if self.title else 'Нет названия'}*
Количество: *{self.amount if self.amount else 'Нет количества'}*
Коротое описание: *{self.short_discription if self.short_discription else 'Нет описания'}*
Описание: *{self.discription if self.discription else 'Нет описания'}*
Фото: *{"Добавлено" if self.file_id else 'Нет фото'}*
"""

    @property
    def empty(self):
        return False if self.title or self.amount or self.file_id or self.short_discription or self.discription else True
            
