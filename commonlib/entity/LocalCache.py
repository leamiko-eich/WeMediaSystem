#encoding=utf-8
## 本地缓存，去重处理
import os

class LocalCache(object):
    def __init__(self, path_config):
        self.path_config = path_config

        # if not os.path.exists(path_config):
#            文件夹不存在，创建文件夹
            # os.makedirs(path_config)

        self.processed_files = set()
        # 读取配置文件，获取已处理的文件列表
        if os.path.exists(self.path_config):
            with open(self.path_config, 'r', encoding='utf-8') as f:
                self.processed_files = set(f.read().splitlines())


    def is_in_cache(self, line):

        if line in self.processed_files :
            # 如果文件已处理过，则跳过
            return True
        return False


    def persist_cache(self, line):
        with open(self.path_config, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

