#encoding=utf-8
import json
import urllib.parse
import time
import pprint


import requests

# notion基本参数
# headers = {
    # 'Notion-Version': '2022-06-28',
    # 'Authorization': 'Bearer '+token,
# }

from NotionBlock import NotionBlock

class NotionSDK(object):
    def __init__(self, tokenName = ""):
        self.session = requests.Session()
        self.notion_block = NotionBlock()
        self.waittime_notion = 1

        
        token = 'secret_rID6dwpwPn2faXesd0jguXgdayYEoeC3gLLWKHahJ0h'
        token_chat_model_api = 'secret_SeogxQfRyY50ukWzMJPWwPo4cYjHdYOvOfJ92fFwgh6'
        if tokenName == 'token_chat_model_api':
            token = token_chat_model_api
        self.token = token   
        self.headers = {
            'Notion-Version': '2021-05-13',
            "Content-Type": "application/json",
            'Authorization': 'Bearer '+token
        }

    def get_table_schema(self, db_id):
        api_url = 'https://api.notion.com/v1/databases/%s' % (db_id)
        response = self.session.get(api_url, headers=self.headers)

        if response.status_code == 200:
            # Parse the response JSON to get the database schema
            schema = response.json()['properties']

            dic_schema = {}
            for key, value in schema.items():
                v_type = value['type']
                dic_schema[key] = v_type
            return dic_schema
        else:
            print("Error fetching the schema. Status code:", response.status_code)

    def get_table_schema2(self, notionJson):
        dic_schema = {}
        if 'results' in notionJson:
            for item in notionJson['results']:
                dict_prop = item['properties']
                new_dict = {}
                for key, value in dict_prop.items():
                    v_type = value['type']
                    dic_schema[key] = v_type
                break
        return dic_schema

    def get_kv_from_properties_dict(self, dict_prop):
        new_dict = {}
        for key, value in dict_prop.items():
            v_type = value['type']
            new_dict[key] = ''
            if v_type == 'title':
                if len(value['title'])>0:
                    new_dict[key] = value['title'][0]['plain_text']
                else:
                    new_dict[key] =''
            if v_type == 'checkbox':
                new_dict[key] = value['checkbox']
            if v_type == 'rich_text':
                if len(value['rich_text'])>0:
                    new_dict[key] = value['rich_text'][0]['plain_text']
            if v_type == 'select':
                new_dict[key] = value['select']['name']
            if v_type == 'multi_select':
                if len(value['multi_select'])>0:
                    new_dict[key] = [x['name'] for x in value['multi_select']]
            if v_type == 'number':
                new_dict[key] = value['number']
        return new_dict

    def get_kv_from_result_dict(self, item):
        dict_prop = item['properties']
        new_dict = self.get_kv_from_properties_dict(dict_prop)

        ## 获取row_id
        row_url = item['url']
        postfix = row_url.split("/")[-1]
        row_id = postfix.split("-")[-1]
        new_dict['row_id'] = row_id
        return new_dict


    def convert_notionJson_to_dict(self, notionJson):
        ret_dict = []
        if 'results' in notionJson:
            for item in notionJson['results']:
                new_dict = self.get_kv_from_result_dict(item)

                # print(row_url, postfix, row_id)
                ret_dict.append(new_dict)

        return ret_dict
        

    def delete_page(self, page_id):
        body = {
            'archived': True
        }


        url = 'https://api.notion.com/v1/pages/'+page_id
        print("delete url:", url)
        notion = self.session.patch(url,headers=self.headers,json=body)

        print(notion)

        return 0

    def has_column_in_notion_database(self, database_id, column_name):
        # 发送 GET 请求来获取数据库的结构信息
        time.sleep(self.waittime_notion)
        response = self.session.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=self.headers
        )

        if response.status_code == 200:
            data = response.json()
            properties = data.get("properties", {})
            print("properties:", properties)
            # 判断是否有 B 列
            if column_name in properties:
                print("有 B 列")
                return True
            else:
                print("没有 B 列")
                return False
        else:
            print(f"请求失败：{response.status_code} - {response.text}")
            return False

    def add_column_to_notion_database(self, database_id, column_name):
        time.sleep(self.waittime_notion)
    # 构建要添加的 B 列的信息
        new_column_data = {
            #"title": [
            #    {
            #        "type": "text",
            #        "text": {
            #            "content": column_name,
            #        },
            #    },
            #],
                "update_date2": {
                    "id": "Qimp",
                    "type": "date",
                    "date": {
                        "start": "2023-07-18",
                        "end": None,
                        "time_zone": None
                    }
                },
        }

        # 发送 PATCH 请求来添加 B 列
        response = self.session.patch(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=self.headers,
            json={"properties": {column_name: new_column_data}},
        )

        if response.status_code == 200:
            print(f"成功添加列 {column_name}")
        else:
            print(f"请求失败：{response.status_code} - {response.text}")


    def delete_row_in_notion_database(self, row_id):
        time.sleep(self.waittime_notion)
        response = self.session.delete(
                    f"https://api.notion.com/v1/blocks/{row_id}",
                    headers=self.headers,
                )
        if response.status_code != 200:
            print(f"删除行失败：{response.status_code} - {response.text}")
        else:
            pass
            # print("删除行成功！", row_id)

    def clear_database(self, database_id):
        time.sleep(self.waittime_notion)
        ret_json = self.dataBase_item_query(database_id, 'db_config.json')
        list_ret_dict = self.convert_notionJson_to_dict(ret_json)
        for kv in list_ret_dict:
            row_id = kv['row_id']
            self.delete_row_in_notion_database(row_id)
        print("clear_database done! db_id:%s" % (database_id))




    def dataBase_filter_select_item(self, query_database_id, payload = None, dic_select={}, dic_checkbox={}, dic_datetime={}, 
                                    list_property=[], fname_out="data.json"):
        time.sleep(self.waittime_notion)
        url_notion_block = 'https://api.notion.com/v1/databases/'+query_database_id+'/query'
        if payload is None:
            payload = {
                "filter":{
                    "and":[
                    ]
                } ,
                 'properties': [ 'config_select']
            }

            for key,value in dic_select.items():
                tmp_select = \
                    {
                        'property': key,
                        'select': {
                            'equals': value
                        }
                    }
                payload['filter']['and'].append(tmp_select)

            for key,value in dic_checkbox.items():
                tmp_checkbox = \
                    {
                        'property': key,
                        'checkbox': {
                            'equals': value
                        }
                    }
                payload['filter']['and'].append(tmp_checkbox)
            
            for key, value in dic_datetime.items():
                cmp, key_day = key.split("|")[0], key.split("|")[1]

                tmp_date_filter = \
                    {
                        "property": key_day,
                        "date": {
                            "on_or_%s"%(cmp): value 
                        }
                    }
                payload['filter']['and'].append(tmp_date_filter)

            # if list_property is not None:
                # payload['properties'] = list_property
