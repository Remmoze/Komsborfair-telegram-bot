from threading import Timer,Thread,Event

class custom_timer:
    def __init__(self, interval, callback, startRunning = False):
        self.running = False

        self.callback = callback
        self.interval = interval

        self.__setupTimer()

    def __setupTimer(self):
        self.thread = Timer(self.interval, self.__handle_time)

    def __handle_time(self):
        self.callback()
        self.__setupTimer()
        if(self.running):
            self.start()

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.cancel()