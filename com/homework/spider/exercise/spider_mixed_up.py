from selenium import webdriver
import requests
import urllib.request
import os
from lxml import etree
import time
import csv
import os
import random
import re
from bs4 import BeautifulSoup
import logging
from xpinyin import Pinyin

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
request_headers = {
    'user-agent' : random.choice(user_agents),
    'Cookie' : '__mta=213809707.1600309936636.1600395373095.1600397540112.15; uuid_n_v=v1; _lxsdk_cuid=17499e7c1a5c8-04796d3442dc92-333769-1fa400-17499e7c1a5c8; mojo-uuid=ccc90bd7045deb2c3355723a6d089b36; mojo-session-id={"id":"e1905c32abed2ce5a89b2884ff769c2f","time":1600391401740}; uuid=43C2EAE0F95711EA86376D55CEC8169C2677CE17D23446779C88E831141DB95D; _csrf=ec0a5b65323422385053b12760660e24259f4583f50540b5c4fb274b33060570; lt=u4rJ3X4RYcCpb-6zrTGO28az6VEAAAAAkAsAADHvmG86-GvpLp1kwAtawGknywwUpVKnYbHE3lyif9SmV2QWI5HS1E5awgZCAjN4Ww; lt.sig=GmmmCbnXQC-FcFnDwmhAJLihtjs; _lxsdk=43C2EAE0F95711EA86376D55CEC8169C2677CE17D23446779C88E831141DB95D; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1600309937,1600350591,1600391402,1600396381; __mta=213809707.1600309936636.1600395373095.1600397538191.15; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1600397540; mojo-trace-id=94; _lxsdk_s=1749ec2d0fe-8c5-c6a-e0d%7C%7C153'
}

csv_file_name = 'homework_information_of_movies.csv'
csv_file_path = 'e:' + os.sep + csv_file_name

csv_fp = open(csv_file_path, 'wt', newline='', encoding='utf-8-sig')    #行间无空行，编码是带有信号位的文本文件

csv_writer = csv.writer(csv_fp)

