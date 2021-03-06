import requests
from pull_requests import pull_requests
from storage import Storage
from commands import Commands
from inlinekeyboard import keyboard

class Telegram_Bot:
    def __init__(self, token):
        self.token = token
        self.storage = Storage()
        self.CommandHandler = Commands(self)
        self.pulls = pull_requests(self, self.CommandHandler.handle_updates)

    def validate(self):
        return self.send_request("getMe")

    def start(self):
        self.pulls.begin_pull()

    def send_request(self, method, params = {}):
        print("[REQUEST]", method, params)

        url = "https://api.telegram.org/bot" + self.token + "/" + method
        response = requests.get(url, params).json()
        if(not response["ok"]):
            print("[ERROR]: ", response)
            raise Exception("Invalid Response")
        return response["result"]

    def reply(self, user_id, message):
        print("[MESSAGE TO", str(user_id), "]", message)
        self.send_request("sendMessage", {
            "chat_id": user_id,
            "text": message
        })

    def reply_with_product(self, user_id, message):
        print("[MESSAGE TO", str(user_id), "]", message)
        self.send_request("sendMessage", {
            "chat_id": user_id,
            "text": message,
            "parse_mode": "MarkdownV2"
        })

    def create_new_product(self, user_id):
        self.reply(user_id, "Создаю новый файл..")
        self.storage.create_new_pending_product(user_id)

        self.reply_default(user_id)

    def reply_default(self, user_id):
        kb = keyboard()
        kb.add_button("/Новый товар")
        kb.add_button("/Изменить название товара")
        kb.add_button("/Изменить количество товара")
        kb.add_button("/Изменить короткое описание")
        kb.add_button("/Изменить описание")
        kb.add_button("/Изменить фотографию")
        kb.add_button("/Отправить!")

        product = self.storage.get_or_create_pending_product(user_id)

        self.send_request("sendMessage", {
            "chat_id": user_id,
            "text": product.print(),
            "parse_mode": "MarkdownV2",
            "reply_markup": kb.build()
        })



