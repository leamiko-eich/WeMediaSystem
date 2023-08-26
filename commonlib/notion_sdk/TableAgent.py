#encoding=utf-8
from NotionSDK import NotionSDK
import pprint

dic_tablename_dbid ={
    "promote_ku": "f212596c26fd460399f462d769a63a6e",
    "recall_art": "e0a48b98591641f182ddebe9cbec86e6",
    "db_target_author": "ef791fae5bda44baa1ee9c17f47d2b0c"
    
}
dic_tokenname_token = {
    "notion_py_api": "secret_rID6dwpwPn2faXesd0jguXgdayYEoeC3gLLWKHahJ0h",
    "chat_model_api":"secret_SeogxQfRyY50ukWzMJPWwPo4cYjHdYOvOfJ92fFwgh6" ,
    "wemedia_py_api": "secret_JjTQJvIxkJrvGT7dBXfNw1HZVTPWJkd5xxMOQS3m1zq"
}

class TableAgent(object):
    ## 抽象出1个类，管理notion的table
    ## 直接根据key-value的形式，读取notion的table
    def __init__(self, tablename="", token_name="notion_py_api", primary_key_name=""): 
        assert(tablename in dic_tablename_dbid)
        assert(token_name in dic_tokenname_token)

        self.db_id = dic_tablename_dbid[tablename]
        self.token = dic_tokenname_token[token_name] 
        self.notion_sdk = NotionSDK(tokenName=token_name)

        self.dic_primarykey_item = {}
        self.table_schema = {}

        self.get_table_schema()


    def get_table_schema(self):
        table_schema = self.notion_sdk.get_table_schema(self.db_id)
        self.table_schema = table_schema
        return table_schema

    def get_all_kv_items_by_filter(self, dic_select={}, dic_checkbox={}, dic_datetime={}, list_property=[]):
        payload = None
        dic_select = dic_select
        dic_checkbox = dic_checkbox
        dic_datetime = dic_datetime
        list_property = list_property
        ret_json = self.notion_sdk.dataBase_filter_select_item(self.db_id, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, dic_datetime=dic_datetime, 
                                                       list_property=list_property, fname_out='db_config_with_filter.json')
        ret_dict = self.notion_sdk.convert_notionJson_to_dict(ret_json)

        return ret_dict

    def get_all_line_with_kv_filter(self, kv_filter):
        payload = None
        dic_select = {}
        dic_checkbox = {}
        dic_datetime = {}
        list_property = {}
        for key, value in kv_filter.items():
            vtype = self.table_schema[key]
            if vtype == "select":
                dic_select[key] = value
            elif vtype  == "checkbox":
                dic_checkbox[key] = value
            elif vtype == "datetime":
                dic_datetime[key] = value
            
        ret_json = self.notion_sdk.dataBase_filter_select_item(self.db_id, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, dic_datetime=dic_datetime, 
                                                       list_property=list_property, fname_out='db_config_with_filter.json')
        ret_dict = self.notion_sdk.convert_notionJson_to_dict(ret_json)
        return ret_dict


    def insert_notiondb_item(self, dic_kv):
        # list_columns = [
            #  ["title","title","1122",""] ,
            #  ["select","website","wechat",""] ,
            # ["checkbox","F_Select",True,""],
            # ["multi_select","seg_list",["x","y","z"],""]
        # ]
        list_columns=[]
        for key, value in dic_kv.items():
            assert(key in self.table_schema)
            list_columns.append([self.table_schema[key], key, value, ""])

        ret_json = self.notion_sdk.add_new_row_in_crawl_db(self.db_id, list_columns)
        # print("ret_json:%s" % (ret_json))
        return ret_json

    def modify_notiondb_item(self, dic_kv):
        list_columns=[]
        row_id = dic_kv["row_id"]
        for key, value in dic_kv.items():
            if key=="row_id": continue
            # assert(key in self.table_schema)
            list_columns.append([self.table_schema[key], key, value, ""])

        ret_json = self.notion_sdk.update_db_row_content(row_id, list_columns)
        return ret_json

    
    

if __name__=="__main__":
    flag_get_schema = True
    flag_test_add_line = False
    flag_test_modify_line = False
    flag_test_get_line_with_kv_filter = False

    # agent = TableAgent(tablename="promote_ku", token_name="notion_py_api")
    agent = TableAgent(tablename="db_target_author", token_name="wemedia_py_api")
    # list_kv_item = agent.get_all_kv_items_by_filter()
    # for kv in list_kv_item:
        # print(kv)
    # exit(0)

    if flag_get_schema:
        ret=agent.get_table_schema()
        print(ret)

    if flag_test_add_line:
        dic_kv = {
            "group_prompt": "2",
            "tag_prompt": "test",  
            "prompt_info": "11"
        }
        agent.insert_notiondb_item(dic_kv)
    
    if flag_test_modify_line:
        dic_kv = {
            "row_id": "072cd7f119b141c394cae406be197756"  ,
            "tag_prompt": "test2",  
            "prompt_info": "11999"
        }
        agent.modify_notiondb_item(dic_kv)

    if flag_test_get_line_with_kv_filter:
        dic_kv = {
            # "tag_prompt": "test2",    
            "content_category": "技术"
        }
        ret= agent.get_all_kv_items_by_filter(dic_kv)
        print(ret)
    