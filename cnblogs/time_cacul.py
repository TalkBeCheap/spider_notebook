from single_thread import main as s_main
from multi_process import main as mp_main
from multi_thread import main as mt_main
from time import time
from functools import wraps
import threading
import multiprocessing
from cnblog_spider.run import main as scrapy_main


def run_time(func):
    @wraps(func)                                # <- 这里加 wraps(func) 即可
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)                  # 函数在这里运行
        end = time()
        cost_time = end - start
        print(f"{func.__doc__} const time {cost_time}")
    return wrapper


@run_time
def test_s_main(page):
    "单线程版本测试"

    for url in urls:
        s_main(url)


@run_time
def test_mt_main(page):
    "多线程版本测试"
    for url in urls:
        t = threading.Thread(target=mt_main, args=(url,))
        t.start()
        t.join()


@run_time
def test_mp_main(page):
    "多进程版本测试"
    pool = multiprocessing.Pool()
    pool.map(mt_main, urls)
    pool.close()


if __name__ == '__main__':
    for page in range(5, 100, 10):
        urls = [
            f'https://www.cnblogs.com/sitehome/p/{i}' for i in range(1, page + 1)]
        print(f"当前页数{page}")
        test_s_main(page)
        test_mt_main(page)
        test_mp_main(page)
