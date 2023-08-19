#encoding=utf-8
import os,sys
ROOTDIR_WeMediaSystem = os.getenv('ROOTDIR_WeMediaSystem')
os.chdir(ROOTDIR_WeMediaSystem)
sys.path.append(ROOTDIR_WeMediaSystem)

from .BaseSelenium import BaseSelenium 
from .ZhihuSelenium import ZhihuSelenium
from .DoubanSelenium import DoubanSelenium
from .WechatPublicSelenium import WechatPublicSelenium
from .XiaohongshuSelenium import XiaohongshuSelenium

from commonlib.schema import MsgInfo, TaskInfo, GenerateArticle, PublicArticle
import logging


class SeleniumManager(object):
    def __init__(self):
        self.platform_agents = {}

    def register_platform_agent(self, platformAgent : BaseSelenium):
        self.platform_agents[platformAgent.name_platform] = platformAgent

    def init_platforms(self):
        self.register_platform_agent(ZhihuSelenium)
        self.register_platform_agent(DoubanSelenium)


    def call_platform(self,  msg_info: MsgInfo):

        name_platform = msg_info.task_info.platform
        logging.info("call_platform name_platform:%s", name_platform)
        assert(name_platform in self.platform_agents)

        cls_agent  = self.platform_agents[name_platform]
        plat_agent : BaseSelenium  = cls_agent()

        if msg_info.task_info.task_name == 'PublicArticle':
            account_name = msg_info.public_article.account_name
            art_title = msg_info.generate_article.generate_title
            art_content = msg_info.generate_article.generate_content

            plat_agent.login_with_cookie(account_name)
            plat_agent.publish_article(art_title, art_content)

        else:
            logging.info("没有找到对应的task： %s" % (msg_info.task_info.task_name))


    def scrawl_platform(self, msg_info: MsgInfo):
        name_platform = msg_info.task_info.platform
        logging.info("call_platform name_platform:%s", name_platform)
        assert(name_platform in self.platform_agents)

        cls_agent  = self.platform_agents[name_platform]
        plat_agent : BaseSelenium  = cls_agent()

        if msg_info.task_info.task_name == 'ScrwalAuthorLink':
            subscribe_link = msg_info.target_author.subscribe_link
            link_art_url = plat_agent.crawl_by_author_link(subscribe_link)
            for dic_url  in link_art_url:
                original_link = dic_url['original_link']
                dic_ret = plat_agent.parse_specific_article(original_link)
                print(dic_ret)
        else:
            logging.info("没有找到对应的task： %s" % (msg_info.task_info.task_name))
    