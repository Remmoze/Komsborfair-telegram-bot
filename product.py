import json
from pprint import pprint

class Product:
    def __init__(self, identifier = "", title = "", image_name = "" , discription = ""):
        self.identifier = identifier
        self.title = title
        self.image_name = image_name
        self.discription = discription
        self.empty = True

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

