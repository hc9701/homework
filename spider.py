import requests
import time

from shuju import db

class SpiderAbstract():
    def parse(self):
        pass

    def store(self):
        pass

class SpiderHuaWei(SpiderAbstract):
    def __init__(self, url, max_result=30):
        app_id = url.split('/')[-1]
        self.url_title = 'http://a.vmall.com/uowap/index?method=internal.getTabDetail&serviceType=13&reqPageNum=1&uri=app|%s&maxResults=1' % (
            app_id)
        self.url_data = 'http://a.vmall.com/uowap/index?method=internal.user.commenList3&serviceType=13&reqPageNum=1&maxResults=%d&appid=%s' % (
            max_result, app_id)
        self.rating = {}
        self.comments = []
        self.app_name = ''
        self.store_name = '华为应用市场'

    def parse(self):
        json1 = requests.get(self.url_title).json()
        self.app_name = json1['layoutData'][0]['dataList'][0]['name']
        self.rating['app_name'] = self.app_name
        self.rating['store_name'] = self.store_name
        self.rating['type'] = 5
        json2 = requests.get(self.url_data).json()
        ratings = {}
        for rating in json2['ratingDstList']:
            ratings['%s'%rating['rating']] = rating['ratingCounts']
        self.rating['ratings'] = ratings
        for comment in json2['list']:
            self.comments.append({
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(comment['operTime'], '%Y/%m/%d %H:%M')),
                'content': comment['commentInfo'],
                'app_name': self.app_name,
                'store_name': self.store_name,
            })

    def store(self):
        db.comments.insert_many(self.comments)
        db.ratings.update_one({
            'app_name': self.app_name,
            'store_name': self.store_name
        },
            {'$set': self.rating},
            upsert=True,
        )

class Spider360(SpiderAbstract):
    def __init__(self,url,max_Result = 30):
        self.url_title = url

        self.url_comment = 'http://a.vmall.com/uowap/index?method=internal.user.commenList3&serviceType=13&reqPageNum=1&maxResults=%d&appid=%s' % (
            max_result, app_id)
        self.rating = {}
        self.comments = []
        self.app_name = ''
        self.store_name = '华为应用市场'
        pass

    def parse(self):
        super().parse()

    def store(self):
        super().store()


if __name__ == '__main__':
    spider = SpiderHuaWei('http://a.vmall.com/uowap/index.html#/detailApp/C9319')
    # spider = SpiderHuaWei('http://a.vmall.com/uowap/index.html#/detailApp/C10111119')
    spider.parse()
    spider.store()
    print(spider.rating, spider.comments)
