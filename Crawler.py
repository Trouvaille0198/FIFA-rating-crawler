import requests
from requests.exceptions import RequestException
from lxml import etree
import pandas as pd
import numpy as np
import os


class RatingCrawler():
    def __init__(self, path=''):
        self.column = [
            'Name', 'Club', 'League', 'Nation', 'Age', 'Height', 'Position',
            'Rating', 'PACE', 'SHOOTING', 'PASSING', 'DRIBBLING', 'DEFENCE',
            'PHYSICAL', 'Picture'
        ]

    if path != '':
        self.path = path
    else:
        self.path = os.getcwd()

    def get_url_text(self, url: str) -> str:
        """
        获取单个页面的html文本
        
        :param url: 地址
        :return: 文本
        """
        try:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            if (response.status_code == 200):
                return response.text
            return None
        except RequestException:
            return None

    def switch2xpath(self, text: str) -> etree.HTML:
        """
        将html文本转换为xpath解析对象
        
        :param text: 文本
        :return: xpath对象
        """
        html = etree.HTML(url_text)
        return html

    def get_player_url(self, url: str, reverse=False) -> list:
        """
        获取球员详细页列表, 在get_whole_player_url中进行调用
        
        :param url: 球员排名页url
        :param reverse: 是否使用倒转页
        :return: 球员详细页的url列表
        """

    def get_whole_player_url(self, page: int, reverse_page=0) -> list:
        """
        获取指定页面的球员详细页列表，并全部合并成一张大列表
        
        :param url: 球员排名页url
        :param page: 正向爬取的页数
        :param reverse_page: 逆向爬取的页数
        :return: 球员详细页的url列表
        """

    def parse_player_info(self, url: str) -> list:
        """
        分析并获取单个球员信息, 在get_player_infos中进行调用
        
        :param url: 球员详细页url
        :return: 球员信息列表
        """

    def get_player_infos(self, url_list: list) -> list:
        """
        整合所有球员信息成复合列表
        
        :param url_list: 球员详细页url列表
        :return: 球员信息复合列表
        """

    def switch2df(self, player_list: list) -> pd.DataFrame:
        """
        将球员信息复合列表转换成DataFrame格式
        
        :param player_list: 球员信息复合列表
        :return: 球员信息DataFrame
        """
        df = pd.DataFrame(player_list, columns=self.column)
        return df

    def save_to_path(self, df):
        """
        保存球员信息表
        
        :param df:球员信息表
        """
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        df.to_csv(self.path + '/players_info.csv',
                  index=False,
                  encoding="utf-8-sig")
        print('已保存至' + self.path + '\\players_info.csv')