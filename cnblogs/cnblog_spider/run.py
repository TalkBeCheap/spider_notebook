from scrapy import cmdline


def main():
    cmdline.execute(
        'scrapy crawl cnblog -o scrapy.csv -a page=10'.split())


if __name__ == '__main__':
    main()
