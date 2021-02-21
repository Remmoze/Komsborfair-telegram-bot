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

    def handle_message(self, message):
        user_id = message["from"]["id"]
        text = message["text"]
        
        print("[MESSAGE FROM " + str(user_id) + "]", text)

        if(text.startswith('/')):
            self.handle_command(user_id, text)
        else:
            pass
    
    def handle_query(self, query):
        user_id = query["from"]["id"]
        product = self.bot.storage.get_or_create_pending_product(user_id)
        command = query["data"]
        if(command == "KCF"):
            self.bot.print_current_product(user_id)
        elif(command == "CNF"):
            self.bot.create_new_product(user_id)
    
    def handle_command(self, user_id, command):
        if(command == "/create"):
            product = self.bot.storage.get_or_create_pending_product(user_id)
            if(not product.empty):
                self.prompt_to_create_new(user_id)
                return
            self.bot.create_new_product(user_id)

    def prompt_to_create_new(self, user_id):
        kb = keyboard()
        kb.add_button("Новый.", "CNF") #Create New File
        kb.add_button("Оставить этот.", "KCF") #Keep Current Fle

        self.bot.send_request("sendMessage", {
            "chat_id": user_id,
            "text": "Вы уверены, что хотите открыть новый файл? Текущий будет удален.",
            "reply_markup": kb.build()
        })

