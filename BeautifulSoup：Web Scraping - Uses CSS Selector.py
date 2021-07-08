import requests as req
from bs4 import BeautifulSoup

# Load web pages into Python through requests
URL = 'https://pt.wikipedia.org/wiki/Rond%C3%B4nia'
r = req.get(URL)
soup = BeautifulSoup(r.content)

selector = "#mw-content-text > div.mw-parser-output > div:nth-child(49) > div > a > img"
print(soup.select(selector))

selector = ".thumbimage"
print(soup.select(selector, limit=3))

