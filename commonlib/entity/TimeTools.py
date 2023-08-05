#encoding=utf-8
import datetime
import random
import hashlib

class TimeTools(object):
    def __init__(self) -> None:
        self.now = datetime.datetime.now()

    def get_current_day(self):
        today = datetime.datetime.today()
        return today.strftime("%Y-%m-%d")

    def get_md5_sum(self, data):
        data_bytes = data.encode('utf-8') 
        m = hashlib.md5()
        m.update(data_bytes)
        md5_value = m.hexdigest()
        return md5_value


    def get_current_hour(self):
        return self.now.hour

    def get_current_minute(self):
        return self.now.minute

    def get_current_day_hour(self):
        date_hour_str = self.now.strftime("%Y-%m-%d %H")
        return date_hour_str

    def get_current_day_hour_minute(self):
        self.now = datetime.datetime.now()
        date_hour_str = self.now.strftime("%Y-%m-%d %H:%M")
        return date_hour_str



    def get_current_hour(self):
        return self.now.hour

    def get_day_after(self, days):
        today = datetime.datetime.today()
        return (today + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

    def get_random_number(self, start=0, end=1000):
        random_num = random.randint(start, end)
        return random_num

    def get_random_time_flag(self):
        random_num = self.get_random_number()
        day_hour = self.get_current_day_hour_minute()
        ret = "%s_%s" % (day_hour, random_num)
        return ret