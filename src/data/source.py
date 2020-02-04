#coding:utf8
'''
Created on 2020年1月29日
'''

# China
# http://www.nhc.gov.cn/xcs/xxgzbd/gzbd_index.shtml

src_province = [
{'name': '内蒙古自治区', 'code': 150000, 'url': 'http://wjw.nmg.gov.cn/xwzx/xwfb/index.shtml'}, 
{'name': '河南省', 'code': 410000, 'url': 'http://www.hnwsjsw.gov.cn/channels/854_2.shtml'}, 
{'name': '广东省', 'code': 440000, 'url': 'http://wsjkw.gd.gov.cn/xxgzbdfk/yqtb/'}, 
{'name': '黑龙江省', 'code': 230000, 'url': 'http://wsjkw.hlj.gov.cn/index.php/Home/Zwgk/all/typeid/42'}, 
{'name': '新疆维吾尔自治区', 'code': 650000, 'url': 'http://www.xjhfpc.gov.cn/tzgg_.htm'}, 
{'name': '湖北省', 'code': 420000, 'url': 'http://wjw.hubei.gov.cn/fbjd/tzgg'}, 
{'name': '辽宁省', 'code': 210000, 'url': 'http://wsjk.ln.gov.cn/wst_wsjskx/'}, 
{'name': '山东省', 'code': 370000, 'url': 'http://wsjkw.shandong.gov.cn/ztzl/rdzt/qlzhfkgz/tzgg/'}, 
{'name': '江苏省', 'code': 320000, 'url': 'http://wjw.jiangsu.gov.cn/col/col7290/index.html'}, 
{'name': '陕西省', 'code': 610000, 'url': 'http://sxwjw.shaanxi.gov.cn/col/col9/index.html'}, 
{'name': '上海市', 'code': 310000, 'url': 'http://wsjkw.sh.gov.cn/xwfb/index.html'}, 
{'name': '贵州省', 'code': 520000, 'url': 'http://www.gzhfpc.gov.cn/ztzl_500663/xxgzbdgrdfyyqfk/yqdt/'}, 
{'name': '重庆市', 'code': 500000, 'url': 'http://wsjkw.cq.gov.cn/tzgg/'}, 
{'name': '西藏自治区', 'code': 540000, 'url': 'http://wjw.xizang.gov.cn/xwzx/wsjkdt/'}, 
{'name': '安徽省', 'code': 340000, 'url': 'http://wjw.ah.gov.cn/news_list_450_1.html'}, 
{'name': '福建省', 'code': 350000, 'url': 'http://wjw.fujian.gov.cn/xxgk/gzdt/wsjsyw/'}, 
{'name': '湖南省', 'code': 430000, 'url': 'http://wjw.hunan.gov.cn/wjw/xxgk/gzdt/zyxw_1/index.html'}, 
{'name': '海南省', 'code': 460000, 'url': 'http://wst.hainan.gov.cn/swjw/rdzt/yqfk/index.html'}, 
{'name': '青海省', 'code': 630000, 'url': 'https://wsjkw.qinghai.gov.cn/zhxw/xwzx/index.html'}, 
{'name': '广西壮族自治区', 'code': 450000, 'url': 'http://wsjkw.gxzf.gov.cn/gzdt/bt/'}, 
{'name': '宁夏回族自治区', 'code': 640000, 'url': 'http://wsjkw.nx.gov.cn/yqfkdt/yqsd1.htm'}, 
{'name': '江西省', 'code': 360000, 'url': 'http://hc.jiangxi.gov.cn/xwzx/wjxw/index.shtml'}, 
{'name': '浙江省', 'code': 330000, 'url': 'http://www.zjwjw.gov.cn/col/col1202194/index.html'}, 
{'name': '河北省', 'code': 130000, 'url': 'http://wsjkw.hebei.gov.cn/index.do?templet=new_list&cid=14'}, 
{'name': '香港特别行政区', 'code': 810000, 'url': ''}, 
{'name': '澳门特别行政区', 'code': 820000, 'url': ''}, 
{'name': '台湾省', 'code': 710000, 'url': ''}, 
{'name': '甘肃省', 'code': 620000, 'url': 'http://wsjk.gansu.gov.cn/channel/10910/index.html'}, 
{'name': '四川省', 'code': 510000, 'url': 'http://wsjkw.sc.gov.cn/scwsjkw/gzbd/ztxqgl.shtml'}, 
{'name': '吉林省', 'code': 220000, 'url': 'http://wjw.jlcity.gov.cn/gsgg/'}, 
{'name': '天津市', 'code': 120000, 'url': 'http://wsjk.tj.gov.cn/col/col14/index.html'}, 
{'name': '云南省', 'code': 530000, 'url': 'http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU157976428326282067&cn=xxgzbd&pcn=ztlm&pid=7'}, 
{'name': '北京市', 'code': 110000, 'url': 'http://wjw.beijing.gov.cn/xwzx_20031/xwfb/'}, 
{'name': '山西省', 'code': 140000, 'url': 'http://wjw.shanxi.gov.cn/wjywl02/index.hrh'}
]

