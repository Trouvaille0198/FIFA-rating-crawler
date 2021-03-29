from Crawler import RatingCrawler

Crawler = RatingCrawler()
list = Crawler.get_whole_player_url(2, 1)
for url in list:
    print(url)