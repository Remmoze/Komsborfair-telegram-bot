from bot import Telegram_Bot

fs = open("token.config", "r", encoding='utf-8')
token = fs.read()
fs.close()

lala = Telegram_Bot(token)
response = lala.validate()

print("\nBOT - [" + str(response["id"]) + "] " + response["first_name"] + '\n')

lala.start()
