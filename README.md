# FIFA-rating-crawler
FIFA球员数据爬取及分析

github项目地址：

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
└───sofifa_crawler 						// 数据爬取
        Crawler.py						// 爬虫类
        main.py							// 爬虫启动程序

```




### 3.2 模块功能
游戏中球员的能力数据都是经过考察调研得出，往往可以反映其真实水平