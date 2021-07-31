import requests
from lxml import etree
import urllib3
import json
import logging
import threading

urllib3.disable_warnings()  # 忽略requests验证错误
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s %(processName)s %(threadName)s : %(levelname)s  %(message)s ',
    datefmt='%Y-%m-%d %A %H:%M:%S')


def get_text(url):
    response = requests.get(url, verify=False)
    logging.debug(response.url)
    text = response.text
    return text


def text_parser(text):
    data = {}
    tree = etree.HTML(text)
    title = tree.xpath("//h2[@class='m-b-sm']/text()")[0]
    score = tree.xpath("//p[contains(@class,'score')]/text()")[0].strip()
    country = tree.xpath(
        "//div[contains(@class,'info')]/span[1]/text()")[0]
    try:
        time = "None"
        time = tree.xpath(
            "//div[contains(@class,'info')]/span[1]/text()")[1].split(" ")[0]
    except IndexError:
        time = "None"
    duration = tree.xpath(
        "//div[contains(@class,'info')]/span[3]/text()")[0]
    img_url = tree.xpath("//div[contains(@class,'item')]//img/@src")[0]
    data = {
        "title": title,
        "score": score,
        "time": time,
        "country": country,
        "duration": duration,
        "img_url": img_url,
    }
    logging.debug(data)
    return data


def save_date(data):
    with open("./ssr1_multi_thead_demo2.json", 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))


def process(url):
    text = get_text(url)
    data = text_parser(text)
    # self.save_date(data)


if __name__ == '__main__':
    import time
    urls = [
        f'https://ssr2.scrape.center/detail/{i}' for i in range(1, 101)]
    start_time = time.time()

    # semaphore = threading.BoundedSemaphore(10)
    for url in urls:
        t = threading.Thread(target=process, args=(url, ))
        t.start()
        t.join()
    end_time = time.time()
    logging.info(f"合计用时间:{end_time - start_time}")
