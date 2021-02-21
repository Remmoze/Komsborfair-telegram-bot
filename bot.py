import requests
from pull_requests import pull_requests
from storage import Storage
from commands import Commands

class Telegram_Bot:
    def __init__(self, token):
        self.token = token
        self.storage = Storage()
        self.CommandHandler = Commands(self)
        self.pulls = pull_requests(self, self.CommandHandler.handle_updates)

    def validate(self):
        response = self.send_request("getMe")
        print("BOT - [" + str(response["id"]) + "] " + response["first_name"])

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

        self.print_current_product(user_id)

    def print_current_product(self, user_id):
        product = self.storage.get_or_create_pending_product(user_id)
        self.reply_with_product(user_id, product.print())


