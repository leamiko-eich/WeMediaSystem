#encoding=utf-8
from multiprocessing import Process
import time
import os
import subprocess

class BackgroudTask(object):
    def __init__(self):
        pass


    def background_scrawl(self):
        curpath=os.getcwd()
        parentpath = os.path.dirname(curpath)
        dir_crawl = os.path.join(parentpath, "scrawl")
        print("curpath:",curpath, parentpath, dir_crawl)
        os.chdir(dir_crawl)
        print("newpath:", os.getcwd())


        command = ' sh back_crawl_zhihu.sh'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        print(result.stdout)
        print(result.stderr)
        print("end back")



        # for i in range(5):
            # time.sleep(1)
            # print("wait", i)


    def start_scrawl(self):
        print("start scrwl")
        p = Process(target=self.background_scrawl)
        p.start()
        print("end scrwl")
