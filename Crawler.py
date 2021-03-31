import requests
from requests.exceptions import RequestException
from lxml import etree
import pandas as pd
import numpy as np
import os
import re


class RatingCrawler():
    def __init__(self, path=''):
        self.column = [
            'Name', 'Club', 'League', 'Nation', 'Age', 'Height', 'Position',
            'Rating', 'PACE', 'SHOOTING', 'PASSING', 'DRIBBLING', 'DEFENCE',
            'PHYSICAL'
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
        if text:
            html = etree.HTML(text)
            return html
        else:
            return None

    def null_manage(self, feature: str) -> int:
        '''
        判断并处理空数据，最后转化为整型数

        :param feature: 文本
        :return: 整型数
        '''
        if feature:
            return int(feature[0])
        else:
            return np.nan

    def delete_nonwords(self, text: str) -> int:
        """
        去除文本中的非字符

        :param text: 文本
        :return: 去除空格、换行符后的文本
        """
        text = re.sub('\s', '', text)  # 去除非数字部分
        return text

    def get_player_url(self, page: str, reverse=False) -> list:
        """
        获取球员详细页列表, 在get_whole_player_url中进行调用

        :param page: 指定球员排名页面的页码
        :param reverse: 是否使用倒转页
        :return: 球员详细页的url列表
        """
        if not reverse:
            url = 'https://www.futhead.com/21/players/?page={}&level=all_nif&bin_platform=pc'.format(
                page)
        else:
            url = 'https://www.futhead.com/21/players/?sort=-rating&level=all_nif&page={}&bin_platform=pc'.format(
                page)
        try:
            html = self.switch2xpath(self.get_url_text(url))  # 获取排名页面的xpath对象
            url_list = html.xpath("//a[@class='display-block padding-0']/@href")
            url_list_completed = []
            # 补全url
            for url in url_list:
                url = r'https://www.futhead.com' + url
                url_list_completed.append(url)
            return url_list_completed
        except:
            return []

    def get_whole_player_url(self, page: int, reverse_page=0) -> list:
        """
        获取指定页面的球员详细页列表，并全部合并成一张大列表

        :param page_num: 正向爬取的页数
        :param reverse_page: 逆向爬取的页数
        :return: 球员详细页的url列表
        """
        url_list = []
        for i in range(1, page + 1):
            print('正在获取第{}页球员列表'.format(str(i)))
            url_list.extend(self.get_player_url(str(i)))
        if reverse_page > 0:
            for i in range(1, reverse_page + 1):
                print('正在获取倒数第{}页球员列表'.format(str(i)))
                url_list.extend(self.get_player_url(str(i), True))
        return url_list

    def parse_player_info(self, url: str) -> list:
        """TODO
        分析并获取单个球员信息, 在get_player_infos中进行调用

        :param url: 球员详细页url
        :return: 球员信息列表
        """
        try:
            # 构建xpath对象
            player = self.switch2xpath(self.get_url_text(url))
            one_piece = []
            # 全名
            full_name = player.xpath(
                "//ul[@class='list-group margin-b-8']//div[@class='font-16 fh-red']/a/text()"
            )[0]
            # 俱乐部
            club = player.xpath(
                "//ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()"
            )[0]
            # 联赛
            league = player.xpath(
                "//ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()"
            )[1]
            # 国籍
            nation = player.xpath(
                "//ul[@class='list-group margin-b-8']//div[@class='row player-sidebar-item']//a[@class='futhead-link']/text()"
            )[2]
            # 年龄
            age = player.xpath(
                "//div[@class='col-xs-7' and text()='Age']/../div[@class='col-xs-5 player-sidebar-value']/text()"
            )[0].split(' ', 1)[0]
            age = int(self.delete_nonwords(age))
            # 身高
            height = player.xpath(
                "//div[@class='col-xs-7' and text()='Height']/../div[@class='col-xs-5 player-sidebar-value']/text()"
            )[0].split('c', 1)[0]
            height = int(self.delete_nonwords(height))
            # 位置
            position = player.xpath(
                "//div[@class='row']//div[@class='playercard-position']/text()")[0]
            position = self.delete_nonwords(position)
            # 综合能力
            rating = player.xpath(
                "//div[@class='player-cards']//div[contains(@class,'playercard  fut21 card-large  nif') and @style=' ']//div[@class='playercard-rating']/text()"
            )[0]
            rating = int(self.delete_nonwords(rating))
            # 速度
            pace = player.xpath(
                "//div[@class='row']//div[@class='playercard-attr playercard-attr1']/span[@class='chembot-value']/text()"
            )
            pace = self.null_manage(pace)
            # 射门
            shooting = player.xpath(
                "//div[@class='row']//div[@class='playercard-attr playercard-attr2']/span[@class='chembot-value']/text()"
            )
            shooting = self.null_manage(shooting)
            # 传球
            passing = player.xpath(
                "//div[@class='row']//div[@class='playercard-attr playercard-attr3']/span[@class='chembot-value']/text()"
            )
            passing = self.null_manage(passing)
            # 过人
            dribbling = player.xpath(
                " //div[@class='row']//div[@class='playercard-attr playercard-attr4']/span[@class='chembot-value']/text()"
            )
            dribbling = self.null_manage(dribbling)
            # 防守
            defence = player.xpath(
                "//div[@class='row']//div[@class='playercard-attr playercard-attr5']/span[@class='chembot-value']/text()"
            )
            defence = self.null_manage(defence)
            # 体能
            physical = player.xpath(
                "//div[@class='row']//div[@class='playercard-attr playercard-attr6']/span[@class='chembot-value']/text()"
            )
            physical = self.null_manage(physical)
            # 头像地址
            picture = player.xpath(
                "//div[@class='row']//div[@class='playercard-picture']/img/@src"
            )[0]
            one_piece.append(full_name)
            one_piece.append(club)
            one_piece.append(league)
            one_piece.append(nation)
            one_piece.append(age)
            one_piece.append(height)
            one_piece.append(position)
            one_piece.append(rating)
            one_piece.append(pace)
            one_piece.append(shooting)
            one_piece.append(passing)
            one_piece.append(dribbling)
            one_piece.append(defence)
            one_piece.append(physical)
            # one_piece.append(picture)

            return one_piece
        except:
            return []

    def get_player_infos(self, url_list: list) -> list:
        """TODO
        整合所有球员信息成复合列表

        :param url_list: 球员详细页url列表
        :return: 球员信息复合列表
        """
        info_list = []
        for url in url_list:
            one_piece = self.parse_player_info(url)
            print('正在爬取第{}条球员信息'.format(url_list.index(url) + 1))
            if one_piece:
                info_list.append(one_piece)
        print('爬取完成！')
        return info_list

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

    def start(self):
        """
        集成功能函数
        """
        player_url_list = self.get_whole_player_url(208, 135)
        info_list = self.get_player_infos(player_url_list)
        df = self.switch2df(info_list)
        self.save_to_path(df)
