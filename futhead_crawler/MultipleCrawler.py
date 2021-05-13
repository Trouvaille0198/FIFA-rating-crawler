from lxml import etree
import requests
import json
import requests
from requests.exceptions import RequestException
import re
import time


def get_player_url(page: str, reverse=False) -> list:
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
        txt = get_one_page(url)
        html = etree.HTML(txt)
        url_list = html.xpath("//a[@class='display-block padding-0']/@href")
        url_list_completed = []
        # 补全url
        for url in url_list:
            url = r'https://www.futhead.com' + url
            url_list_completed.append(url)
        return url_list_completed
    except:
        return []


def get_whole_player_url( page: int, reverse_page=0) -> list:
    """
    获取指定页面的球员详细页列表，并全部合并成一张大列表

    :param page_num: 正向爬取的页数
    :param reverse_page: 逆向爬取的页数
    :return: 球员详细页的url列表
    """
    url_list = []
    for i in range(1, page + 1):
        print('正在获取第{}页球员列表'.format(str(i)))
        url_list.extend(get_player_url(str(i)))
    if reverse_page > 0:
        for i in range(1, reverse_page + 1):
            print('正在获取倒数第{}页球员列表'.format(str(i)))
            url_list.extend(get_player_url(str(i), True))
    return url_list


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + ' ')


def get_one_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(txt):
    html = etree.HTML(txt)
    name = html.xpath(
        "//div[@itemprop='child']/span[@itemprop='title' ]/text()")
    age = html.xpath(
        "//div[@class='row player-sidebar-item']/div[@class='col-xs-7' and text()='Age']/../div[@class='col-xs-5 player-sidebar-value']/text()")
    height = html.xpath(
        "//div[@class='row player-sidebar-item']/div[@class='col-xs-7' and text()='Height']/../div[@class='col-xs-5 player-sidebar-value']/text()")
    infos = html.xpath(
        "//div[@class='row player-sidebar-item'] /div[@class='col-xs-5 player-sidebar-value']/text()")
    club = html.xpath(
        "//div[@class='col-xs-5 player-sidebar-value']/a[@class='futhead-link' ]/text()")
    pace = html.xpath(
        "//div[@class='playercard-attr playercard-attr1']/span[@class='chembot-value' ]/text()")
    acceleration = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Acceleration']/../span[contains(@class,'player-stat-value ')]/text()")
    SprintSpeed = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Sprint Speed']/../span[contains(@class,'player-stat-value ')]/text()")
    shooting = html.xpath(
        "//div[@class='playercard-attr playercard-attr2']/span[@class='chembot-value' ]/text()")
    pos = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Positioning']/../span[contains(@class,'player-stat-value ')]/text()")
    fini = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Finishing']/../span[contains(@class,'player-stat-value ')]/text()")
    shotpower = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Shot Power']/../span[contains(@class,'player-stat-value ')]/text()")
    longs = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Long Shots']/../span[contains(@class,'player-stat-value ')]/text()")
    vol = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Volleys']/../span[contains(@class,'player-stat-value ')]/text()")
    pen = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Penalties']/../span[contains(@class,'player-stat-value ')]/text()")
    passing = html.xpath(
        "//div[@class='playercard-attr playercard-attr3']/span[@class='chembot-value' ]/text()")
    vis = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Vision']/../span[contains(@class,'player-stat-value ')]/text()")
    cros = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Crossing']/../span[contains(@class,'player-stat-value ')]/text()")
    freekick = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Free Kick']/../span[contains(@class,'player-stat-value ')]/text()")
    shortp = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Short Passing']/../span[contains(@class,'player-stat-value ')]/text()")
    longp = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Long Passing']/../span[contains(@class,'player-stat-value ')]/text()")
    curve = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Curve']/../span[contains(@class,'player-stat-value ')]/text()")
    drib = html.xpath(
        "//div[@class='playercard-attr playercard-attr4']/span[@class='chembot-value' ]/text()")
    agi = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Agility']/../span[contains(@class,'player-stat-value ')]/text()")
    bal = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Balance']/../span[contains(@class,'player-stat-value ')]/text()")
    react = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Reactions']/../span[contains(@class,'player-stat-value ')]/text()")
    ballcon = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Ball Control']/../span[contains(@class,'player-stat-value ')]/text()")
    dribble = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Dribbling']/../span[contains(@class,'player-stat-value ')]/text()")
    com = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Composure']/../span[contains(@class,'player-stat-value ')]/text()")
    defen = html.xpath(
        "//div[@class='playercard-attr playercard-attr5']/span[@class='chembot-value' ]/text()")
    inter = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Interceptions']/../span[contains(@class,'player-stat-value ')]/text()")
    heading = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Heading']/../span[contains(@class,'player-stat-value ')]/text()")
    daw = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Def. Awareness']/../span[contains(@class,'player-stat-value ')]/text()")
    standtk = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Standing Tackle']/../span[contains(@class,'player-stat-value ')]/text()")
    slidtk = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Sliding Tackle']/../span[contains(@class,'player-stat-value ')]/text()")
    phy = html.xpath(
        "//div[@class='playercard-attr playercard-attr6']/span[@class='chembot-value' ]/text()")
    jmp = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Jumping']/../span[contains(@class,'player-stat-value ')]/text()")
    sta = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Stamina']/../span[contains(@class,'player-stat-value ')]/text()")
    str = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Strength']/../span[contains(@class,'player-stat-value ')]/text()")
    agg = html.xpath(
        "//div[@class='divided-row player-stat-row sm']/span[@class='player-stat-title' and text()='Aggression']/../span[contains(@class,'player-stat-value ')]/text()")
    ages = age[0]
    heights = height[0]
    try:
        items = [
            name[0],
            club[0],  # club
            club[2],  # nation
            infos[6],  # strong foot
            int(ages[0:2]),
            int(heights[0:3]),
            int(pace[0]),
            int(shooting[0]),
            int(passing[0]),
            int(drib[0]),
            int(defen[0]),
            int(phy[0]),
            int(acceleration[0]),
            int(SprintSpeed[0]),
            int(pos[0]),
            int(fini[0]),
            int(shotpower[0]),
            int(longs[0]),
            int(vol[0]),
            int(pen[0]),
            int(vis[0]),
            int(cros[0]),
            int(freekick[0]),
            int(shortp[0]),
            int(longp[0]),
            int(curve[0]),
            int(agi[0]),
            int(bal[0]),
            int(react[0]),
            int(ballcon[0]),
            int(dribble[0]),
            int(com[0]),
            int(inter[0]),
            int(heading[0]),
            int(daw[0]),
            int(standtk[0]),
            int(slidtk[0]),
            int(jmp[0]),
            int(sta[0]),
            int(str[0]),
            int(agg[0])
        ]
        return items
    except:
        items = []


def get_player_infos( UrlList: list):
    InfoList = []
    for url in UrlList:
        txt = get_one_page(url)
        OneUrl = parse_one_page(txt)
        print('正在爬取第{}条球员信息'.format(UrlList.index(url) + 1))
        if OneUrl:
            InfoList.append(OneUrl)
    print('爬取完成！')
    return InfoList


def main():
    player_url_list = get_whole_player_url(2)
    info_list = get_player_infos(player_url_list)
    write_to_file(info_list)




main()