# 
            
            json_data = json.dumps(payload, indent=4)
            with open('payload.json', 'w') as file:
                file.write(json_data)
            
            # payload = {
                # "filter": { 
                        # "property": "config_select",
                        # "select": {
                            # "equals": "auto_gen"
                        # }
# 
                # },
                # 'properties': [ 'config_select']
            # }
        
        # res_notion = requests.post(url_notion_block, json= payload,    headers=self.headers)
        res_notion = self.session.post(url_notion_block, json= payload,    headers=self.headers)
        res_json = res_notion.json()

        json_data = json.dumps(res_json, indent=4)
        with open(fname_out, 'w') as file:
            file.write(json_data)
        return res_json


    def dataBase_item_query(self, query_database_id, fname_out="data.json"):
        time.sleep(self.waittime_notion)
        url_notion_block = 'https://api.notion.com/v1/databases/'+query_database_id+'/query'
        res_notion = self.session.post(url_notion_block,headers=self.headers)
        S_0 = res_notion.json()

        json_data = json.dumps(S_0, indent=4)
        with open(fname_out, 'w') as file:
            file.write(json_data)
        return S_0



    def page_query(self, page_id):
        time.sleep(self.waittime_notion)
        url = 'https://api.notion.com/v1/pages/%s' % (page_id)

        response = self.session.get(url,  headers=self.headers)
        json_data = json.dumps(response.json(), indent=4)
        with open('page.json', 'w') as file:
            file.write(json_data)

        print(response.text)

    def retrieve_block_children(self, page_id):
        time.sleep(self.waittime_notion)
        url = 'https://api.notion.com/v1/blocks/%s/children'  % (page_id)
        response = self.session.get(url,  headers=self.headers)
        json_data = json.dumps(response.json(), indent=4)
        with open('block_children.json', 'w') as file:
            file.write(json_data)
        print(response.text)


    def create_page(self, parentid, title, list_content = []):
        time.sleep(self.waittime_notion)
        url = "https://api.notion.com/v1/pages"

        payload = {

            "parent": {
                "type":"page_id",
                "page_id":parentid,
            },

            "properties": {
                "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": title,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": title,
                            "href": None
                        }
                    ],
                "Tags": {
                    "id": "iP{h",
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "0bf325ed-ba55-4b75-bbdd-1212e9e4eb32",
                            "name": "4",
                            "color": "pink"
                        }
                    ]
                }

            },
            "children": []
        }

        for content in list_content:
            new_json = self.notion_block.add_head_json(content)
            payload["children"].append(new_json)

        # new_title = self.notion_block.add_head_json("#hhh1")
        # payload["children"].append(new_title)
        # new_title = self.notion_block.add_head_json("##hhh2")
        # payload["children"].append(new_title)
