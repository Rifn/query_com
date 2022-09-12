#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/7 17:51
# @Author  : Barrett
# @Email   : 1198878568@qq.com
# @FileName: tool.py
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from requests.auth import HTTPBasicAuth


# 获取特定公司的指定信息
def get_company_message(company, headers):
    # 获取查询到的网页内容（全部）
    sess = requests.session()
    search = sess.get('https://www.qcc.com/web/search?key={}'.format(company), headers=headers, timeout=10)
    search.raise_for_status()
    search.encoding = 'utf-8'  # linux utf-8
    soup = BeautifulSoup(search.text, features="html.parser")
    href = soup.find_all('a', {'class': 'title'})[0].get('href')
    time.sleep(4)
    # 获取查询到的网页内容（全部）
    details = sess.get(href, headers=headers, timeout=10)
    details.raise_for_status()
    details.encoding = 'utf-8'  # linux utf-8
    details_soup = BeautifulSoup(details.text, features="html.parser")
    message = details_soup.find_all({'table': 'ntable'})[0].text
    time.sleep(2)
    return message, search.text


# 将获取的信息转化为dataframe
def message_to_df(message):
    # 统一社会信用代码
    unified_social_credit_code = []
    try:
        unified_social_credit_code.append(
            message.split('统一社会信用代码')[1].split('复制')[0].replace(" ", "").replace("\n", ""))
    except:
        unified_social_credit_code.append('无法收集')

    # 企业名称
    list_companys = []
    try:
        list_companys.append(message.split('企业名称')[1].split('复制')[0].replace(" ", "").replace("\n", ""))
    except:
        list_companys.append('无法收集')

    # 法定代表人
    Legal_Person = []
    try:
        s = message.split('法定代表人')[1].split('关联')[0].replace("\n", "").replace(" ", "")[1:]
        Legal_Person.append(s)
    except:
        Legal_Person.append('无法收集')

    # 登记状态
    Registration_status = []
    try:
        Registration_status.append(message.split('登记状态')[1].split('成立日期')[0].replace(" ", "").replace("\n", ""))
    except:
        Registration_status.append('无法收集')

    # 成立日期
    Date_of_Establishment = []
    try:
        Date_of_Establishment.append(message.split('成立日期')[1].split('复制')[0].replace(" ", "").replace("\n", ""))
    except:
        Date_of_Establishment.append('无法收集')

    # 注册资本
    registered_capital = []
    try:
        registered_capital.append(message.split('注册资本')[1].split('实缴资本')[0].replace(' ', '').replace("\n", ""))
    except:
        registered_capital.append('无法收集')

    # 实缴资本
    contributed_capital = []
    try:
        contributed_capital.append(message.split('实缴资本')[1].split('核准日期')[0].replace(' ', '').replace('\n', ''))
    except:
        contributed_capital.append('无法收集')

    # 核准日期
    Approved_date = []
    try:
        Approved_date.append(message.split('核准日期')[1].split('组织机构代码')[0].replace(' ', '').replace("\n", ""))
    except:
        Approved_date.append('无法收集')

    # 组织机构代码
    Organization_Code = []
    try:
        Organization_Code.append(message.split('组织机构代码')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        Organization_Code.append('无法收集')

    # 工商注册号
    companyNo = []
    try:
        companyNo.append(message.split('工商注册号')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        companyNo.append('无法收集')

    # 纳税人识别号
    Taxpayer_Identification_Number = []
    try:
        Taxpayer_Identification_Number.append(
            message.split('纳税人识别号')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_Identification_Number.append('无法收集')

    # 企业类型
    enterprise_type = []
    try:
        enterprise_type.append(message.split('企业类型')[1].split('营业期限')[0].replace('\n', '').replace(' ', ''))
    except:
        enterprise_type.append('无法收集')

    # 营业期限
    Business_Term = []
    try:
        Business_Term.append(message.split('营业期限')[1].split('纳税人资质')[0].replace('\n', '').replace(' ', ''))
    except:
        Business_Term.append('无法收集')

    # 纳税人资质
    Taxpayer_aptitude = []
    try:
        Taxpayer_aptitude.append(message.split('纳税人资质')[1].split('所属行业')[0].replace(' ', '').replace("\n", ""))
    except:
        Taxpayer_aptitude.append('无法收集')

    # 所属行业
    sub_Industry = []
    try:
        sub_Industry.append(message.split('所属行业')[1].split('所属地区')[0].replace('\n', '').replace(' ', ''))
    except:
        sub_Industry.append('无法收集')

    # 所属地区
    sub_area = []
    try:
        sub_area.append(message.split('所属地区')[1].split('登记机关')[0].replace(' ', '').replace("\n", ""))
    except:
        sub_area.append('无法收集')

    # 登记机关
    Registration_Authority = []
    try:
        Registration_Authority.append(message.split('登记机关')[1].split('人员规模')[0].replace(' ', '').replace("\n", ""))
    except:
        Registration_Authority.append('无法收集')

    # 人员规模
    staff_size = []
    try:
        staff_size.append(message.split('人员规模')[1].split('参保人数')[0].replace(' ', '').replace('\n', ''))
    except:
        staff_size.append('无法收集')

    # 参保人数
    Number_of_participants = []
    try:
        Number_of_participants.append(message.split('参保人数')[1].split('趋势图')[0].replace(' ', '').replace("\n", ""))
    except:
        Number_of_participants.append('无法收集')

    # 曾用名
    Used_Name = []
    try:
        Used_Name.append(message.split('曾用名')[1].split('英文名')[0].replace(' ', '').replace("\n", ""))
    except:
        Used_Name.append('无法收集')

    # 英文名
    English_name = []
    try:
        English_name.append(message.split('英文名')[1].split('复制')[0].replace('\n', '').replace(' ', ''))
    except:
        English_name.append('无法收集')

    # 进出口企业代码
    import_and_export_code = []
    try:
        import_and_export_code.append(message.split('进出口企业代码')[1].split('注册地址')[0].replace(' ', '').replace("\n", ""))
    except:
        import_and_export_code.append('无法收集')

    # 注册地址
    register_adress = []
    try:
        register_adress.append(message.split('注册地址')[1].split('附近')[0].replace(' ', '').replace("\n", ""))
    except:
        register_adress.append('无法收集')

    # 经营范围
    Business_Scope = []
    try:
        Business_Scope.append(message.split('经营范围')[1].split('复制')[0].replace(' ', '').replace("\n", ""))
    except:
        Business_Scope.append('无法收集')

    df = pd.DataFrame({'统一社会信用代码': unified_social_credit_code,
                       '企业名称': list_companys,
                       '法定代表人': Legal_Person,
                       '登记状态': Registration_status,
                       '成立日期': Date_of_Establishment,
                       '注册资本': registered_capital,
                       '实缴资本': contributed_capital,
                       '核准日期': Approved_date,
                       '组织机构代码': Organization_Code,
                       '工商注册号': companyNo,
                       '纳税人识别号': Taxpayer_Identification_Number,
                       '企业类型': enterprise_type,
                       '营业期限': Business_Term,
                       '纳税人资质': Taxpayer_aptitude,
                       '所属行业': sub_Industry,
                       '所属地区': sub_area,
                       '登记机关': Registration_Authority,
                       '人员规模': staff_size,
                       '参保人数': Number_of_participants,
                       '曾用名': Used_Name,
                       '英文名': English_name,
                       '进出口企业代码': import_and_export_code,
                       '注册地址': register_adress,
                       '经营范围': Business_Scope})
    return df


# 修改这些参数即可运用本案例
user_agent = '此代码上方介绍了获取的方法'
cookie = '此代码上方介绍了获取的方法'
username = '企查查登录成功后的用户名'
password = '登录成功后的企查查密码'
save_path = '自己目录的绝对路径/某某.csv'

# 测试所用
companys = ['某某某公司', '某某某公司']

afterLogin_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44',
    'cookie': 'qcc_did=18acf2da-8455-4017-bb4e-743a7baf24ca; '
              'UM_distinctid=17f5f798fbd4a4-022b421481c17c-4e607a6f-13c680-17f5f798fbe7c2; '
              'QCCSESSID=23d66cbbfc584d3fadf0f050c1; _uab_collina=165716133172961255436054; '
              'CNZZDATA1254842228=1159757031-1646565420-https%3A%2F%2Fcn.bing.com%2F|1657164690; '
              'acw_tc=71c8899616571656096324070eebc7490cb5fd0c82393938129210d635 '
}

# ms = get_company_message("桂林经开投资控股有限责任公司", headers=afterLogin_headers)


def read_companies(path):
    with open(path, encoding="utf-8") as f:
        data = f.readlines()
    data = [s[0:-1] for s in data]
    return data


def df_to_textli(df):
    li = []
    cols = df.columns
    for col in cols:
        s = "【" + str(col) + "】" + ": " + str(df.iloc[0][col])
        li.append(s)
    return li

# df = pd.DataFrame()
# li = read_companies("./list.txt")
# print(li)
#
# for com in li:
#     ms = get_company_message(com, afterLogin_headers)
#     df_com = message_to_df(ms)
#     df = pd.concat([df, df_com], axis=0, ignore_index=True)
#     print(com + "  完成！")
#
# print(df)
# df.to_excel("./data.xlsx", index=False)

