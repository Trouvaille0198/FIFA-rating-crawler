import requests
from requests.exceptions import RequestException
from lxml import etree
import pandas as pd
import numpy as np
import os
import re
import time


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

    def get_player_url(self, offset: str) -> list:
        """
        获取球员详细页列表, 在get_whole_player_url中进行调用

        :param offset: 页码偏移量,最大18900
        :return: 球员详细页的url列表
        """
        url = "https://sofifa.com/players?type=all&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&pn%5B6%5D=18&pn%5B7%5D=16&pn%5B8%5D=14&pn%5B9%5D=12&pn%5B10%5D=10&pn%5B11%5D=8&pn%5B12%5D=7&pn%5B13%5D=5&pn%5B14%5D=3&pn%5B15%5D=2&col=oa&sort=desc&hl=en-US&offset={}".format(
            offset)
        try:
            html = self.switch2xpath(self.get_url_text(url))  # 获取排名页面的xpath对象
            url_list = html.xpath("//table//tr//a[@class='tooltip']/@href")
            url_list_completed = []
            # 补全url
            for url in url_list:
                url = r'https://sofifa.com'+url+r'?hl=en-US'
                url_list_completed.append(url)
            return url_list_completed
        except:
            return []

    def get_whole_player_url(self, page: int) -> list:
        """
        获取指定页面的球员详细页列表，并全部合并成一张大列表

        :param page_num: 爬取的页数,最大315页
        :return: 球员详细页的url列表
        """
        url_list = []
        count = 1
        for i in range(0, page*60, 60):
            print('正在获取第{}页球员列表'.format(str(count)))
            count += 1
            url = "https://sofifa.com/players?type=all&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&pn%5B6%5D=18&pn%5B7%5D=16&pn%5B8%5D=14&pn%5B9%5D=12&pn%5B10%5D=10&pn%5B11%5D=8&pn%5B12%5D=7&pn%5B13%5D=5&pn%5B14%5D=3&pn%5B15%5D=2&col=oa&sort=desc&hl=en-US&offset={}".format(
                str(i))
            url_list.extend(self.get_player_url(str(i)))
        return url_list

    def parse_player_info(self, url: str) -> list:
        """TODO
        分析并获取单个球员信息, 在get_player_infos中进行调用

        :param url: 球员详细页url
        :return: 球员信息列表
        """
        # try:
        # 构建xpath对象
        player = self.switch2xpath(self.get_url_text(url))
        one_piece = []

        # 头像地址
        # photo = player.xpath(
        #     "//div[contains(@class,'player')]/img/@data-src"
        # )[0]

        # 名字
        name = player.xpath("//div[contains(@class,'player')]//div[@class='info']/h1/text()")[0]
        # 国籍
        nation = player.xpath("//div[contains(@class,'player')]//div[@class='info']/div/a/@title")[0]
        # 位置
        position = player.xpath("//div[contains(@class,'player')]//div[@class='info']//div/span[1]/text()")[0]
        # 信息字段
        info_str = player.xpath("//div[contains(@class,'player')]//div[@class='info']//div/text()[last()]")[0]
        # 年龄
        age = int(re.search(r"(\d+)y.o.", info_str).group(1))
        # 生日
        birth = re.search(r"[(](.*?)[)]", info_str).group(1)
        # 身高
        height = re.search(r"(\d+'\d+)", info_str).group(1)
        # 体重
        weight = re.search(r"(\d+)lbs", info_str).group(1)

        # 综合能力字段
        overall_str = player.xpath(
            "//*[@id='list']/script[2]/text()"
        )[0]
        pace = int(re.search('POINT_PAC=(\d+)', overall_str).group(1))
        # 射门
        shooting = int(re.search('POINT_SHO=(\d+)', overall_str).group(1))
        # 传球
        passing = int(re.search('POINT_PAS=(\d+)', overall_str).group(1))
        # 盘带
        dribbling = int(re.search('POINT_DRI=(\d+)', overall_str).group(1))
        # 防守
        defense = int(re.search('POINT_DEF=(\d+)', overall_str).group(1))
        # 力量
        physical = int(re.search('POINT_PHY=(\d+)', overall_str).group(1))

        one_piece.append(pace)
        one_piece.append(shooting)
        one_piece.append(passing)
        one_piece.append(dribbling)
        one_piece.append(defense)
        one_piece.append(physical)
        one_piece.append(name)
        one_piece.append(nation)
        one_piece.append(position)
        one_piece.append(age)
        one_piece.append(birth)
        one_piece.append(height)
        one_piece.append(weight)

        print(one_piece)
        return one_piece
        # except:
        #     return []

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
        """TODO
        将球员信息复合列表转换成DataFrame格式

        :param player_list: 球员信息复合列表
        :return: 球员信息DataFrame
        """
        df = pd.DataFrame(player_list, columns=self.column)
        return df

    def save_to_path(self, df):
        """TODO
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
        """TODO
        集成功能函数
        """
        player_url_list = self.get_whole_player_url(208, 135)
        info_list = self.get_player_infos(player_url_list)
        df = self.switch2df(info_list)
        self.save_to_path(df)
