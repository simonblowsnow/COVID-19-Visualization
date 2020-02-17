#coding:utf8
'''
Created on 2020年1月29日
'''

# China: http://www.nhc.gov.cn/xcs/xxgzbd/gzbd_index.shtml

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

PROVINCE = dict((p['name'], p['code']) for p in src_province) 

REGION_SHORT = {
    "博尔塔拉蒙古自治州": ["博尔塔拉"], 
    "昌吉回族自治州": ["昌吉"], 
    "巴音郭楞蒙古自治州": ["巴音郭楞"], 
    "伊犁哈萨克自治州": ["伊犁"], 
    "克孜勒苏柯尔克孜自治州": ["克孜勒苏"], 
    "恩施土家族苗族自治州": ["恩施"], 
    "黔南布依族苗族自治州": ["黔南"], 
    "黔东南苗族侗族自治州": ["黔东南"], 
    "黔西南布依族苗族自治州": ["黔西南"], 
    "湘西土家族苗族自治州": ["湘西"], 
    "海南藏族自治州": ["海南"], 
    "海西蒙古族藏族自治州": ["海西"], 
    "果洛藏族自治州": ["果洛"], 
    "玉树藏族自治州": ["玉树"], 
    "黄南藏族自治州": ["黄南"], 
    "海北藏族自治州": ["海北"], 
    "临夏回族自治州": ["临夏"], 
    "甘南藏族自治州": ["甘南"], 
    "凉山彝族自治州": ["凉山"], 
    "阿坝藏族羌族自治州": ["阿坝"], 
    "甘孜藏族自治州": ["甘孜"], 
    "延边朝鲜族自治州": ["延边"], 
    "红河哈尼族彝族自治州": ["红河"], 
    "怒江傈僳族自治州": ["怒江"], 
    "西双版纳傣族自治州": ["西双版纳"], 
    "楚雄彝族自治州": ["楚雄"], 
    "文山壮族苗族自治州": ["文山"], 
    "大理白族自治州": ["大理"], 
    "迪庆藏族自治州": ["迪庆"], 
    "德宏傣族景颇族自治州": ["德宏"],
    "石河子市": ["石河子", "第八师石河子市", "第八师石河子", "第八师", "兵团第八师石河子市"],   # TODO: 新疆其它师市合一地区可统一处理
    "五家渠市": ["第六师", "兵团第六师五家渠市"],
    "浦东新区": ["浦东", "浦东区"],
    "锡林郭勒盟": ["锡林郭勒"],
    "兴安盟": ["兴安"],
    "阿拉善盟": ["阿拉善"],
    "白沙黎族自治县": ["白沙", "白沙县"],
    "昌江黎族自治县": ["昌江", "昌江县"],
    "乐东黎族自治县": ["乐东", "乐东县"],
    "陵水黎族自治县": ["陵水", "陵水县"],
    "保亭黎族苗族自治县": ["保亭", "保亭县"],
    "琼中黎族苗族自治县": ["琼中", "琼中县", "琼中苗族黎族自治县"],
    "石柱土家族自治县": ["石柱", "石柱县城"], 
    "秀山土家族苗族自治县": ["秀山", "秀山县"], 
    "酉阳土家族苗族自治县": ["酉阳", "酉阳县"], 
    "彭水苗族土家族自治县": ["彭水", "彭水县"],
    "石柱土家族自治县": ["石柱", "石柱县"]
}


# 直属含有县的省 
PROVINCE_WITH_COUNTY = set([460000, 500000])
# 直辖市
PROVINCE_LEVEL_CITY = set([110000, 310000, 120000, 500000])

SPECIAL_NAME = set(['恩施'])

# 未使用
REGION_ZHOU = ['凉山', '阿坝', '甘孜', '黔西南', '黔东南', '黔南', '恩施', '湘西',
    '西双版纳', '楚雄', '红河', '德宏', '大理', '文山', '怒江', '迪庆', 
    '海南', '海西', '海北','果洛', '玉树', '黄南', '临夏', '甘南', 
    '延边', '伊犁', '博尔塔拉', '昌吉回族', '巴音郭楞', '克孜勒苏'
]
