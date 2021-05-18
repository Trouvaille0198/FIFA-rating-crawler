# FIFA-rating-crawler
FIFA 球员数据爬取及分析

github项目地址：https://github.com/Trouvaille0198/FIFA-rating-crawler

## 一、简述
《FIFA》是美国艺电公司（EA）推出的足球动作系列游戏。每年，来自游戏公司的数据调查人员（球探）都会对现实世界的真实球员进行考察与评估，为其各项能力进行打分评级，构筑了一个庞大精准的写实游戏数据库。

此项目完成了以下工作

- 编写了**网络爬虫**程序，从数据查询网站 https://sofifa.com/ 上爬取了一万八千余条 FIFA 球员详细信息；
- 对爬取的球员数据进行了**可视化分析**；
- 通过简单的**机器学习**算法
  - 构建线性回归模型，对 FIFA 球员**综合能力值**的计算方法进行了猜测
  - 构建聚类模型和分类模型，分析了球员司职与球员各项能力之间的关系

## 二、环境
### 2.1 编译环境
- 操作系统：windows 10
- 集成开发环境：IDLE
- 编辑器：Visual Studio Code
- Python 版本：3.9.1
### 2.2 外部库
| 模块名     | 功能                                   |
| ---------- | -------------------------------------- |
| requests   | 发送 HTTP 请求                         |
| lxml       | 解析 HTML 元素                         |
| numpy      | 提供科学计算方法                       |
| pandas     | 提供数据结构化、数据清理、数据分析工具 |
| seaborn    | 绘制可视化图表                         |
| matplotlib | 为 seaborn 提供底层支持                |
| sklearn    | 提供机器学习封装算法                   |

## 三、概览
### 3.1 项目结构

```shell
FIFA-rating-crawler
│   .gitignore 
│   README.md 
│
├───data_anlysis                        // 数据分析
│       player_anal.ipynb               // 球员各项能力值可视化
│       position_classification.ipynb   // Knn，球员司职分类
│       position_clustering.ipynb       // K-means，球员司职聚类
│       rating_predict.ipynb            // 线性回归，球员综合能力值预测
│
├───players_info  						// 数据存放
│       players_info.csv				// 球员完整数据
│       players_info_classified.csv		// 球员筛选数据
│       pred_fig.png					// 聚类后的两两特征图
│       real_fig.png					// 部分字段的两两特征图
│ 
├───sofifa_crawler 						// sofifa网站数据爬取
│       Crawler.py						// 爬虫类
│       main.py							// 爬虫启动程序
│
└───futhead_crawler                     // futhead网站数据爬取
		Crawler.py						// 爬虫类
		MultipleCrawler.py              // 多个球员爬取模块
		SingleCrawler.py				// 单个球员爬取模块
		ToCSV.py						// 数据保存模块

```




### 3.2 模块功能
#### 3.2.1 爬虫模块
sofifa 网站的球员信息封装在球员详细页中

url 样例：https://sofifa.com/player/158023/lionel-messi/210040/

