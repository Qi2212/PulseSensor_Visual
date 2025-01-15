## 项目说明

​	在当今物联网技术飞速发展的时代背景下，智慧医疗作为物联网应用的重要领域之一，正以前所未有的速度改变着传统医疗行业的面貌。我们团队致力于开发一款基于物联网的智慧心率检测系统，旨在通过先进的物联网技术，实现对人体心率的实时监测与数据传输，以及结合可视化手段以及当下流行的大语言模型Agent框架为智慧心率这一方向实现我们的设计想法。该系统融合了智能传感器技术、射频识别技术、数据库系统原理以及Python语言程序设计、大语言模型Agent思维链等多学科知识，希望我们的选题在相关领域能有创新性的引导。


## 系统功能

（1）检测传感器及语音模块设备是否进行正常的连接

（2）传感器连接下位机通过串口正确传输数据到上位机

（3）语音模块与测试步骤配合实现实时正确播报

（4）上位机对接收的数据进行可视化报告

（5）ChatGLM大语言模型结合Agent自动读取数据库数据给出建议

（6）采集数据的数据库存储以及CSV日志文件的生成与下载

（7）历史数据的可视化回顾

（8）用户反馈系统问题



## 系统环境搭建

Python环境的搭建方面:本系统软件部分语言全部使用Python语言进行搭建，为了运行本系统需要的Python环境3.12.1及以上。

使用Python的时候，强烈建议创建虚拟环境来搭建开发环境，可以使用source或者conda进行创建虚拟环境，用conda创建虚拟环境是使用`conda create env -n sensor`创建一个名为sensor的虚拟环境，使用`conda activate senso`r进行激活，`pip install/conda install`相关的python库，首次下载是conda会自动安装最新的python版本，可以使用conda list进行查看python版本。创建完虚拟环境以后，需要下载运行项目所需的全部Python库，我已将需要的库打成`requirements.txt`放在源代码目录下，可以使用`pip install -r requirements.txt`进行安装。部分库及版本如下：

```t
accessible-pygments==0.0.5

alabaster==0.7.16

altair==5.5.0

annotated-types==0.7.0

anyio==4.7.0

argon2-cffi==23.1.0

argon2-cffi-bindings==21.2.0

arrow==1.3.0

asttokens==3.0.0

attrs==24.3.0

babel==2.16.0

beautifulsoup4==4.12.3

streamlit==1.41.1

zhipuai==2.1.5.20241204

zipp==3.21.0

zundler==0.2.2
```

详见代码目录下`requirements.txt`

后续代码更新放在GitHub仓库:https://github.com/Qi2212/PulseSensor_Visual.git



## 基础配置

* 更改数据库配置

  在`.\sensor\fronted_page\db_config\db_info.py`的文件中修改`config`

  ```python
  config = {
          'host': 'localhost', #如果用服务器连接就改成服务器ip地址
          'user': 'root',
          'port':3306, #默认是3306，如果修改了端口也需要改
          'password': 'your database password', #password修改为自己的本地数据库密码
          'db': 'sensor', #现在数据库里面创建sensor的db
          'charset': 'utf8mb4',
          'cursorclass': pymysql.cursors.DictCursor
      }
  ```

  

* 配置自己的ChatGLM4的API_KEY

  在`.\sensor\fronted_page\expert.py`的Line 85中修改

  ```python
  api_key = "your api key" #具体创建方法在智谱AI中
  ```

* 修改代码中的目录

  > 代码文件中的很多路径都是我的本地路径，需要全部修改，建议修改为相对路径 好移植

* 创建虚拟环境

  建议python 3.12.1机以上的Python版本

  使用`conda`

  `conda create env -n sensor`

* 激活虚拟环境

  `conda activate sensor`

* 安装运行所需Python库

  `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`



## 启动项目

* 进入fronted_page目录下

  `cd fronted_page`

* 启动项目

  `streamlit run fronted.py`
