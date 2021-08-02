import requests
import parsel
import urllib3

urllib3.disable_warnings()

for page in range(1, 326):
    url = f"https://www.phei.com.cn/module/goods/searchkey.jsp?Page={page}&goodtypeid=1goodtypename=%E8%AE%A1%E7%AE%97%E6%9C%BA"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh)Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    r = requests.get(url, headers=headers, verify=False)

    print(url, r.status_code, len(r.text))
    selector = parsel.Selector(r.text)
    infos = selector.css("div.book_list_area li")
    for info in infos:
        base_url = "https://www.phei.com.cn"
        title = info.css("span.book_title>a::text").get()
        href = base_url + info.css("span.book_title>a::attr(href)").get()
        author = info.css("span.book_author::text").get()
        price = info.css("span.book_price>b::text").get()
        print(title, author, price, href)
