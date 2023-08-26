#encoding=utf-

from NotionSDK import NotionSDK

def test_page():
    ## ===============  页面测试
    # page_id = '584bc1d8a42743acb5ef239230fe2340'
    page_id = '0a480e5de6494b0b8e06f0965b1d613f'
    # notion_sdk.delete_page(page_id)
    # notion_sdk.page_query(page_id)
    # notion_sdk.retrieve_block_children(page_id)
    title = "你好123"
    list_content = [
        "#原始文案", 
        "dou shi zheyangde",
        "##爆款标题", 
        "wei shenme"
    ]
    page_id = '853434a03b1f42afa6b264aad36e905a'

    def split_content(content, n):
        return [content[i:i+n] for i in range(0, len(content), n)]
    list_content = []
    content = ""
    with open("1.txt", "r", encoding='utf-8') as f:
        content = f.read()
    print("len: %d" % (len(content)))
    with open("1.txt", "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip(" ").strip("\n")
            if len(line)< 1500:
                list_content.append(line)
            else:
                new_line_list = split_content(line, 1500)
                list_content.extend(new_line_list)

    
    # print(list_content)
    # new_page_id = notion_sdk.create_page(page_id, title, list_content)
    # print("new_page_id:", new_page_id)

    page_id = '0a480e5de6494b0b8e06f0965b1d613f'
    # notion_sdk.append_block_children(page_id, "2.txt")



def test_database():
    ## 测试开关
    flag_download_db_content = True
    flag_test_select_line_from_db = False
    flag_download_schema_in_db = False
    flag_test_add_newrow_in_db = False
    flag_test_convert_notionjson_to_dict =True
    flag_test_update_db_row_content = False
    flag_add_column_to_db = False
    flag_delete_row_in_db = False
    flag_clear_database = False
    ## ================ 数据库测试
    database_id = '28367fb4d8764685a00196d0158780be'
    database_id = '2436017bd910428a9259a302baa9ae8c'


    database_id = 'cd505d04eab84ef7ac3ad249a50a8319' ## 正式数据库
    # database_id = 'be3be9587924459ab573eec02918dc5f' ## config配置
    database_id = '7f863dd9221844179e047825b57e8a58' ## 爬虫文章数据库
    database_id = '4fd530b46946419cae8ce0e86f82d2d0' ## 爬虫配置数据库
    database_id = 'efd32c79509c4bcaa05fe1e913506af0' ## 热点分割
    # database_id = '899c6a175fcd4e088c23a42de3a9ca98' ## write_skill_db
    # database_id = '5644a7cbf23347f3938a54c3fc05a9e7' ## daily_write_db
    database_id = '28285c424d284bfc8f45e48192541163' ## dispatch db
    
    # 查询数据库-全部内容
    if flag_download_db_content:
        ret_json = notion_sdk.dataBase_item_query(database_id, 'db_config.json')
    if flag_delete_row_in_db:
        row_id = '9cd33fd01b7f4dad9337ba042a487b5a'
        row_id = '27e7a15908c645dea504d09cd0198c10'
        notion_sdk.delete_row_in_notion_database(row_id)
    if flag_clear_database:
        notion_sdk.clear_database(database_id)
    if flag_test_update_db_row_content:
        # row_id = 'ddca66e724e94067ba644c73c77259fe'
        # row_id = '096415bd2f5643579d316d4634cd0175'
        list_columns = [
            #  ["rich_text","new_scrawl_date","2023-07-09 02",""] ,
             ["date","update_date","2023-05-07",""] ,
        ]
        ret_json = notion_sdk.update_db_row_content(row_id, list_columns)
    if flag_add_column_to_db:
        notion_sdk.add_column_to_notion_database(database_id, 'recall_date')
    if flag_download_schema_in_db:
        ret = notion_sdk.has_column_in_notion_database(database_id, 'recall_date')
        print("ret:", ret)
    # 查询部分内容
    if flag_test_select_line_from_db:
        payload = None
        dic_select = {}
        dic_checkbox = {}
        dic_datetime = {"before|update_date":"2023-06-01"}
        list_property = []
        ret_json = notion_sdk.dataBase_filter_select_item(database_id, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, dic_datetime=dic_datetime, 
                                                       list_property=list_property, fname_out='db_config_with_filter.json')
    if flag_test_add_newrow_in_db:
        list_columns = [
             ["title","title","1122",""] ,
            #  ["select","category","政治",""] ,
             ["select","website","wechat",""] ,
            #  ["select","author","yjf2",""] ,
            #  ["rich_text","art_link","www.baidu.com",""] ,
            ["checkbox","F_Select",True,""],
            ["multi_select","seg_list",["x","y","z"],""]
        ]
        ret_json = notion_sdk.add_new_row_in_crawl_db(database_id, list_columns)
    if flag_test_convert_notionjson_to_dict:
        # ret_json = notion_sdk.dataBase_item_query(database_id, 'db_config.json')
        ret_dict = notion_sdk.convert_notionJson_to_dict(ret_json)
        print(ret_dict)
    # 查询数据库，并且带有过滤条件
    # payload = None
    # dic_select = {'config_select':'auto_gen'}
    # dic_select = {'doc_stage':'07pre_publish'}
    # dic_checkbox = {'status':True}
    # list_property = ['config_select']
    # json_data = notion_sdk.dataBase_filter_select_item(database_id, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, 
                                                    #    list_property=list_property, fname_out='db_config_with_filter.json')
# 
    # dic_checkbox = {'FinalSelect':True}
    # json_data = notion_sdk.dataBase_filter_select_item(database_id, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, 
                                                    #    list_property=list_property, fname_out='db_config_with_filter.json')
# 
    # title = "title2"
    # page_link = "http://www.baidu.com"
    # notion_sdk.add_new_row_in_db(database_id, title, page_link)


    # page_id = 'df1ea4e1ae474129bc0e102505397c3e'
    

    # notion_sdk.retrieve_block_children(page_id)






if __name__== '__main__':
    notion_sdk = NotionSDK()

    test_database()
