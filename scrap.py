# -*- coding:utf8 -*-


from bs4 import BeautifulSoup
import urllib2
import re


thread = 'http://tieba.baidu.com/p/4760750844?pn='


def gen_req(url):
    req = urllib2.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req


def scrap_page(page_num):
    url = thread + str(page_num)
    req = gen_req(url)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    divs = soup.find_all('div', class_='d_post_content j_d_post_content ')
    key_words = ['青轴', '樱桃', '茶轴']
    black_list = [84, 87, 104, 99]
    print 'Is going to find'
    for div in divs:
        found = False
        for word in key_words:
            if word in str(div):
                found = True
                break
        if found:
            # check price

            price_ok = False
            numbers = map(int, re.findall(r'\d+', div.text))
            if u'价格' in div.text:
                price_string = re.findall(ur'价格.*\d+', div.text)
                if price_string:
                    prices = map(int, re.findall(r'\d+', price_string[0]))
                    if prices and 50 < prices[0] < 180:
                        price_ok = True
            else:
                for num in numbers:
                    if 50 < num < 180 and num not in black_list:
                        price_ok = True
            if price_ok:
                print numbers
                print div.text


if __name__ == '__main__':
    for i in range(0, 7):
        scrap_page(i)
