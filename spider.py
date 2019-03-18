from urllib.request import urlopen
from urllib.robotparser import RobotFileParser

from domain import *
from general import *
from graph import Graph
from html_parser import HtmlParser


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    graph = None
    robot_parser = RobotFileParser()
    save_html = False
    maxNodes = 600

    def __init__(self, project_name, base_url, domain_name, save_html):
        Spider.save_html = save_html
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.graph = Graph(Spider.project_name)
        Spider.robot_parser.set_url(base_url + 'robots.txt')
        Spider.robot_parser.read()
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            links, html_doc = Spider.parse_html(page_url)
            Spider.graph.add_ts(page_url, links)
            if len(Spider.crawled) < Spider.maxNodes:
                Spider.add_links_to_queue(page_url, links)
            if Spider.save_html:
                with open(os.path.join(Spider.project_name, "%d.html" % len(Spider.crawled)), "w") as doc:
                    doc.write(html_doc)
            if page_url in Spider.queue:
                Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def parse_html(page_url):
        html_string = ''
        try:
            response = urlopen(page_url, timeout=5)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = HtmlParser(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set(), html_string
        return finder.page_links(), html_string

    @staticmethod
    def add_links_to_queue(current, links):
        for url in links:
            if not Spider.robot_parser.can_fetch("*", url):
                continue
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
