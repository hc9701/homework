from lxml import html

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
            ratings['%s' % rating['rating']] = rating['ratingCounts']
        self.rating['ratings'] = ratings
        for comment in json2['list']:
            self.comments.append({
                'time': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(comment['operTime'], '%Y/%m/%d %H:%M')),
                'content': comment['commentInfo'],
                'app_name': self.app_name,
                'store_name': self.store_name,
            })

    def store(self):
        db.ratings.update_one({
            'app_name': self.app_name,
            'store_name': self.store_name
        },
            {'$set': self.rating},
            upsert=True,
        )
        db.comments.insert_many(self.comments)


class Spider360(SpiderAbstract):
    def __init__(self, url, max_result=30):
        self.max_result = max_result
        self.url_title = url
        self.url_comment = 'http://comment.mobilem.360.cn/comment/getComments?baike=%s&start=0&count=%d'
        self.url_rating = 'http://comment.mobilem.360.cn//comment/getLevelCount?baike=%s'
        self.store_name = '360应用市场'
        self.app_name = ''
        self.rating = {'type': 3, 'store_name': self.store_name}
        self.comments = []

    def parse(self):
        f = requests.get(self.url_title)
        doc = html.fromstring(f.content)
        self.app_name = doc.xpath('//title')[0].text.split('_')[0]
        self.rating['app_name'] = self.app_name
        script_list = doc.xpath('//script')[8].text.strip()
        baike_name = script_list.split('\n')[12].split("'")[3]
        f1 = requests.get(self.url_comment % (baike_name, self.max_result)).json()
        for comment in f1['data']['messages']:
            self.comments.append({
                'app_name': self.app_name,
                'store_name': self.store_name,
                'content': comment['content'],
                'time': comment['create_time'],
            })
        f2 = requests.get(self.url_rating % baike_name).json()
        self.rating['好评'] = f2['best']
        self.rating['中评'] = f2['good']
        self.rating['差评'] = f2['bad']

    def store(self):
        db.ratings.update_one({
            'app_name': self.app_name,
            'store_name': self.store_name
        },
            {'$set': self.rating},
            upsert=True,
        )
        db.comments.insert_many(self.comments)


class SpiderKuChuan():
    def __init__(self, url, day=365):
        package_name = url.split('?')[1].split('&')[0].split('=')[1]
        self.url = url
        self.url_data = 'http://android.kuchuan.com/histortydailydownload?packagename=%s&longType=%d-d' % (
            package_name, day)
        self.score = []
        self.app_name = ''

    def parse(self):
        f = requests.get(self.url)
        doc = html.fromstring(f.content)
        self.app_name = doc.xpath('//input[1]')[0].get('value')
        f = requests.get(self.url_data).json()['data']
        categories = f['categories']
        data = f['series'][0]['data']
        for when, value in zip(categories, data):
            self.score.append({
                "time": time.strptime(when, '%Y-%m-%d'),
                "value": value["y"],
                "app_name": self.app_name,
            })

    def store(self):
        db.scores.insert_many(self.score)


if __name__ == '__main__':
    # spider = SpiderHuaWei('http://a.vmall.com/uowap/index.html#/detailApp/C9319')
    # spider = SpiderHuaWei('http://a.vmall.com/uowap/index.html#/detailApp/C10111119')
    # spider = Spider360('http://zhushou.360.cn/detail/index/soft_id/7953?recrefer=SE_D_qq')
    # spider = Spider360('http://zhushou.360.cn/detail/index/soft_id/902591')
    # spider = SpiderKuChuan(
    #     'http://android.kuchuan.com/page/detail/download?package=com.tencent.mobileqq&infomarketid=1&site=0#!/day/com.tencent.mobileqq')
    spider = SpiderKuChuan(
        'http://android.kuchuan.com/page/detail/download?package=com.tencent.qqlite&infomarketid=1&site=0#!/day/com.tencent.qqlite')
    spider.parse()
    spider.store()
    # pymongo.errors.BulkWriteError: batch op errors occurred
