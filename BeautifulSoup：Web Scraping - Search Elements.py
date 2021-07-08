import requests as req
from bs4 import BeautifulSoup

# Load web pages into Python through requests
URL = 'https://pt.wikipedia.org/wiki/Ariquemes'
r = req.get(URL)
print(r.content[:2000])

soup = BeautifulSoup(r.content)
print(soup.prettify())

# Access elements and attributes inside HTML pages
title = soup.h1
print(title)

tables = soup.find_all("table")
print(len(tables))
print(tables[1])
print(tables[1]["style"])

lists = soup.find_all("li")
print(len(lists))

childs = list(lists[3].children)
print(len(childs))
print(childs)

# Search elements with given classes and attributes
links = soup.find_all("a")
print(len(links))
print(links[0:3])

attributes_fliter = {"class": "mw-jump-link"}
attributes = soup.find_all("a", attributes_fliter)
print(attributes)

links_filter = {"rel": "alternate", "title": "Editar"}
links = soup.find_all("link", links_filter)
print(links)

elements_filter = {"class": "noprint"}
elements = soup.find_all(None, elements_filter)
print(elements)

classes_filter = {"class": "fn"}
classes = soup.find_all(None, classes_filter)
print(classes)

ids_filter = {"id": "firstHeading"}
ids = soup.find_all(None, ids_filter)
print(ids)
