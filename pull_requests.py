from datetime import datetime
from timer import custom_timer

class pull_requests:
    def __init__(self, bot, callback):
        self.bot = bot
        self.offset = 0
        self.timer = custom_timer(2, self.update)
        self.callback = callback

    def update(self):
        response = self.bot.send_request("getUpdates", {"offset":self.offset})
        if(not response): #array is empty
            self.trace("No updates were received")
            return

        self.offset = response[-1]["update_id"] + 1
        self.callback(response)

    def begin_pull(self):
        self.timer.start()

    def stop_pull(self):
        self.timer.stop()

    def trace(self, message):
        print(self.getTime() + " " + message)

    def getTime(self):
        return datetime.now().strftime('[%H:%M:%S]')
