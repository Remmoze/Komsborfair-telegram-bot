import json
from pprint import pprint

class Product:
    def __init__(self):
        self.title = ""
        self.file_id = ""
        self.is_file_a_photo = False
        self.short_discription = ""
        self.discription = ""
        self.identifier = ""

    def print(self):
        return f"""*{self.title if self.title else 'no title'}*
Описание: *{self.discription if self.discription else 'no discription'}*
ID: *{self.identifier if self.identifier else 'no id'}*
"""

    @property
    def empty(self):
        return False if self.title or self.file_id or self.short_discription or self.discription else True
            