# 
        # new_title = self.notion_block.add_head_json("parwe1")
        # payload["children"].append(new_title)
        # encoded_data = urllib.parse.urlencode(payload)
        response = self.session.post(url, json=payload, headers=self.headers)
        print("notion_sdk create_page response:", response)

        dic_resp = response.json()
        new_page_id = dic_resp["id"]
        return new_page_id

    def append_block_children(self, block_id, path_content):
        time.sleep(self.waittime_notion)
        url = "https://api.notion.com/v1/blocks/%s/children" %(block_id)

        def split_content(content, n):
            return [content[i:i+n] for i in range(0, len(content), n)]
        list_content = []
        with open(path_content, "r", encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip(" ").strip("\n")
                if len(line)< 1500:
                    list_content.append(line)
                else:
                    new_line_list = split_content(line, 1500)
                    list_content.extend(new_line_list)


        payload = {
            "children":[]
        }
        cnt=0
        for content in list_content:
            cnt+=1
            new_json = self.notion_block.add_head_json(content)
            payload["children"].append(new_json)

            if cnt>80:
                response = self.session.patch(url, json=payload, headers=self.headers)
                print("notion_sdk create_block response:", response)
                time.sleep(20)
                cnt =0
                payload["children"] = []

        json_data = json.dumps(payload, indent=4)
        with open('append_block_children.json', 'w') as file:
            file.write(json_data)

        response = self.session.patch(url, json=payload, headers=self.headers)
        print("notion_sdk create_block response:", response)
        dic_resp = response.json()
        new_page_id = dic_resp["id"]
        return new_page_id


    def get_base_unit_json(self, unit_type='select', key='key', value='value', link=''):
        time.sleep(self.waittime_notion)
        ret_json = {} 
        if unit_type =='select':
            ret_json = {
                key: {
                    "id": "f==P",
                    "type": "select",
                    "select": {
                        "name": value,
                        # "color": "brown"
                    }
                }
            }
        if unit_type == 'date':
            ret_json = {
                key: {
                    "type": "date",
                    "date": {
                        "start": value,
                        "end": None,
                        "time_zone": None
                    }
                }
            }
        if unit_type == 'multi_select':
            ret_json = {
                key: {
                    "type": "multi_select",
                    "multi_select": [
                    ]
                },
            }
            for xx in value:
                ret_json[key]["multi_select"].append({"name":xx})
        if unit_type == 'checkbox':
            ret_json = {
                key: {
                    "id": "jmt{",
                    "type": "checkbox",
                    "checkbox": value
                }
            }


        elif unit_type == 'title':
            ret_json = {
                key: {"title": [{"type": "text", "text": {"content": value}}]},
            }
        elif unit_type == 'rich_text':
            if len(value)>=1800:
                value = value[:1800]
                value = value + "\n 原文内容超出notion长度限制，请到原始链接查看"
            ret_json = {
                key: {
                    "id": "=@nd",
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": value,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": value,
                            "href": None
                        }
                    ]
                },
            }
        return ret_json

    def add_new_row_in_crawl_db(self, db_id, list_columns=[]):
        time.sleep(self.waittime_notion)
        url = "https://api.notion.com/v1/pages"
        payload = {
            "parent": {"type": "database_id", "database_id": db_id},
            "properties": {
                # "title": {"title": [{"type": "text", "text": {"content": title}}]},
                # "category": {
                    # "id": "f==P",
                    # "type": "select",
                    # "select": {
                        # "id": "ce775a78-1d11-473e-ac9e-be26e996f985",
                        # "name": "cate2",
                        # "color": "brown"
                    # }
                # },
            }
        }
        for column in list_columns:
            ## type key value link
            new_unit = self.get_base_unit_json(column[0], column[1], column[2], column[3])
            payload['properties'].update(new_unit)

        response = self.session.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            pass
        else:
            print("添加行时出现错误：", response.json())
            return {"msg": "insert error"}

        dic_prop = response.json()
        kv_dict = self.get_kv_from_result_dict(dic_prop)
        # kv_dict = self.get_kv_from_properties_dict(dic_prop)
        return kv_dict
        # print(response.text)


    def add_new_row_in_db(self, parent_id, title, video_link, page_link):
        time.sleep(self.waittime_notion)
        url = "https://api.notion.com/v1/pages"
        new_page_link = "https://www.notion.so/%s" % (page_link)
        # new_page_link = "/%s" % (page_link )
        # new_page_link = "/3e1b38c55f564bb6886ca75a29278e2c"
        # print("new_page_link:", new_page_link)


        payload={
            "parent": {"type": "database_id", "database_id": parent_id},
            "properties": {
                "title": {"title": [{"type": "text", "text": {"content": title, "link": {"url": video_link} }}]},
                "\u5468\u6570": {
                    "id": "_^;W",
                    "type": "select",
                    "select": {
                        "id": "m<U^",
                        "name": "20\u5468",
                        "color": "blue"
                    }
                },
                "\u6587\u6848\u9636\u6bb5": {
                    "id": "yVds",
                    "type": "select",
                    "select": {
                        "id": "6de12623-45b1-4842-bf3f-db04beb8d90f",
                        "name": "01\u6d77\u9009",
                        "color": "orange"
                    }
                },
                "\u539f\u59cb\u6587\u6848": {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "\u539f\u59cb",
                                "link": {
                                    "url": new_page_link
                                }
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "\u539f\u59cb",
                            "href": new_page_link
                        }
                    ]
                },
            }
        }


        response = self.session.post(url, json=payload, headers=self.headers)

        print(response.text)

    def update_db_row_content(self, row_id, list_columns):
        time.sleep(self.waittime_notion)
        data = {
            "properties": {
                # "new_scrawl_date": {
                    # "rich_text": [
                        # {
                            # "text": {
                                # "content": new_date
                            # }
                        # }
                    # ]
                # }
            }
        }
        for column in list_columns:
            ## type key value link
            new_unit = self.get_base_unit_json(column[0], column[1], column[2], column[3])
            data['properties'].update(new_unit)

        response = self.session.patch(f"https://api.notion.com/v1/pages/{row_id}", headers=self.headers, json=data)
        # 检查响应状态码
        if response.status_code == 200:
            print("行内容已成功更新！")
        else:
            print("更新行内容时出现错误：", response.json())
        return response

if __name__== '__main__':
    notion_sdk = NotionSDK()