#   得到每页26个电影的 符合month限定要求的 链接， 并将链接传给找到对应电影信息的函数
def get_per_page_26_movies_links(url, month):
    web_data = requests.get(url=url, headers=request_headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        soup = BeautifulSoup(html_text, 'lxml')
        selector = etree.HTML(html_text)                                            # 默认一套网页信息处理
        movie_public_date = selector.xpath('//span[contains(text(),"上映时间:")]')[0].tail  # 根据“上映时间”关键字来做定位
        print(movie_public_date)
        p = re.compile('\s+')
        movie_public_date = re.sub(p, '', movie_public_date)
        year_month_day = movie_public_date.split('-')                                     # 通过正则表达式和split函数将上映时间中得年月日分离
        # 获取指定 month 月份的链接
        if int(year_month_day[1]) == month:                                                # 根据月份进行判断
            movie_homepage_elements = soup.select('#app > div > div.movies-panel > div.movies-list > dl > dd > div.movie-item.film-channel > a')
            for movie_homepage_element in movie_homepage_elements:                          # 从目标词条中提取href属性的值，从而得到电影信息的url
                movie_homepage_href = movie_homepage_element.get('href').strip()
                movie_homepage_href = 'https://maoyan.com' + movie_homepage_href
                print(movie_homepage_href)
                get_movie_info(movie_homepage_href, year_month_day[0], year_month_day)                      # 将参数传入下一个得到电影信息的函数
#   得到对应链接在猫眼上的各种信息
def get_movie_info(movie_homepage_url, year, date):
    web_data = requests.get(url=movie_homepage_url, headers=request_headers)
    status_code = web_data.status_code
    if status_code == 200:
        html_text = web_data.text
        selector = etree.HTML(html_text)                                                    # 默认一套网页信息处理
        movie_Chinese_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')[0].strip()     # 电影中文名称
        print(movie_Chinese_name)
        movie_English_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/div/text()')[0].strip()    # 电影英文名称
        selenium_search_in_Douban_IMDb(movie_Chinese_name, movie_English_name, year, date)        # 分别在豆瓣和IMDb中根据 中文名称+年份/英文名称+年份进行区分



def selenium_search_in_Douban_IMDb(movie_Chinese_name, movie_English_name, year, date):
    browser = webdriver.Chrome()
    douban_url = "https://movie.douban.com/"
    browser.get(url=douban_url)     # 打开浏览器并进入目标url
    time.sleep(random.uniform(1.1, 2.6))
    inp_query_element = browser.find_element_by_id(id_="inp-query")     # 定位输入栏
    inp_query_element.send_keys(movie_Chinese_name)                     # 输入目标关键字
    submit_element = browser.find_element_by_xpath('//*[@id="db-nav-movie"]/div[1]/div/div[2]/form/fieldset/div[2]/input')      # 定位搜索按钮
    time.sleep(random.uniform(1.1, 2.6))
    submit_element.click()                                              # 点击搜索按钮
    time.sleep(random.uniform(1.1, 2.6))
    # current_url = browser.current_url

    target_link = browser.find_element_by_xpath('//a[contains(text(), "{}") and contains(text(), "{}")]'.format(movie_Chinese_name, year))  # 根据中文名称+年份定位
    target_link.click()
    time.sleep(random.uniform(1.1, 2.6))
    html_text = browser.page_source                                     # 获取网页源码
    selector = etree.HTML(html_text)                                    # 分析源码
    douban_movie_score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0].strip()     #获取豆瓣评分
    douban_movie_comment = selector.xpath('//*[@id="hot-comments"]/div[1]/div/p/span/text()')[0].strip()        #获取豆瓣置顶评论
    print(douban_movie_score, douban_movie_comment)

    # 将提取的信息存入CSV文件中
    csv_writer.writerow((movie_Chinese_name, movie_English_name, date, douban_movie_score, douban_movie_comment))
    # 输出程序执行的信息 ---使用日志输出
    logger.info(movie_Chinese_name)

    # 开始IMDb的搜索和poster的下载 与上面类似
    IMDb_url = "https://www.imdb.com/"
    browser.get(url=IMDb_url)
    time.sleep(random.uniform(1.1, 2.6))
    suggestion_search_element = browser.find_element_by_xpath('//*[@id="suggestion-search"]')
    suggestion_search_element.send_keys(movie_English_name)
    suggestion_search_button_element = browser.find_element_by_xpath('//*[@id="suggestion-search-button"]')
    time.sleep(random.uniform(1.1, 2.6))
    suggestion_search_button_element.click()
    time.sleep(random.uniform(1.1, 2.6))
    # 定位目标link
    p = Pinyin()
    imdb_target_link = browser.find_element_by_xpath('//a[contains(text(), "{}") or contains(text(), "{}") or contains(text(), "{}")]'.format(year, p.get_pinyin(movie_Chinese_name, " ").title(), movie_English_name))
    imdb_target_link.click()
    time.sleep(random.uniform(1.1, 2.6))

    html_text = browser.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    imdb_poster_uri_elements = soup.select('#title-overview-widget > div.vital > div.slate_wrapper > div.poster > a > img')
    for imdb_poster_uri_element in imdb_poster_uri_elements:
        imdb_poster_uri = imdb_poster_uri_element.get('src').strip()
        print(imdb_poster_uri)
        uri = imdb_poster_uri
        img_data_stream = urllib.request.urlopen(uri).read()
        img_file = uri.split("/")[-1]

    # img_file_path = "d:" + "\\" + img_file

        img_file_path = "d:" + os.sep + img_file

        with open(img_file_path, 'wb') as fp:
            fp.write(img_data_stream)
            print("End.......")

if __name__ == '__main__':
#
    csv_header = ('电影中文名称', '电影英文名称', '上映日期', '豆瓣评分', '豆瓣置顶评论')
    # 表头
    csv_writer.writerow(csv_header)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)



# 程序开端（除数据存储）
    urls = ['https://maoyan.com/films?yearId={}&showType=3&sortId=1&offset={}'.format(str(i), str(j)) for i in
            range(15, 14, -1) for j in range(0, 60, 30)]                    # 根据规律找到相应年份的相应页数
    for url in urls:
        get_per_page_26_movies_links(url, 8)                                # 通过自定义函数，将上述url传入，第二个参数含义为目标月份（默认设置成8月）
        time.sleep(2)


    # 测试    def selenium_search_in_Douban_IMDb(movie_Chinese_name, movie_English_name, year):
    # selenium_search_in_Douban_IMDb("八佰", "The Eight Hundred", 2020)