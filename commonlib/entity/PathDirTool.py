#encoding=utf-8
import os

class PathDirTool(object):
    def __init__(self):
        pass

    def create_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

            
if __name__ == "__main__":
    obj = PathDirTool()
    obj.create_dir("data")