![image-20210518085935156](http://image.trouvaille0198.top/image-20210518085935156.png)

![image-20210518085923747](http://image.trouvaille0198.top/image-20210518085923747.png)

球员详细页的入口则在网站上分页展现

url 样例：https://sofifa.com/?col=oa&sort=desc

![image-20210518085835975](http://image.trouvaille0198.top/image-20210518085835975.png)因此，爬虫的主要思路是：分页爬取所有的球员详细页，再从详细页中爬取到每个球员的具体数据

根据 sofifa 网站网页的 DOM 结构，项目设计了爬虫类 Crawler。下面简要介绍一些具有重要功能的类方法。

##### 1）get_url_text
伪装请求头后，对网站发出 GET 请求，得到完整的 HTML 页面。并做了简单的异常处理
##### 2）get_whole_player_url
获取指定页面组的球员详细页表，并以列表形式存储

##### 3）parse_player_info

解析并存储单个球员的具体信息，具体爬取字段在数据成员中展现：

```python
self.column = [
            'Name', 'Nation', 'Club', 'Position', 'Age', 'Birth', 'Height',
            'Weight', 'Jersey number', 'Strong feet', 'Value', 'Wage',
            'Release clause', 'Rating', 'Potential', 'PACE', 'SHOOTING',
            'PASSING', 'DRIBBLING', 'DEFENCE', 'PHYSICAL', 'crossing', 'finishing', 'heading accuracy',
            'short passing', 'volleys', 'dribbling skill', 'curve', 'fk accuracy', 'long passing',
            'ball control', 'acceleration', 'sprint speed', 'agility', 'reactions', 'balance', 'shot power',
            'jumping', 'stamina', 'strength', 'long shots', 'aggression', 'interceptions', 'positioning', 				'vision','penalties', 'composure', 'defensive_awareness', 'standing_tackle', 'sliding_tackle']
```

##### 4）start

爬虫入口，集成一次爬虫的完整过程

最后爬取的数据以 csv 格式存储，去除重复项后，共计 16741 条球员完整数据

#### 3.2.2 数据分析模块

##### 1）数据清洗与分析

`player_anal` 中，对爬取的球员数据完成了简单的清洗，绘制部分字段的分布图，将过于细分的球员司职进行合并。

##### 2）构建综合能力值预测模型

游戏中球员的能力数据都是经过考察调研得出，往往可以反映其真实水平。为了探索球员总评的计算公式，项目采用线性回归算法对各项能力值进行简单的机器学习，利用字典特征提取和标准化对数据进行特征工程。预测结果的均分误差在 6.5 以下，与真实总评基本吻合。

##### 3）构建球员 Knn 分类模型

球员司职不同，能力模型自然不同，为了探索不同位置的能力差异，项目采用 Knn 算法对 ”中锋、边锋、中场、中后卫、边后卫“ 五个位置进行分类预测。训练时使用了网络搜索自动调参，尽可能找到全局最优值。

预测结果的准确率超过 82%，如果仅仅分 ”中锋、中场、中后卫“ 三类，预测结果可达 97%。

##### 4）构建球员 K-means 聚类模型

如果不给出球员位置信息，使用基于 K-means 聚类的无监督学习，更能体现能力数据之间的关联程度。

项目设置训练簇数为 3，来匹配实际中 ”中锋、中场、中后卫“ 这三大位置，训练效果良好，轮廓系数为 0.356，准确率可达 86.8%。

![pred_fig](http://image.trouvaille0198.top/pred_fig.png)

## 四、核心实现

本节介绍了项目中一些重要、具有特色的核心模块。

### 4.1 解析 DOM 节点树

通过 chrome 的 F12 开发者工具，确定爬取数据的节点位置，转换成 xpath 语法后即可提取。

机械地编写 xpath 会让语法泛用性降低，某类元素节点的绝对位置在上万个 HTML 文本中必然会出现差异。项目采用类自顶向下的方式、根据节点间的相对位置来构建 xpath 语法。

例如，欲爬取视野 `Vision` 字段：

<img src="http://image.trouvaille0198.top/image-20210518111837690.png" alt="image-20210518111837690" style="zoom:50%;" />

首先找到包装精神 `MENTALITY` 属性的 `div` 标签：

<img src="http://image.trouvaille0198.top/image-20210518111738620.png" alt="image-20210518111738620" style="zoom:50%;" />

找到内部的列表标签 `ul`：

<img src="http://image.trouvaille0198.top/image-20210518111558100.png" alt="image-20210518111558100" style="zoom:50%;" />

最后找到目标，是一个列表项标签 `li`

<img src="http://image.trouvaille0198.top/image-20210518111634333.png" alt="image-20210518111634333" style="zoom:50%;" />

找到目标后，构建 xpath 语法

```python
vision = self.get_feature(player, "//div[@class='column col-3']//div[@class='card']//h5[text()='Mentality']/../ul/li[4]/span/text()", True)
```

代码中 `get_feature` 函数是对解析函数 `xpath()` 的再封装，增加了空数据处理功能

```python
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
```

其中第二个参数即为构建好的 xpath 语法字符串

以此类推，可以爬取到全部字段

### 4.2 机器学习部分

项目所有机器学习、特征工程算法均使用 `sklearn` 库中的封装模型。

以 knn 分类为例

首先筛选出五个位置的球员信息，从中分离出特征字段组 x 与标签组 y 

```python
data_test = data.query("位置=='中锋' or 位置=='边锋' or 位置=='中场' or 位置=='中后卫' or 位置=='边后卫'")
x = data_test.drop(['位置','Position'],axis=1)
y = data_test['位置'].to_list()
```

将数据集划分成测试集与验证集

```python
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=82)
```

随后，为了避免字段间数据数量级差异带来的负面影响，使用标准化对数据进行特征工程

```python
transfer_std = StandardScaler()
x_train_std = transfer_std.fit_transform(x_train)
x_test_std = transfer_std.transform(x_test)
```

正式开始训练。声明一个 knn 算法模型，选用网格搜索与十折交叉验证提高精度。

```python
# KNN
estimator_knn = KNeighborsClassifier()
# 调优
param_dict = {"n_neighbors": [i for i in range(1,20)]}
estimator_knn = GridSearchCV(
    estimator_knn, param_grid=param_dict, cv=10)  # 10折
```

训练模型，得到预测值 `y_pred`

```python
estimator_knn.fit(x_train_std, y_train)
y_pred = estimator_knn.predict(x_test_std)
```

查看准确率

```python
print("准确率为：\n", estimator_knn.score(x_test_std, y_test))

# 准确率为：
# 0.8257488479262672
```





