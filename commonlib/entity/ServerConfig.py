#encoding=utf-8


class ServerConfig(object):
    def __init__(self):
        self.min_gap_hour = 6

        self.mode = "dev"

    def set_mode(self, mode):
        self.mode = mode

    def set_url(self, url):
        self.url = url

    def set_page_num(self, page_num):
        self.page_num = page_num