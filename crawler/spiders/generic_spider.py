import requests
from bs4 import BeautifulSoup
from queue import Queue
import re

class Generic_Spider():
    def __init__(self):
        self.__urls = ['https://store.steampowered.com/', 'https://www.nuuvem.com/']
        self.__url_regex = re.compile("^http.*") # Regex to match an url

    def searchPages(self):
        # Performs a BFS on a base page and download every visited page from them
        for url in self.__urls:
            url_visited = {} #Avoid download the same html
            queue = Queue()
            queue.put_nowait(url)
            name_regex = re.compile('/.*\.com')
            start, end = name_regex.search(url).span()
            name = url[start+2:end-4]
            while len(url_visited) <= 3 and not queue.empty():
                curr_url = queue.get_nowait()
                if url_visited.get(curr_url, False):
                    continue
                url_visited[curr_url] = True
                curr_html = requests.get(curr_url)
                curr_html_text = curr_html.text
                soup = BeautifulSoup(curr_html_text, "html.parser")
                print(curr_url)
                self.__downloadPage(name + str(len(url_visited)), curr_url, soup)
                # Get every link on the current html and adds it on the set and the 'queue'
                for link in soup.findAll('a', href = True):
                    href = link.get('href')
                    if re.match(self.__url_regex, href):
                            print(href)
                            queue.put_nowait(href)

    def __downloadPage(self, name, url, curr_html_soup):
        html_path = open('pages/' + name + '.html', 'wb')
        html_path.write(curr_html_soup.encode('utf-8'))
        html_path.close()

def main():
    crawler = Generic_Spider()
    crawler.searchPages()

if __name__ == '__main__':
    main()
                    