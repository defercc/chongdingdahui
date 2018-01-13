import time
import json
import requests
import logging
import webbrowser
from urllib import parse
import urllib.parse
from bs4 import BeautifulSoup

class Worker(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.baidu_query_url = 'http://htpmsg.jiecaojingxuan.com/msg/current'
		self.timeout = 4

	def get_subject(self):
		# 获取接口数据
		subject_json = requests.get(self.baidu_query_url,timeout=self.timeout).json()

		# 判断答题数据是否有返回
		if 'msg' in subject_json and subject_json['msg'] == 'no data':
			print(time.strftime('%H:%M:%S',time.localtime(time.time())), 'Wating for the subject...')
			return

		# 答题数据返回判断数据格式
		if 'data' in subject_json:
			data = subject_json['data']
			if 'event' in data and 'desc' in data['event'] and 'options' in data['event']:
				event, desc, options = data['event'], data['event']['desc'], json.loads(data['event']['options'])

				# 打印问题
				print(desc)

				# 打开百度浏览器搜索题目
				self.start_browser_and_search(desc)

				# 打印选项并返回(题目+选项)在bing搜索的结果数，结果只做参考
				if len(options) >= 2:
					for op in tuple(options):
						self.getSearchCount(desc, op)

					input('按任意键继续')
				else:
					print('No options...')

	def start_browser_and_search(self, search_wd):
	    s_url = 'https://www.baidu.com/s?wd=' + search_wd
	    search_question = urllib.parse.quote(search_wd)
	    webbrowser.open('https://www.baidu.com/s?wd=' + search_question)

	def getSearchCount(self, desc, option):
		soup = None
		bing_query_str = 'https://cn.bing.com/search?q=%s&qs=n&form=QBRE&sp=-1&pq=undefined&sc=1-15&sk=&cvid=47AF996DCDC445E3BF15B6E776D53F45' % (desc+option)
		htmldoc = requests.get(bing_query_str,timeout=self.timeout).text

		soup = BeautifulSoup(htmldoc, "html.parser")
		if len(soup.find_all('span', class_='sb_count')) >= 1:
			print(option, '====>',soup.find_all('span', class_='sb_count')[0].string)
		else:
			print(option, '====> 暂无结果')

	def main(self):
	    while True:
	        self.get_subject()
	        time.sleep(1)

if __name__ == '__main__':
	worker = Worker()
	worker.main()
	