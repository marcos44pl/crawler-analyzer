import threading
import time
from queue import Queue

from domain import *
from general import *
from spider import Spider

end_flag = False


class ParallelCrawler:
    NUMBER_OF_THREADS = 32

    def __init__(self, homepage, project_name, save_flag):
        self.save_flag = save_flag
        self.home_page = homepage
        self.project_name = project_name
        self.domain_name = get_domain_name(homepage)
        self.queue_file = project_name + '/queue.txt'
        self.crawled_file = project_name + '/crawled.txt'
        self.queue = Queue()

    def crawl(self):
        try:
            start = time.time()
            Spider(self.project_name, self.home_page, self.domain_name, self.save_flag)
            self._create_workers()
            self._crawl()
            end = time.time()
            print("Time elapsed: ", end - start)
        finally:
            Spider.graph.save()

    def _create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self._work)
            t.daemon = True
            t.start()

    def _work(self):
        global end_flag
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    def _create_jobs(self):
        for link in file_to_set(self.queue_file):
            self.queue.put(link)
        self.queue.join()
        self._crawl()

    def _crawl(self):
        queued_links = file_to_set(self.queue_file)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + ' links in the queue')
            self._create_jobs()
