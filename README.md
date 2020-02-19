
# 2019新型冠状病毒疫情数据可视化、疫情历史数据分析、数据更新、数据清洗行政区域代码标准化，疫情小区地图数据呈现

针对此次武汉新型冠状病毒(COVID-19，原2019-nCov)数据变化情况，做可视分析(Coronavirus Visualization Analysis)，旨在表现可视化的魅力！

[新冠肺炎疫情 · 数据分析系统](http://106.54.48.46:8002)  
	WuHan COVID-19 Data Visualization Analysis System		http://106.54.48.46:8002

全栈项目：前后分离，具体代码路径见结尾的[项目结构]

## 可视化效果

[http://ncov.myvis.cn:8002](http://ncov.myvis.cn:8002)


## 项目特点

1. 支持常规省、市、县三级地图数据可视化，下钻交互。

2. 动态效果播放呈现各级区域疫情数据随时间变化趋势。(★★★★★)

3. 全国省市混合热力图数据呈现，及时间序列变化趋势。(★★★★)

4. 交互式数据分析，同时支持各级地区、时间维度组合分析。

5. 疫情周边确诊患者小区地理位置3D可视化。

6. 兼容移动端设备


## 当前进度

1. 完成数据获取、数据清洗

2. 完成省级、市级地图、条形图数据展示和下钻交互。

3. 完成时间轴动画播放

4. 完成曲线图

5. 完成疫情小区数据解析入库，及数据清洗

6. 完成ThreeJs场景流动线条，完成3种风格地图可视化


## 初步效果

疫情小区地图

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/map1.png)

时间序列曲线

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/line2.png)

时间序列播放

![Demo Image](https://github.com/simonblowsnow/2019-ncov-vis/blob/master/web/epidemic-map/image/time.png)



## 项目结构

1.前端源码：web目录下（VUE、ElementUI、ECharts、Maptalks、D3js）

	开发部署：
		
		cd web/epidemic-map
		
		npm install
		
		npm run serve
		
		效果：http://localhost:8080/
		
	具体参考 web/epidemic-map/README.md
	
	

2.后端源码：src目录下（PYTHON3、Flask、Mysql）

	配置文件：src/config.py	
	
	启动服务：
		start.bat - On Windows
		
		./start.sh - On Linux
		

3.数据库：（Mysql）
	
	文件：src/db/epidemic.sql
	
	新建数据库epidemic，将该文件导入MySQL即可。（命令行方式：use epidemic; source /root/epidemic.sql;）
	
	数据库账号密码在src/config.py中配置
	

4.数据：
	
	使用API：https://lab.isaaclin.cn/nCoV
	
	数据更新：src/data/dxy_record.py （手动）
	
	数据清洗：地区标准化 - region_recognition.py
	
	自动更新任务：startData.bat 或 ./startData.sh
	
