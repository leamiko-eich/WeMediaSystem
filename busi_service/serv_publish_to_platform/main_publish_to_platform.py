#encoding=utf-8
import os,sys
ROOTDIR_WeMediaSystem = os.getenv('ROOTDIR_WeMediaSystem')
os.chdir(ROOTDIR_WeMediaSystem)
sys.path.append(ROOTDIR_WeMediaSystem)

from commonlib.entity import set_my_log
from PublishAgent import PublishAgent

if __name__ == "__main__":
    set_my_log("log_publish.log")
    PublishAgent().start_flow()