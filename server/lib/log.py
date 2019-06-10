from datetime import datetime

class Log():
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod 
    def log(msg):
        print("%s : %s", (Log.timestamp(), str(msg)))

