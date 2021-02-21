from inlinekeyboard import keyboard

class Commands:
    def __init__(self, bot):
        self.bot = bot

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
        if("photo" in message):
            self.bot.reply(user_id, "Качество фото будет лучше, если вы отправите его файлом, а не фотографией!")
            file_id = message["photo"][0]["file_id"]
        
        if("document" in message):
            file_id = message["document"]["file_id"]
        
        response = self.bot.send_request("getFile", {"file_id": file_id})
        path = response["file_path"]
        file_format = path.split('.')[-1]
        image = self.bot.getFile(path)

        fs = open(str(user_id) + "." + file_format, "wb")
        fs.write(image)
        fs.close()

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
            pass

    def handle_command(self, user_id, command):
        if(command == "/create"):
            product = self.bot.storage.get_or_create_pending_product(user_id)
            if(not product.empty):
                self.prompt_to_create_new(user_id)
                return
            self.bot.create_new_product(user_id)
        elif(command == "/Оставить этот."):
            self.bot.print_current_product(user_id)
        elif(command == "/Новый."):
            self.bot.create_new_product(user_id)

    def prompt_to_create_new(self, user_id):
        kb = keyboard()
        kb.add_button("/Новый.") #Create New File
        kb.add_button("/Оставить этот.") #Keep Current Fle

        self.bot.send_request("sendMessage", {
            "chat_id": user_id,
            "text": "Вы уверены, что хотите открыть новый файл? Текущий будет удален.",
            "reply_markup": kb.build()
        })

