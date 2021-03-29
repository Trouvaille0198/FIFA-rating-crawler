# FIFA-rating-crawler

## 目标内容
- 正数url
    https://www.futhead.com/21/players/?page={}&level=all_nif&bin_platform=pc
    1-209
- 倒数url
    https://www.futhead.com/21/players/?sort=-rating&level=all_nif&page={}&bin_platform=pc
    1-136
- 具体内容页
    https://www.futhead.com/21/players/20406/

## Xpath
- 球员详情页
    //div[@class='row']//div[@class='col-flex-300']/ul/li/div/a[@class='display-block padding-0']/@href