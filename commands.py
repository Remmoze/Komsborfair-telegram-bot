from inlinekeyboard import keyboard
import re

class Commands:
    def __init__(self, bot):
        self.bot = bot
        self.subscribers = {}

    def handle_updates(self, new_updates):
        for update in new_updates:
            if("message" in update):
                self.handle_message(update["message"])
            elif("callback_query" in update):
                self.handle_query(update["callback_query"])
                print("[QUERY]", update)
            else:
                print("[UPDATE]", update)

    def handle_photo_update(self, user_id, message):
        file_id = ""
        is_photo = False
        if("photo" in message):
            self.bot.reply(user_id, "Качество фото будет лучше, если вы отправите его файлом, а не фотографией!")
            file_id = message["photo"][0]["file_id"]
            is_photo = True
        
        if("document" in message):
            file_id = message["document"]["file_id"]
            is_photo = False
        
        product = self.bot.storage.get_or_create_pending_product(user_id)
        product.file_id = file_id
        product.is_file_a_photo = is_photo

        self.bot.reply(user_id, "Фотография продукта была изменена!")
        self.bot.reply_default(user_id)

    def handle_message(self, message):
        user_id = message["from"]["id"]

        if("photo" in message or "document" in message):
            self.handle_photo_update(user_id, message)
            return

        text = ""
        if("text" in message):
            text = message["text"]
        
        print("[MESSAGE FROM " + str(user_id) + "]", message)

        if(text.startswith('/')):
            self.handle_command(user_id, text)
        else:
            self.handle_subscribers(user_id, text)

    def handle_command(self, user_id, command):
        product = self.bot.storage.get_or_create_pending_product(user_id)
        if(command == "/create" or command == '/start'):
            if(not product.empty):
                self.prompt_to_create_new(user_id)
                return
            self.bot.create_new_product(user_id)
        elif(command == "/Оставить этот."):
            self.bot.reply_default(user_id)
        elif(command == "/Новый товар"):
            self.bot.create_new_product(user_id)
        elif(command == "/Отправить!"):
            self.bot.reply(user_id, "потом доделаю")
            self.bot.create_new_product(user_id)
        else:
            if(command == "/Изменить название товара"):
                self.subscribe_to_message(user_id, "title")
                self.bot.reply(user_id, "Введите новое описание:")
            elif(command == "/Изменить количество товара"):
                self.subscribe_to_message(user_id, "amount")
                self.bot.reply(user_id, "Введите новое количество:")
            elif(command == "/Изменить короткое описание"):
                self.subscribe_to_message(user_id, "short_disc")
                self.bot.reply(user_id, "Введите короткое описание:")
            elif(command == "/Изменить описание"):
                self.subscribe_to_message(user_id, "disc")
                self.bot.reply(user_id, "Введите описание (не больше 140 символов!):")
            elif(command == "/Изменить фотографию"):
                self.bot.reply(user_id, "Пришлите новую фотографию, лучше документом!")

    def handle_subscribers(self, user_id, text):
        if(not user_id in self.subscribers):
            self.bot.reply(user_id, "Не уверен что вы имели ввиду!")
            self.bot.reply_default(user_id)
            return

        text = re.escape(text)

        product = self.bot.storage.get_or_create_pending_product(user_id)
        variable = self.subscribers[user_id]
        if(variable == "title"):
            product.title = text
            self.bot.reply(user_id, "Название именено: " + text)
        elif(variable == "amount"):
            product.amount = text
            self.bot.reply(user_id, "Количество именено: " + text)
        elif(variable == "short_disc"):
            product.short_discription = text
            self.bot.reply(user_id, "Количество именено: " + text)
        elif(variable == "disc"):
            product.discription = text
            self.bot.reply(user_id, "Количество именено: " + text)            
            
        del self.subscribers[user_id]
        self.bot.reply_default(user_id)
        
    def subscribe_to_message(self, user_id, variable_name):
        self.subscribers[user_id] = variable_name

    def prompt_to_create_new(self, user_id):
        kb = keyboard()
        kb.add_button("/Новый товар") #Create New File
        kb.add_button("/Оставить этот.") #Keep Current Fle

        self.bot.send_request("sendMessage", {
            "chat_id": user_id,
            "text": "Вы уверены, что хотите открыть новый файл? Текущий будет удален.",
            "reply_markup": kb.build()
        })

