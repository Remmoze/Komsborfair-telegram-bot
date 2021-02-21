import requests
from pull_requests import pull_requests
from storage import Storage
from pprint import pprint
from inlinekeyboard import keyboard

class Telegram_Bot:
    def __init__(self, token):
        self.token = token
        self.pulls = pull_requests(self, self.updates)
        self.storage = Storage()

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

    def updates(self, new_updates):
        for update in new_updates:
            if("message" in update):
                self.__handle_message(update["message"])
            elif("callback_query" in update):
                self.__hangle_button(update["callback_query"])
                print("[QUERY]", update)
            else:
                print("[UPDATE]", update)

    def __handle_message(self, message):
        user_id = message["from"]["id"]
        text = message["text"]

        print("[MESSAGE FROM " + str(user_id) + "]", text)

        product = self.storage.create_or_get_pending_product(user_id)

        if(text.startswith("/create")):
            if(not product.empty):
                self.prompt_to_create_new(user_id)
                return
            self.reply_with_product(user_id, product.print())

    def __hangle_button(self, callback_query):
        user_id = callback_query["from"]["id"]
        product = self.storage.create_or_get_pending_product(user_id)
        command = callback_query["data"]
        if(command == "KCF"):
            self.reply_with_product(user_id, product.print())
        elif(command == "")

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

    def prompt_to_create_new(self, user_id):
        kb = keyboard()
        kb.add_button("Новый", "CNF") #Create New File
        kb.add_button("Оставить этот", "KCF") #Keep Current Fle

        self.send_request("sendMessage", {
            "chat_id": user_id,
            "text": "Вы уверены, что хотите начать открыть новый файл? Текущий будет удален. ",
            "reply_markup": kb.build()
        })

