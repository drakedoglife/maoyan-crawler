import re
import requests
from bs4 import BeautifulSoup as bs
import time

def getHTMLText(url, **headers):
	try:
		if headers:
			r = requests.get(url, headers=headers)
		else:
			r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ''

def getMovieList(url, lst):
	for i in range(10):
		true_url = url + str(i * 10)
		html = getHTMLText(true_url, **{
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
			'Connection': 'keep-alive',
			'Accept-Encoding': 'gzip, deflate, br',
			'Cookie': '__mta=150377737.1585390071914.1585838152324.1585838294621.17; _lxsdk_s=1713b45812a-ffe-f57-336%7C%7C36; mojo-session-id={"id":"5534f86731c5c82f1c3d689ff6f311f9","time":1585837341884}; mojo-trace-id=30; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1585840802; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1585390072,1585420861,1585837341; __mta=150377737.1585390071914.1585840156561.1585840801756.19; _csrf=4b5ba2273380da5c524f1b46e937ebf2e3fe4a58964817525fbac085f4183f71; mojo-uuid=0a78381235d0369b85ed32c962f65bd8; _lxsdk=FBA8488070DB11EA9627719D08EAB05445E2FA03967A425DA063148CF66BD463; _lxsdk_cuid=171209caf8e77-0fde037e02935d8-3f616e4b-13c680-171209caf8fc8; uuid=FBA8488070DB11EA9627719D08EAB05445E2FA03967A425DA063148CF66BD463; uuid_n_v=v1',
			'Accept-Language': 'zh-cn',
			'Host': 'maoyan.com'
			})
		try:
			if html == '':
				continue
			soup = bs(html, 'html.parser')
			movieDict = {}
			dd = soup.find_all('dd')
			for info in dd:
				rank = info.find('i', attrs={'class': 'board-index'}).text
				name = info.find('p', attrs={'class': 'name'}).find('a').text
				star = re.findall(r'[\u4e00-\u9fa5]+', info.find('p', attrs={'class': 'star'}).text)
				del star[0]
				releasetime = info.find('p', attrs={'class': 'releasetime'}).text.split(':')[-1]
				score = re.findall(r'\d.*?\d', info.find('p', attrs={'class': 'score'}).text)
				movieDict.update({
					'排名': rank,
					'电影名称': name,
					'主演': star,
					'上映时间': releasetime,
					'得分': score
					})
				with open('maoyan.txt', 'a') as f:
					f.write(str(movieDict) + '\n')
		except:
			break


if __name__ == '__main__':
	url = "https://maoyan.com/board/4?offset="
	mList = []
	getMovieList(url, mList)

