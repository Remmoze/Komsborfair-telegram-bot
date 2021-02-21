from bot import Telegram_Bot

fs = open("token.config", "r", encoding='utf-8')
token = fs.read()
fs.close()

lala = Telegram_Bot(token)
resp = lala.validate()

print()

lala.start()
