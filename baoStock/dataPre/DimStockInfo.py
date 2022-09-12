import baostock as bs
import pandas as pd

#### 登陆系统 ####
lg = bs.login()
# 获取证券基本资料
def get_stock_basic_info():
    rs = bs.query_stock_basic()
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result
# 获取证券行业资料
def get_stock_industry_info():
    rs = bs.query_stock_industry()
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)
    return  result

# 获取上证50成分股
def get_sz50_info():
    rs = bs.query_sz50_stocks()
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        sz50_stocks.append(rs.get_row_data())
    result = pd.DataFrame(sz50_stocks, columns=rs.fields)
    return set(list(result["code"]))

# 获取沪深300成分股
def get_hs300_info():
    rs = bs.query_hs300_stocks()
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
    return set(list(result["code"]))

# 获取中证500成分股
def get_zz500_info():
    rs = bs.query_zz500_stocks()
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)
    return set(list(result["code"]))

def get_dim_info():
    basicInfo = get_stock_basic_info()
    industryInfo = get_stock_industry_info()
    basicInfo = pd.merge(basicInfo,industryInfo,left_on="code",right_on="code",how="left")
    sz50_set = get_sz50_info()
    zz500_set = get_zz500_info()
    hs300_set = get_hs300_info()
    basicInfo["sz50"] = basicInfo["code"].apply(lambda x: 1 if x in sz50_set  else 0)
    basicInfo["zz500"] = basicInfo["code"].apply(lambda x: 1 if x in zz500_set  else 0)
    basicInfo["hs300"] = basicInfo["code"].apply(lambda x: 1 if x in hs300_set  else 0)
    basicInfo.to_excel("d:/tmp.xlsx")
get_dim_info()
bs.logout()