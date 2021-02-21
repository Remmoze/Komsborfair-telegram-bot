import json

class keyboard:
    def __init__(self):
        self.buttons = []

    def add_button(self, text):
        button = {"text":text}
        self.buttons.append(button)

    def build(self):
        #ReplyKeyboardMarkup
        return json.dumps({
            "keyboard": [self.buttons],
            "one_time_keyboard": True
        })

    