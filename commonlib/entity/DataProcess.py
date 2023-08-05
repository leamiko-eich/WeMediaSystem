#encoding=utf-8
from DBAgent import DBAgent
from articles import Article, UserConfig

class DataProcess(object):
    def __init__(self):
        self.db_agent = DBAgent('sqlite', '../data/articles.db')


    def get_latest_articles(self, reqeust_args=None):
        query_dict = {}
        query_list = ["type", "author", "website", "category"]
        for query in query_list:
            value = reqeust_args.get(query, "Empty")
            print("query:%s value:%s" %(query, value))
            if value !="Empty":
                query_dict[query]  = value
        print("query_dict:", query_dict)
        db_ret = self.db_agent.get_latest_articles(query_dict)
        list_article = []
        for item in db_ret:
            new_article = Article(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            list_article.append(new_article)
        return list_article

    def get_all_subscribe_users(self, request_args=None):
        list_users = []
        db_ret = self.db_agent.get_all_users()
        for item in db_ret:
            new_user = UserConfig(item[0], item[1], item[2], item[3], item[4], item[5]) 
            list_users.append(new_user)
        return list_users


    def add_new_config(self, post_dict):
        new_user = UserConfig()
        new_user.parse_from_post_dict(post_dict)
        # def insert_crawl_link(self, username, author, source, category, link):
        self.db_agent.insert_crawl_link(new_user.user, new_user.author, new_user.website, new_user.category, new_user.subscribe_url)
        return new_user


        
