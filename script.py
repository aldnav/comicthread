import requests
import threading
from bs4 import BeautifulSoup


class XKCD(threading.Thread):

    def run(self):
        r = requests.get('https://c.xkcd.com/random/comic')
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        url = soup.find(id='comic').find('img')['src']
        print(f'https:{url}')


class CommitStrip(threading.Thread):

    def run(self):
        r = requests.get('http://www.commitstrip.com/?random=1')
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup.find_all(class_='entry-content')[0].find('img')['src'])


class Node(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xkcd = XKCD()
        self.commitstrip = CommitStrip()
        self.daemon = False

    def run(self):
        self.xkcd.start()
        self.commitstrip.start()

        self.xkcd.join()
        self.commitstrip.join()


if __name__ == '__main__':
    # Get xkcd
    # Get commitstrip
    node = Node()
    node.start()
