from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = ''
data = pd.read_csv(path)

# 划分特征集与标签集
x = data.loc[:, ['PACE', 'SHOOTING', 'PASSING', 'DRIBBLING', 'DEFENCE',
                 'PHYSICAL']]
y = data['Rating']
# 划分数据集
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=4)
# 开始训练
estimator = LinearRegression()
estimator.fit(x_train, y_train)

print("正规方程_权重系数为: ", estimator.coef_)
print("正规方程_偏置为:", estimator.intercept_)

y_predict = estimator.predict(x_test)
error = mean_squared_error(y_test, y_predict)
print("正规方程_能力值预测:", y_predict)
print("正规方程_均分误差:", error)

y_test_list = y_test.to_list()
for i in range(len(y_predict)):
    print('预测值：', y_predict[i], '，测试值：', y_test_list[i], '，误差：', y_predict[i]-y_test_list[i])
