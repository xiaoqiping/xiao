#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-


#咸鱼客户提供的代码，相对之前的全一点上一版的只有all数据，没有pc wise 区分的数据
from urllib.parse import urlencode
import queue
import math
import datetime
import random
import time
import json
import requests
import pandas as pd
import csv

COOKIES = input("请输入COOKIES,没有按默认值,输完之后请按回车键确认:")
stat_time =   input("请输入需要开始日期，例如 '2020-03-15' ,输完之后请按回车键确认:")
end_time =   input("请输入需要结束日期，例如 '2020-04-04' ,输完之后请按回车键确认:")

if not stat_time:
    print("请输入开始时间")
    stat_time = input("请输入开始日期，例如 '2020-03-15' ,输完之后请按回车键确认:")

if not end_time:
    print("请输入结束时间")
    end_time = input("请输入结束日期，例如 '2020-04-04' ,输完之后请按回车键确认:")

if not COOKIES:
    COOKIES = 'BAIDUID=49AC6D4C0D47962D5F7152B3982A89FC:FG=1; BIDUPSID=49AC6D4C0D47962D5F7152B3982A89FC; PSTM=1585538243; BDUSS=GdFSkxVcGRpSzJrfnRnSWUzTlJ-LTkwVm9jQ2c2SlJ5VmNHN0N2djdtazF-S2hlRVFBQUFBJCQAAAAAAAAAAAEAAACpBMgANDYwOTU5MjYwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADVvgV41b4FeU; MCITY=-309%3A; BDRCVFR[br4t9dKzX5c]=aeXf-1x8UdYcs; H_PS_PSSID=; delPer=0; PSINO=2; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1585891864,1585892661,1585892666,1586136159; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1586136159'

PROVINCE_CODE = {'山东': '901', '贵州': '902', '江西': '903', '重庆': '904', '内蒙古': '905', '湖北': '906', '辽宁': '907', '湖南': '908', '福建': '909', '上海': '910', '北京': '911', '广西': '912', '广东': '913', '四川': '914', '云南': '915', '江苏': '916', '浙江': '917', '青海': '918', '宁夏': '919', '河北': '920', '黑龙江': '921', '吉林': '922', '天津': '923', '陕西': '924', '甘肃': '925', '新疆': '926', '河南': '927', '安徽': '928', '山西': '929', '海南': '930', '台湾': '931', '西藏': '932', '香港': '933', '澳门': '934'}

