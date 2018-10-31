import requests
import re
from urllib.robotparser import RobotFileParser
from abc import ABCMeta, abstractmethod
from queue import PriorityQueue
from bs4 import BeautifulSoup

class Spider(metaclass = ABCMeta):
    def __init__(self, basicUrl, pageLimit, level):
        self._basicUrl = basicUrl
        self._robotParser = RobotFileParser()
        self._urlRegex = re.compile(basicUrl)
        self._pageCount = pageLimit #A limit of pages
        self._pageHeap = PriorityQueue()
        self._visited = set()
        self._level = level

    def _searchPages(self, startPage):
        page = (0, startPage)
        self._pageHeap.put_nowait(page) #Inserting the first page to be crawled
        while not self._pageHeap.empty() and self._pageCount >= 0:
            _, currPage = self._pageHeap.get_nowait() #Get the current page. The first element of the 2-uple is useless here
            currPage = self._cleanUrl(currPage)
            self._crawlPage(currPage)

    def _crawlPage(self, page):
        #Put pages in the heap
        #print(page + 'en/', self._robotParser.can_fetch('*', page+'en/'))
        if not page in self._visited and self._robotParser.can_fetch('*', page):
            self._visited.add(page) #Prevent revisiting this page
            self._pageCount -= 1
            print(page)
            pageText = requests.get(page).text
            soupObject = BeautifulSoup(pageText, 'html.parser')
            self._downloadPage(soupObject)
            for link in soupObject.findAll('a', href = True): #Search every link on the current page
                href = link.get('href')
                if self._checkRegex(href) and not href in self._visited and self._pageCount >= 0:
                    href = self._fixUrl(href)
                    hrefSoup = None
                    if self._level > 1:
                        hrefText = requests.get(href).text
                        hrefSoup = BeautifulSoup(hrefText, 'html.parser')
                    rank = self._getRank(hrefSoup, href, level = self._level)
                    self._pageHeap.put_nowait((-rank, href))

    def _checkRegex(self, page):
        #Check if this page is relevant by matching the basicRegex with the page url
        return re.match(self._urlRegex, page)

    @abstractmethod
    def _downloadPage(self, soupObject):
        #Method to download pages
        pass
    
    @abstractmethod
    def _getRank(self, soupObject, url, level):
        #Method to priorize game pages
        pass

    @abstractmethod
    def _cleanUrl(self, url):
        #Method to remove noise
        pass

    @abstractmethod
    def _fixUrl(self, url):
        #Fix some pruned url
        pass

    def run(self):
        self._robotParser.set_url(self._basicUrl + 'robots.txt')
        self._robotParser.read()
        self._searchPages(self._basicUrl)