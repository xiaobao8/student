import pymysql
pymysql.install_as_MySQLdb()
# import requests
#
# class ZhiLianSpder(object):
#     def __init__(self):
#         self.start_url = "https://mq.51job.com/ajax/get_cojoblist.ajax.php"
#         self.header = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
#         }
#         self.data = {
#             "ucoid": 156141,
#             "pageno": 1,
#             "pagesize": 20
#         }
#
#     def get_content(self, url):
#         response = requests.post(url, headers=self.header, data=self.data)
#         return response.json()
#
#     def run(self):
#         for i in range(2):
#             content = self.get_content(self.start_url)
#             for ii in content["joblist"]:
#                 print(ii["cname"])
#             self.data["pageno"] = i
#             print('------------------------')
#
#
#
# if __name__ == '__main__':
#     zl = ZhiLianSpder()
#     zl.run()