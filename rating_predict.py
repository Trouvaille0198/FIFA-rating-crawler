from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = ''
data = pd.read_csv(path)

# 划分特征集与标签集
x = data['PACE', 'SHOOTING', 'PASSING', 'DRIBBLING', 'DEFENCE',
         'PHYSICAL'].to_dict(orient='records')
y = data['Rating'].values
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