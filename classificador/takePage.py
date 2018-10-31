import requests as rq
from bs4 import BeautifulSoup

headers = {'user-agent': 'Rodrigo'}
#url of the html page
url = ''
r = rq.get(url, headers=headers)
page = BeautifulSoup(r.text, "html.parser")

#Y = 'negative' or 'positive'

#X = number of the html page
# foldername = name of the site
with open("foldername/YPages/pageX.html", "w") as file:
    file.write(str(page))
