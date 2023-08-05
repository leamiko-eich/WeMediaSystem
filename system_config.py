#encoding=utf-8
## 1. 引入包
## 2. 输入开关
import sys 
import os

import os,sys
if not os.path.exists("log"):
    os.makedirs("log")

rootDirName = "WeMediaSystem"


def get_is_linux():
    is_linux = False
    if sys.platform.startswith('win'):
        # 当前系统是 Windows
        is_linux = False
        print("[当前系统] windows")
    elif sys.platform.startswith('linux'):
        # 当前系统是 Linux
        print("[当前系统] linux")
        is_linux = True
    else:
        # 其他操作系统
        print("其他操作系统")
    return is_linux

def find_root_directory():
    # 获取当前目录路径
    current_directory = os.getcwd()

    # 从当前目录开始逐级向上遍历父目录，直到找到名为'mymedia'的目录
    while True:
        parent_directory = os.path.dirname(current_directory)
        if os.path.basename(current_directory) == rootDirName:
            return current_directory
        elif current_directory == parent_directory:
            # 已经到达根目录，但没有找到'mymedia'目录
            raise FileNotFoundError("Could not find the root directory named '%s'." % (rootDirName))
        else:
            current_directory = parent_directory




def set_system_path(is_linux):
    curpath=os.getcwd()
    curpath=os.path.dirname(os.path.abspath(__file__))
    os.chdir(curpath)
    rootdir = os.path.dirname(curpath)
    print("curpath:%s\t rootdir:%s"%(curpath, rootdir))
    if is_linux:
        sys.path.append("%s"%(rootdir))
        sys.path.append("%s/mygpt"%(rootdir))
        sys.path.append("%s/commonlib"%(rootdir))
        sys.path.append("%s/commonlib/entity"%(rootdir))
        sys.path.append("%s/win_automation/notion_automation"%(rootdir))
    else:
        sys.path.append("%s"%(rootdir))
        sys.path.append("%s\\mygpt"%(rootdir))
        sys.path.append("%s\\commonlib"%(rootdir))
        sys.path.append("%s\\commonlib\\entity"%(rootdir))
        sys.path.append("%s\\win_automation\\notion_automation"%(rootdir))

is_linux = get_is_linux()
root_directory = find_root_directory()
print("root_directory:%s"%(root_directory))
set_system_path(is_linux)