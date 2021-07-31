import requests
from lxml import etree
from fake_useragent import UserAgent
import logging
import threading
from queue import Queue

logging.basicConfig(
    level=logging.DEBUG,
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
    logging.info(string)
    return string


def save_date(data):
    with open("./result.txt", 'a', encoding='utf-8') as f:
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
    url_queue = Queue()
    urls = [f'https://www.cnblogs.com/sitehome/p/{i}' for i in range(1, 50)]

    for url in urls:
        url_queue.put(url)

    while not url_queue.empty():   # 若队列不为空继续运行
        url = url_queue.get()
        logging.info(f"当前地址:{url}")
        t = threading.Thread(target=main, args=(url,))
        t.start()
        t.join()
    end_time = time.time()
    logging.info(f"合计用时间:{end_time - start_time}")
