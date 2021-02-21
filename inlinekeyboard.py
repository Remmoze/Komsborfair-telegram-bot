import json

class keyboard:
    def __init__(self):
        self.buttons = []

    def add_button(self, text, callbackinfo):
        button = {
            "text":text,
            "callback_data": callbackinfo
        }
        self.buttons.append(button)

    def build(self):
        return json.dumps({"inline_keyboard": [self.buttons]})

    