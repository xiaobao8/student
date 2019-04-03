# import requests
# from lxml import etree
# from pymongo import MongoClient
#
#
# class DianYing(object):
#     def __init__(self):
#         self.start_url = "http://www.1905.com/vod/list/n_1/o3p1.html?fr=vodhome_js_rbpb"
#         self.headers = {
#             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
#         }
#         self.db = MongoClient()
#         self.collection = self.db.dianying
#     def get_content(self, url):
#         response = requests.get(url, headers=self.headers)
#         return etree.HTML(response.content.decode())
#
#     def data_save(self, data):
#         # 添加
#         self.db.collection.dianying.insert(data)
#         print("添加成功")
#     def run(self):
#
#         while True:
#             ele = {}
#             content = self.get_content(self.start_url)
#             sele = content.xpath("//section[@class='mod row search-list']/div")
#             for i in sele:
#                 ele["href"] = i.xpath("./a/img/@src")
#                 ele["title"] = i.xpath("./a/h3/text()")
#                 ele["daoyan"] = i.xpath(".//p/text()")
#                 self.data_save(ele)
#                 ele = {}
#
#
# if __name__ == '__main__':
#     d = DianYing()
#     d.run()