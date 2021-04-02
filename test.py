import re
import numpy as np


def wage_manege(text):
    text = re.sub('€', '', text)  # 去除欧元单位
    try:
        if text[-1].isdigit():
            text = float(text[:-1])/1000
        elif text[-1] == 'K':
            text = float(text[:-1])
        elif text[-1] == 'M':
            text = float(text[:-1])*1000
        else:
            text = np.nan
    except:
        text = np.nan
    return text


money = '€0.3K'
print(wage_manege(money))
