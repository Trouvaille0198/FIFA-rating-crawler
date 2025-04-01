from Crawler import RatingCrawler
import numpy as np
import threading


def thread_it(func, *args):
    """将函数打包进线程"""
    t = threading.Thread(target=func, args=args)
    t.daemon = True  # 守护
    # t.setDaemon(True)  # 守护
    t.start()


Crawler = RatingCrawler()
thread_it(Crawler.start(1))
