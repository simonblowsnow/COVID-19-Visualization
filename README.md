
# 2019新型冠状病毒疫情数据获取、清洗、可视化、分析

针对此次武汉新型冠状病毒(2019-nCov)数据变化情况，做可视分析(Visualization Analysis)，旨在呈现并还原疫情发展情况。

## 项目特点

1. 支持常规省、市、县三级地图数据可视化，下钻交互。

2. 动态效果播放呈现各级区域疫情数据随时间变化趋势。(★★★★★)

3. 全国省市混合热力图数据呈现，及时间序列变化趋势。(★★★★)

4. 其它创新

专业可视分析技术与思维倾情打造，敬请期待！

## 当前进度

1.完成数据获取、数据清洗

2.完成省级、市级地图、条形图数据展示和下钻交互。

TODO：时间轴动画播放


## 初步效果

全国地图

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/demo.png)

省级地图

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/demo4.png)

时间序列

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/demo3.png)



## 项目结构

1.前端源码：web目录下（VUE、ElementUI、ECharts、Maptalks、D3js）

	开发部署：参考 web/epidemic-map/README.md
	
	开发效果：http://localhost:8080/

2.后端源码：src目录下（PYTHON3、Flask、Mysql）
	配置文件：src/config.py	

3.数据库文件：src/db/epidemic.sql

4.数据：

	目前使用API：https://lab.isaaclin.cn/nCoV
	
	数据请求：src/data/dxy_record.py
	
	数据清洗：地区标准化 - region_recognition.py
	
	TODO: 数据定时增量更新
