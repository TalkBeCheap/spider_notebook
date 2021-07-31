import requests

url = "http://www.glidedsky.com/level/web/crawler-basic-1"

r = requests.get(url)
print(r.text)
