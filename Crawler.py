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
            'Name', 'Nation', 'Club', 'Position', 'Age', 'Birth', 'Height',
            'Weight', 'Jersey number', 'Strong feet', 'Value', 'Wage',
            'Release clause', 'Rating', 'Potential', 'PACE', 'SHOOTING',
            'PASSING', 'DRIBBLING', 'DEFENCE', 'PHYSICAL', 'crossing', 'finishing', 'heading accuracy',
            'short passing', 'volleys', 'dribbling skill', 'curve', 'fk accuracy', 'long passing',
            'ball control', 'acceleration', 'sprint speed', 'agility', 'reactions', 'balance', 'shot power',
            'jumping', 'stamina', 'strength', 'long shots', 'aggression', 'interceptions', 'positioning', 'vision',
            'penalties', 'composure', 'defensive_awareness', 'standing_tackle', 'sliding_tackle']

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

    def get_feature(self, xpath_obj, selector: str, is_int=False) -> str:
        """
        通过xpath语法获取特征字段

        :param xpath_obj: xpath对象
        :param selector: xpath语法字符串
        :return: 字符串型字段
        """
        feature = xpath_obj.xpath(selector)
        if is_int:
            if feature:
                try:
                    feature = int(feature[0])
                except:
                    feature = np.nan
            else:
                feature = np.nan
        else:
            if feature:
                feature = feature[0]
            else:
                feature = np.nan
        return feature

    def wage_manage(self, text: str) -> int:
        """
        处理金额数据

        :param text: 金额文本
        :return: 以k为单位的金额
        """
        try:
            text = re.sub('€', '', text)  # 去除欧元单位
            if text[-1].isdigit():
                text = float(text[:-1]) / 1000
            elif text[-1] == 'K':
                text = float(text[:-1])
            elif text[-1] == 'M':
                text = float(text[:-1]) * 1000
            else:
                text = np.nan
        except:
            text = np.nan
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
                url = r'https://sofifa.com' + url + r'?hl=en-US&attr=classic'
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
        for i in range(0, page * 60, 60):
            print('正在获取第{}页球员列表'.format(str(count)))
            count += 1
            url = "https://sofifa.com/players?type=all&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&pn%5B6%5D=18&pn%5B7%5D=16&pn%5B8%5D=14&pn%5B9%5D=12&pn%5B10%5D=10&pn%5B11%5D=8&pn%5B12%5D=7&pn%5B13%5D=5&pn%5B14%5D=3&pn%5B15%5D=2&col=oa&sort=desc&hl=en-US&offset={}".format(
                str(i))
            url_list.extend(self.get_player_url(str(i)))
        print('\n')
        return url_list

    def parse_player_info(self, url: str) -> list:
        """TODO
        分析并获取单个球员信息, 在get_player_infos中进行调用

        :param url: 球员详细页url
        :return: 球员信息列表
        """
        # 构建xpath对象
        player = self.switch2xpath(self.get_url_text(url))
        one_piece = []
        try:
            # 头像地址
            # photo = player.xpath(
            #     "//div[contains(@class,'player')]/img/@data-src"
            # )[0]

            # 名字
            name = self.get_feature(
                player,
                "//div[contains(@class,'player')]//div[@class='info']/h1/text()"
            )
            # 国籍
            nation = self.get_feature(
                player,
                "//div[contains(@class,'player')]//div[@class='info']/div/a/@title"
            )
            # 俱乐部
            club = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5//a/text()"
            )
            # 位置
            position = self.get_feature(
                player,
                "//div[contains(@class,'player')]//div[@class='info']//div/span[1]/text()"
            )

            # 信息字段
            info_str = self.get_feature(
                player,
                "//div[contains(@class,'player')]//div[@class='info']//div/text()[last()]"
            )
            # 年龄
            age = int(re.search(r"(\d+)y.o.", info_str).group(1))
            # 生日
            birth = re.search(r"[(](.*?)[)]", info_str).group(1)
            try:
                birth = time.strftime(r"%Y-%m-%d", time.strptime(birth, r"%b %d, %Y"))
            except:
                birth = np.nan
            # 身高
            height = re.search(r"(\d+'\d+)", info_str).group(1)
            height = int(
                float(height.split("'")[0]) * 2.54 * 12 +
                float(height.split("'")[1]) * 2.54)
            # 体重
            weight = int(
                float(re.search(r"(\d+)lbs", info_str).group(1)) * 0.454)
            # 俱乐部球衣号码
            jersey_number = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//li/label[text()='Jersey Number']/../text()"
            )
            # 惯用脚
            strong_feet = self.get_feature(
                player,
                "//div[@class='card']/h5[text()='Profile']/../ul/li/label[text()='Preferred Foot']/../text()"
            )
            release_clause = self.get_feature(
                player,
                " //div[@class='card']/h5[text()='Profile']/../ul/li/label[text()='Release Clause']/../span/text()"
            )
            release_clause = self.wage_manage(release_clause)
            # 综合能力
            rating = self.get_feature(
                player, "//section//div[@class='columns']/div[1]//span/text()",
                True)
            # 潜力
            potential = self.get_feature(
                player, "//section//div[@class='columns']/div[2]//span/text()",
                True)
            # 身价
            value = self.get_feature(
                player, "//section//div[@class='columns']/div[3]//div/text()")
            value = self.wage_manage(value)
            # 周薪
            wage = self.get_feature(
                player, "//section//div[@class='columns']/div[4]//div/text()")
            wage = self.wage_manage(wage)
            # 综合能力字段
            overall_str = self.get_feature(player,
                                           "//*[@id='list']/script[2]/text()")
            # 速度
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

            # 传中
            crossing = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Attacking']/../ul/li[1]/span/text()",
                True)
            # 射术
            finishing = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Attacking']/../ul/li[2]/span/text()",
                True)
            # 头球精度
            heading_accuracy = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Attacking']/../ul/li[3]/span/text()",
                True)
            # 短传
            short_passing = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Attacking']/../ul/li[4]/span/text()",
                True)
            # 凌空
            volleys = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Attacking']/../ul/li[5]/span/text()",
                True)

            # 盘带
            dribbling_skill = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Skill']/../ul/li[1]/span/text()",
                True)
            # 弧线
            curve = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Skill']/../ul/li[2]/span/text()",
                True)
            # 任意球精度
            fk_accuracy = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Skill']/../ul/li[3]/span/text()",
                True)
            # 长传
            long_passing = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Skill']/../ul/li[4]/span/text()",
                True)
            # 控球
            ball_control = self.get_feature(
                player,
                "//div[@class='column col-3']//div[@class='card']//h5[text()='Skill']/../ul/li[5]/span/text()",
                True)

            # 加速
            acceleration = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Movement']/../ul/li[1]/span/text()", True)
            # 最快速度
            sprint_speed = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Movement']/../ul/li[2]/span/text()", True)
            # 敏捷
            agility = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Movement']/../ul/li[3]/span/text()", True)
            # 反应
            reactions = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Movement']/../ul/li[4]/span/text()", True)
            # 平衡
            balance = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Movement']/../ul/li[5]/span/text()", True)

            # 射门力量
            shot_power = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Power']/../ul/li[1]/span/text()", True)
            # 弹跳
            jumping = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Power']/../ul/li[2]/span/text()", True)
            # 体能
            stamina = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Power']/../ul/li[3]/span/text()", True)
            # 强壮
            strength = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Power']/../ul/li[4]/span/text()", True)
            # 远射
            long_shots = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Power']/../ul/li[5]/span/text()", True)

            # 侵略性
            aggression = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[1]/span/text()", True)
            # 拦截意识
            interceptions = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[2]/span/text()", True)
            # 跑位
            positioning = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[3]/span/text()", True)
            # 视野
            vision = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[4]/span/text()", True)
            # 点球
            penalties = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[5]/span/text()", True)
            # 沉着
            composure = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[6]/span/text()", True)

            # 防守意识
            defensive_awareness = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Defending']/../ul/li[1]/span/text()", True)
            # 抢断
            standing_tackle = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Defending']/../ul/li[2]/span/text()", True)
            # 铲球
            sliding_tackle = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Defending']/../ul/li[3]/span/text()", True)

            one_piece.append(name)
            one_piece.append(nation)
            one_piece.append(club)
            one_piece.append(position)
            one_piece.append(age)
            one_piece.append(birth)
            one_piece.append(height)
            one_piece.append(weight)
            one_piece.append(jersey_number)
            one_piece.append(strong_feet)
            one_piece.append(value)
            one_piece.append(wage)
            one_piece.append(release_clause)
            one_piece.append(rating)
            one_piece.append(potential)
            one_piece.append(pace)
            one_piece.append(shooting)
            one_piece.append(passing)
            one_piece.append(dribbling)
            one_piece.append(defense)
            one_piece.append(physical)
            # 添加具体能力项
            one_piece.append(crossing)
            one_piece.append(finishing)
            one_piece.append(heading_accuracy)
            one_piece.append(short_passing)
            one_piece.append(volleys)
            one_piece.append(dribbling_skill)
            one_piece.append(curve)
            one_piece.append(fk_accuracy)
            one_piece.append(long_passing)
            one_piece.append(ball_control)
            one_piece.append(acceleration)
            one_piece.append(sprint_speed)
            one_piece.append(agility)
            one_piece.append(reactions)
            one_piece.append(balance)
            one_piece.append(shot_power)
            one_piece.append(jumping)
            one_piece.append(stamina)
            one_piece.append(strength)
            one_piece.append(long_shots)
            one_piece.append(aggression)
            one_piece.append(interceptions)
            one_piece.append(positioning)
            one_piece.append(vision)
            one_piece.append(penalties)
            one_piece.append(composure)
            one_piece.append(defensive_awareness)
            one_piece.append(standing_tackle)
            one_piece.append(sliding_tackle)

            return one_piece
        except:
            return []

    def get_player_infos(self, url_list: list) -> list:
        """
        整合所有球员信息成复合列表

        :param url_list: 球员详细页url列表
        :return: 球员信息复合列表
        """
        info_list = []
        error_count = 0
        for url in url_list:
            print('正在爬取第{}条球员信息'.format(url_list.index(url) + 1))
            one_piece = self.parse_player_info(url)

            if one_piece:
                print("第{}条: ".format(url_list.index(url) + 1), one_piece,
                      '\n')
                info_list.append(one_piece)
            else:
                print("第{}条爬取失败!\n".format(url_list.index(url) + 1))
                error_count += 1
        print('爬取完成!\n爬取成功{}条\n爬取失败{}条'.format(
            len(url_list) - error_count, error_count))
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

    def start(self, pages: int):
        """
        集成功能函数
        :param pages: 爬取页数
        """
        player_url_list = self.get_whole_player_url(int(pages))
        info_list = self.get_player_infos(player_url_list)
        df = self.switch2df(info_list)
        self.save_to_path(df)
