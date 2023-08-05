#encoding=utf-8
import os
import json

class LocalKV(object):
    def __init__(self, path_kv):
        self.path_kv = path_kv
        self.dic_kv ={}

        if not os.path.exists(path_kv):
            # 将字典保存为 JSON 文件
            with open(path_kv, 'w', encoding='utf-8') as file:
                json.dump(self.dic_kv, file, indent=4, sort_keys=True)

        self.load_kv()

    def insert_key_value(self, key, value):
        self.dic_kv[key] = value 

    def has_key(self, key):
        return key in self.dic_kv

    def get_value_by_key(self, key):
        assert(key in self.dic_kv)
        return self.dic_kv[key]

    def persist_kv(self):
        with open(self.path_kv, 'w', encoding='utf-8') as file:
            json.dump(self.dic_kv, file, indent=4)

    def load_kv(self):
        with open(self.path_kv, 'r', encoding='utf-8') as file:
            self.dic_kv = json.load(file)
        return self.dic_kv
        
            



if __name__ == "__main__":
    local_kv = LocalKV("kv.json")

    dic_kv = {
        "a":1,
        "b":2
    }


    print (local_kv.load_kv() )
    local_kv.insert_key_value("d", "dds")
    local_kv.persist_kv()
    print (local_kv.load_kv() )