CITY_CODE = {'广州': '95', '深圳': '94', '东莞': '133', '云浮': '195', '佛山': '196', '湛江': '197', '江门': '198', '惠州': '199', '珠海': '200', '韶关': '201', '阳江': '202', '茂名': '203', '潮州': '204', '揭阳': '205', '中山': '207', '清远': '208', '肇庆': '209', '河源': '210', '梅州': '211', '汕头': '212', '汕尾': '213', '郑州': '168', '南阳': '262', '新乡': '263', '开封': '264', '焦作': '265', '平顶山': '266', '许昌': '268', '安阳': '370', '驻马店': '371', '信阳': '373', '鹤壁': '374', '周口': '375', '商丘': '376', '洛阳': '378', '漯河': '379', '濮阳': '380', '三门峡': '381', '济源': '667', '成都': '97', '宜宾': '96', '绵阳': '98', '广元': '99', '遂宁': '100', '巴中': '101', '内江': '102', '泸州': '103', '南充': '104', '德阳': '106', '乐山': '107', '广安': '108', '资阳': '109', '自贡': '111', '攀枝花': '112', '达州': '113', '雅安': '114', '眉山': '291', '甘孜': '417', '阿坝': '457', '凉山': '479', '南京': '125', '苏州': '126', '无锡': '127', '连云港': '156', '淮安': '157', '扬州': '158', '泰州': '159', '盐城': '160', '徐州': '161', '常州': '162', '南通': '163', '镇江': '169', '宿迁': '172', '武汉': '28', '黄石': '30', '荆州': '31', '襄阳': '32', '黄冈': '33', '荆门': '34', '宜昌': '35', '十堰': '36', '随州': '37', '恩施': '38', '鄂州': '39', '咸宁': '40', '孝感': '41', '仙桃': '42', '天门': '73', '潜江': '74', '神农架': '687', '杭州': '138', '丽水': '134', '金华': '135', '温州': '149', '台州': '287', '衢州': '288', '宁波': '289', '绍兴': '303', '嘉兴': '304', '湖州': '305', '舟山': '306', '福州': '50', '莆田': '51', '三明': '52', '龙岩': '53', '厦门': '54', '泉州': '55', '漳州': '56', '宁德': '87', '南平': '253', '哈尔滨': '152', '大庆': '153', '伊春': '295', '大兴安岭': '297', '黑河': '300', '鹤岗': '301', '七台河': '302', '齐齐哈尔': '319', '佳木斯': '320', '牡丹江': '322', '鸡西': '323', '绥化': '324', '双鸭山': '359', '济南': '1', '滨州': '76', '青岛': '77', '烟台': '78', '临沂': '79', '潍坊': '80', '淄博': '81', '东营': '82', '聊城': '83', '菏泽': '84', '枣庄': '85', '德州': '86', '威海': '88', '济宁': '352', '泰安': '353', '莱芜': '356', '日照': '366', '西安': '165', '铜川': '271', '安康': '272', '宝鸡': '273', '商洛': '274', '渭南': '275', '汉中': '276', '咸阳': '277', '榆林': '278', '延安': '401', '石家庄': '141', '衡水': '143', '张家口': '144', '承德': '145', '秦皇岛': '146', '廊坊': '147', '沧州': '148', '保定': '259', '唐山': '261', '邯郸': '292', '邢台': '293', '沈阳': '150', '大连': '29', '盘锦': '151', '鞍山': '215', '朝阳': '216', '锦州': '217', '铁岭': '218', '丹东': '219', '本溪': '220', '营口': '221', '抚顺': '222', '阜新': '223', '辽阳': '224', '葫芦岛': '225', '长春': '154', '四平': '155', '辽源': '191', '松原': '194', '吉林': '270', '通化': '407', '白山': '408', '白城': '410', '延边': '525', '昆明': '117', '玉溪': '123', '楚雄': '124', '大理': '334', '昭通': '335', '红河': '337', '曲靖': '339', '丽江': '342', '临沧': '350', '文山': '437', '保山': '438', '普洱': '666', '西双版纳': '668', '德宏': '669', '怒江': '671', '迪庆': '672', '乌鲁木齐': '467', '石河子': '280', '吐鲁番': '310', '昌吉': '311', '哈密': '312', '阿克苏': '315', '克拉玛依': '317', '博尔塔拉': '318', '阿勒泰': '383', '喀什': '384', '和田': '386', '巴音郭楞': '499', '伊犁': '520', '塔城': '563', '克孜勒苏柯尔克孜': '653', '五家渠': '661', '阿拉尔': '692', '图木舒克': '693', '南宁': '90', '柳州': '89', '桂林': '91', '贺州': '92', '贵港': '93', '玉林': '118', '河池': '119', '北海': '128', '钦州': '129', '防城港': '130', '百色': '131', '梧州': '132', '来宾': '506', '崇左': '665', '太原': '231', '大同': '227', '长治': '228', '忻州': '229', '晋中': '230', '临汾': '232', '运城': '233', '晋城': '234', '朔州': '235', '阳泉': '236', '吕梁': '237', '长沙': '43', '岳阳': '44', '衡阳': '45', '株洲': '46', '湘潭': '47', '益阳': '48', '郴州': '49', '湘西': '65', '娄底': '66', '怀化': '67', '常德': '68', '张家界': '226', '永州': '269', '邵阳': '405', '南昌': '5', '九江': '6', '鹰潭': '7', '抚州': '8', '上饶': '9', '赣州': '10', '吉安': '115', '萍乡': '136', '景德镇': '137', '新余': '246', '宜春': '256', '合肥': '189', '铜陵': '173', '黄山': '174', '池州': '175', '宣城': '176', '巢湖': '177', '淮南': '178', '宿州': '179', '六安': '181', '滁州': '182', '淮北': '183', '阜阳': '184', '马鞍山': '185', '安庆': '186', '蚌埠': '187', '芜湖': '188', '亳州': '391', '呼和浩特': '20', '包头': '13', '鄂尔多斯': '14', '巴彦淖尔': '15', '乌海': '16', '阿拉善盟': '17', '锡林郭勒盟': '19', '赤峰': '21', '通辽': '22', '呼伦贝尔': '25', '乌兰察布': '331', '兴安盟': '333', '兰州': '166', '庆阳': '281', '定西': '282', '武威': '283', '酒泉': '284', '张掖': '285', '嘉峪关': '286', '平凉': '307', '天水': '308', '白银': '309', '金昌': '343', '陇南': '344', '临夏': '346', '甘南': '673', '海口': '239', '万宁': '241', '琼海': '242', '三亚': '243', '儋州': '244', '东方': '456', '五指山': '582', '文昌': '670', '陵水': '674', '澄迈': '675', '乐东': '679', '临高': '680', '定安': '681', '昌江': '683', '屯昌': '684', '保亭': '686', '白沙': '689', '琼中': '690', '贵阳': '2', '黔南': '3', '六盘水': '4', '遵义': '59', '黔东南': '61', '铜仁': '422', '安顺': '424', '毕节': '426', '黔西南': '588', '银川': '140', '吴忠': '395', '固原': '396', '石嘴山': '472', '中卫': '480', '西宁': '139', '海西': '608', '海东': '652', '玉树': '659', '海南': '676', '海北': '682', '黄南': '685', '果洛': '688', '拉萨': '466', '日喀则': '516', '那曲': '655', '林芝': '656', '山南': '677', '昌都': '678', '阿里': '691'}
headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}

