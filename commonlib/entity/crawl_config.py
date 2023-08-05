
### 即将删除，不再使用
class CrawlConfig(object):
    def __init__(self,  user, author, website, category, link_homepage, crawl_date):
        self.user = user
        self.author = author
        self.website = website
        self.category = category
        self.link_homepage = link_homepage
        self.crawl_date = crawl_date

    def __str__(self):
        return f"{self.user}\n{self.author}\n{self.website}\n{self.link_homepage}"
