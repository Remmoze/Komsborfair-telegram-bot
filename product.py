import json
from pprint import pprint

class Product:
    def __init__(self):
        self.__title = ""
        self.__image_name = ""
        self.__short_discription = ""
        self.__discription = ""

        self.empty = True
        self.identifier = ""

    def print(self):
        return f"""*{self.title if self.title else 'no title'}*
Описание: *{self.discription if self.discription else 'no discription'}*
ID: *{self.identifier if self.identifier else 'no id'}*
"""

    def import_json(self, json_file):
        print(json.loads(json_file))

    def export_json(self):
        json_object = json.dumps({
            "identifier": self.identifier,
            "title": self.title,
            "image_name": self.image_name,
            "discription": self.discription,
            "empty": self.empty
        })
        return json_object

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.empty = False
        self.__title = value

    @property
    def short_discription(self):
        return self.__short_discription

    @short_discription.setter
    def short_discription(self, value):
        self.empty = False
        self.__short_discription = value

    @property
    def discription(self):
        return self.__discription

    @discription.setter
    def discription(self, value):
        self.empty = False
        self.__discription = value