class BaiduIndex:
    """
        百度搜索指数
        :keywords; list
        :start_date; string '2018-10-02'
        :end_date; string '2018-10-02'
        :area; int, search by cls.province_code/cls.city_code
    """

    province_code = PROVINCE_CODE
    city_code = CITY_CODE
    _all_kind = ['all']
    _params_queue = queue.Queue()

    def __init__(self, keywords: list, start_date: str, end_date: str, area=0):
        self.keywords = keywords
        self._area = area
        self._init_queue(start_date, end_date, keywords)

    def get_index(self):
        """
        获取百度指数
        返回的数据格式为:
        {
            'keyword': '武林外传',
            'type': 'wise',
            'date': '2019-04-30',
            'index': '202'
        }
        """
        while 1:
            try:
                params_data = self._params_queue.get(timeout=1)
                encrypt_datas, uniqid = self._get_encrypt_datas(
                    start_date=params_data['start_date'],
                    end_date=params_data['end_date'],
                    keywords=params_data['keywords']
                )
                key = self._get_key(uniqid)
                for encrypt_data in encrypt_datas:
                    for kind in self._all_kind:
                        encrypt_data[kind]['data'] = self._decrypt_func(
                                key, encrypt_data[kind]['data'])
                    for formated_data in self._format_data(encrypt_data):
                        yield formated_data
            except requests.Timeout:
                self._params_queue.put(params_data)
            except queue.Empty:
                break
            self._sleep_func()

    def _init_queue(self, start_date, end_date, keywords):
        """
            初始化参数队列
        """
        keywords_list = self._split_keywords(keywords)
        time_range_list = self._get_time_range_list(start_date, end_date)
        for start_date, end_date in time_range_list:
            for keywords in keywords_list:
                params = {
                    'keywords': keywords,
                    'start_date': start_date,
                    'end_date': end_date
                }
                self._params_queue.put(params)

    def _split_keywords(self, keywords: list) -> [list]:
        """
        一个请求最多传入5个关键词, 所以需要对关键词进行切分
        """
        return [keywords[i*5: (i+1)*5] for i in range(math.ceil(len(keywords)/5))]

    def _get_encrypt_datas(self, start_date, end_date, keywords):
        """
        :start_date; str, 2018-10-01
        :end_date; str, 2018-10-01
        :keyword; list, ['1', '2', '3']
        """
        request_args = {
            'word': ','.join(keywords),
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'area': self._area,
        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
        html = self._http_get(url)
        datas = json.loads(html)
        uniqid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return (encrypt_datas, uniqid)

    def _get_key(self, uniqid):
        """
        """
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
        html = self._http_get(url)
        datas = json.loads(html)
        key = datas['data']
        return key

    def _format_data(self, data):
        """
            格式化堆在一起的数据
        """
        keyword = str(data['word'])
        time_length = len(data['all']['data'])
        start_date = data['all']['startDate']
        cur_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        for i in range(time_length):
            for kind in self._all_kind:
                index_datas = data[kind]['data']
                index_data = index_datas[i] if len(index_datas) != 1 else index_datas[0]
                formated_data = {
                    'keyword': keyword,
                    'type': kind,
                    'date': cur_date.strftime('%Y-%m-%d'),
                    'index': index_data if index_data else '0'
                }
                yield formated_data
            cur_date += datetime.timedelta(days=1)

    def _http_get(self, url, cookies=COOKIES):
        """
            发送get请求, 程序中所有的get都是调这个方法
            如果想使用多cookies抓取, 和请求重试功能
            在这自己添加
        """
        headers['Cookie'] = cookies
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            raise requests.Timeout
        return response.text

    def _get_time_range_list(self, startdate, enddate):
        """
            切分时间段
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            tempdate = startdate + datetime.timedelta(days=300)
            if tempdate > enddate:
                date_range_list.append((startdate, enddate))
                break
            date_range_list.append((startdate, tempdate))
            startdate = tempdate + datetime.timedelta(days=1)
        return date_range_list

    def _decrypt_func(self, key, data):
        """
            数据解密方法
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a)//2):
            n[a[o]] = a[len(a)//2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

    def _sleep_func(self):
        """
            sleep方法, 单账号抓取过快, 一段时间内请求会失败
        """
        sleep_time = random.choice(range(50, 90)) * 0.1
        time.sleep(sleep_time)

    def duqu_list(file):
        with open(file, encoding="utf-8-sig") as f:
            f.readlines()
            f.seek(0)  # 把指针移到文件开头位置
            result = []
            for line in f.readlines():  # readlines以列表输出文件内容
                line = line.replace(",", "").replace("\n", "")  # 改变元素，去掉，和换行符\n,tab键则把逗号换成"/t",空格换成" "
                result.append(line)
        return result

    def list_spilt(one_data_list):
        '''
        将一维的列表转化为矩阵形式
        '''
        res_list = []
        for i in range(0, len(one_data_list)):
            res_list.append(one_data_list[i])
        return res_list


def token_check():
    code_name = 'baidu_index_config'
    code = 'B7BC52B2D53115267CD1AC9662ADE22EYUQDHGTLB'
    try:
        url = 'http://39.100.113.43:9000/key.php'
        response = requests.get(url, timeout=(6.05, 27.05), params={"code_name": code_name, 'code': code})
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        if response.text != '200':
            print("操作失败")
            exit()
    except requests.RequestException as e:
        print("操作失败")
        exit()
if __name__ == "__main__":
    token_check()

    # 建立csv文件，保存数据
    csvFile = open(r'file/百度指数/senlin_down.csv', 'a+', newline='', encoding='utf_8_sig')
    # csvFile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvFile)
    writer.writerow(('name', 'type','value', 'date'))

    one_data_list = BaiduIndex.duqu_list('file/百度指数/data.txt')
    keywordlist = BaiduIndex.list_spilt(one_data_list)
    for i in range(0,len(keywordlist)):
        keywords = [keywordlist[i]]
        baidu_index = BaiduIndex(keywords, stat_time, end_time)
        result_data=[]
        for index in baidu_index.get_index():
            result_data.append(index)
            print(index)

            #两种方式存csv

            # df = pd.DataFrame(result_data)
            # df.to_csv("%s.csv"%keywords[0],encoding='utf-8-sig')

            writer.writerow((index['keyword'], index['keyword'],index['index'], index['date']))
