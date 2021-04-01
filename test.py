# -*- coding:utf-8 -*-
#! python2
import re
string = '1244(356)43637'
p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
print(re.match(r'[(](.*?)[)]', string).group(0))
print(re.search(p2, string).group(0))
