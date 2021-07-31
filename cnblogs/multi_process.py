import requests
from lxml import etree
from fake_useragent import UserAgent
import logging
import threading
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(filename)s %(processName)s %(threadName)s : %(levelname)s  %(message)s ',
    datefmt='%Y-%m-%d %A %H:%M:%S')


def get_text(url):
    headers = {"User-Agent": UserAgent().chrome}
    r = requests.get(url, headers=headers)
    return r.text


def parse_text(text):
    tree = etree.HTML(text)
    hrefs = tree.xpath("//div[@class='post-item-text']/a/@href")
    titles = tree.xpath("//div[@class='post-item-text']/a/text()")
    string = []
    output = ''
    for (title, href) in zip(titles, hrefs):
        # print(href, title)
        output = title + '  ' + href
        string.append(output)
    # logging.info(string)
    return string


def save_date(data):
    with open("./mp_main.txt", 'a', encoding='utf-8') as f:
        for i in data:
            f.write(i)
            f.write('\n')


def main(url):
    text = get_text(url)
    data = parse_text(text)
    save_date(data)


if __name__ == "__main__":

    import time
    start_time = time.time()
    urls = [f'https://www.cnblogs.com/sitehome/p/{i}' for i in range(1, 50)]
    pool = multiprocessing.Pool()
    pool.map(main, urls)
    pool.close()
    end_time = time.time()
    logging.info(f"合计用时间:{end_time - start_time}")
