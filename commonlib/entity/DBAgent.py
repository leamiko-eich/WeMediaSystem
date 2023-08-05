import sqlite3
#import mysql.connector
import logging
from NotionSDK import NotionSDK
from commonlib.entity.articles import Article

class DBAgent:
    def __init__(self, db_type, db_name):
        if db_type == "sqlite":
            self.conn = sqlite3.connect(db_name)
        elif db_type == "mysql":
            pass
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database=db_name
            )
        self.cur_article = self.conn.cursor()
        self.cur_article.execute('''CREATE TABLE IF NOT EXISTS articles
                           (user TEXT, author TEXT, website TEXT, category TEXT, title TEXT, url TEXT PRIMARY KEY, 
                           create_date DATE NOT NULL,  art_content TEXT)''')
        self.conn.commit()
        self.notion_sdk = NotionSDK()
        self.database_id = '7f863dd9221844179e047825b57e8a58' ## 爬虫数据库
        self.notiondb_scrawl_config = '4fd530b46946419cae8ce0e86f82d2d0' ## 爬虫配置数据库

    def insert_data_by_sql(self, sql, tuple_param):
        self.cur_article.execute(sql, tuple_param)
        self.conn.commit()
    
    def save_article(self, article):
        # logging.info(" save_article title:%s" %(article.title) )
        self.cur_article.execute("INSERT OR REPLACE INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
            article.user, article.author, article.website, article.category, article.title, 
            article.url, article.create_date, article.art_content))
        self.conn.commit()

        list_columns = [
             ["title","title",article.title,""] ,
             ["select","category",article.category,""] ,
             ["select","website",article.website,""] ,
             ["select","author",article.author,""] ,
             ["rich_text","art_link",article.url,""] ,
             ["rich_text","update_date",article.create_date,""] ,
             ["rich_text","art_content",article.art_content,""] ,
        ]
        self.notion_sdk.add_new_row_in_crawl_db(self.database_id, list_columns)

    def get_latest_articles_as_obj(self, query_dict):
        list_ret = self.get_latest_articles(query_dict)
        list_obj = []
        for item in list_ret:
            obj_art = Article(user=item[0], author=item[1], website=item[2], category=item[3], title=item[4],  
                              url=item[5], create_date=item[6], art_content=item[7])
            list_obj.append(obj_art)
        return list_obj

    def get_latest_articles(self, query_dict):
        sql_select = "Select * from articles"
        sql_condition = ""
        if "type" in query_dict and query_dict["type"]!="all":
            sql_condition += "where "
            mtype = query_dict["type"]
            sql_condition += " category='%s' " %(mtype) 

        if "author" in query_dict and query_dict["author"]!="all":          
            if sql_condition == "":
                sql_condition += " where "
            else:
                sql_condition += " and "
            author = query_dict["author"]
            sql_condition += " author='%s' " %(author)

        if "website" in query_dict and query_dict["website"]!="all":
            if sql_condition == "":
                sql_condition += " where "
            else:
                sql_condition += " and "
            website = query_dict["website"]
            sql_condition += " website='%s' " %(website)


        sql_rank = "order by create_date desc limit 500"


        all_sql = "%s %s %s" %(sql_select, sql_condition, sql_rank)
        self.cur_article.execute(
            all_sql
        )
        ret = self.cur_article.fetchall()
        return ret

    def get_articles_by_sql_as_obj(self, sql):
        list_ret = self.get_article_by_sql(sql)
        list_obj = []
        for item in list_ret:
            obj_art = Article(user=item[0], author=item[1], website=item[2], category=item[3], title=item[4],  
                              url=item[5], create_date=item[6], art_content=item[7])
            list_obj.append(obj_art)
        return list_obj


    def get_article_by_sql(self, sql):
        self.cur_article.execute(
            sql
        )
        ret = self.cur_article.fetchall()
        return ret

    def get_all_users(self):
        self.cur_article.execute(
            "SELECT * FROM crawl_config"
        )
        ret = self.cur_article.fetchall()
        return ret

    def get_subscribe_link(self, website):
        self.cur_article.execute(
            "SELECT * FROM crawl_config where website='%s'" % (website)
        )
        ret = self.cur_article.fetchall()
        new_ret = []
        for line in ret:
            newline = line + ('sqlite', 'unique_id')
            new_ret.append(newline)

        # 查询部分内容
        payload = None
        dic_select = {'website':website}
        dic_checkbox = {}
        list_property = []
        ret_json = self.notion_sdk.dataBase_filter_select_item(self.notiondb_scrawl_config, payload=payload, dic_select=dic_select, dic_checkbox=dic_checkbox, 
                                                       list_property=list_property, fname_out='db_config_with_filter.json')
        ret_list_dict = self.notion_sdk.convert_notionJson_to_dict(ret_json)

        for kv in ret_list_dict:
            new_config = [ kv['username'], kv['arthur'], kv['website'], kv['category'], kv['subscribe_link'], kv['new_scrawl_date'], 'notion_db', kv['row_id']]
            new_ret.append(new_config)

        return new_ret

    def insert_crawl_link(self, username, author, source, category, link):
        init_crawl_date = "2023-01-01 12"
        self.cur_article.execute('''
            INSERT OR REPLACE INTO crawl_config (username, author, website, category, link_homepage, crawl_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, author, source, category, link, init_crawl_date))
        self.conn.commit()

    def update_crawl_date(self, link, new_crawl_date):
        sql_line = "update crawl_config set crawl_date = '%s' where link_homepage = '%s'" %(new_crawl_date, link)
        self.cur_article.execute(sql_line)
        self.conn.commit()

    def test_sql(self):
        sql = "select * from articles where category='技术'"
        self.cur_article.execute(sql)
        ret = self.cur_article.fetchall()
        for item in ret:
            print(item)


    def close(self):
        self.conn.close()


if __name__=="__main__":
    db_agent = DBAgent('sqlite', '../../data/articles.db')
    # db_agent.test_sql()
    db_ret = db_agent.get_all_users()
    for line in db_ret:
        print(line)
