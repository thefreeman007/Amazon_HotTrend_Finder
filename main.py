import warnings
warnings.filterwarnings('ignore')
import os
from os import listdir
import pandas as pd
import logging
import pickle
import keepa

# 设置日志配置
logging.basicConfig(
    filename="process_log.txt",  # 日志文件名
    level=logging.INFO,         # 日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    datefmt="%Y-%m-%d %H:%M:%S"  # 时间格式
)

# Pandas display settings Pandas 数据显示设置
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.width', 6000)

# Global path variables for managing data input and output 全局路径变量，用于管理数据的输入输出
RAW_DICT_PATH = "./data/all_dict/"  # Path to dictionary files 字典文件路径
DATA_DF_PATH = "./data/all_df/"      # Path to processed DataFrame 数据文件路径
OUTPUT_PATH = "./output/"            # Path for output files 输出文件路径

# Choosing track keyword 选择赛道关键词
market_keywords = "Shower Curtain Sets"

# Feature columns and their corresponding ranking order 特征列和对应的排名方式
feature_list = ["average_daily_growth_rate", "average_sales"]
ranking_order_list = [False, False]  # Ranking order: False for descending, True for ascending 排序方式：False为降序，True为升序
#Hope to calculate the growth rate over what time period and the average sales.
#希望计算多长时间段的增长率/以及平均销售额
day=30
def get_dict_list():
    """
    Retrieve the list of dictionary file paths 获取字典文件路径列表
    """
    return [os.path.join(RAW_DICT_PATH, f) for f in listdir(RAW_DICT_PATH)]

def get_predict_data_list():
    """
    Retrieve the list of prediction data file paths 获取预测数据文件路径列表
    """
    return [os.path.join(DATA_DF_PATH, f) for f in listdir(DATA_DF_PATH)]

def compute_growth_rate(products_csv, day):
    """
    Calculate average daily growth rate and average sales for the last n days 计算最近n天的平均日增长率和平均销量
    :param products_csv: The product's sales CSV data 产品的销售CSV数据
    :param day: Number of days to consider 考虑的天数
    :return: average daily growth rate and average sales 平均日增长率和平均销量
    """
    try:
        # Parse and clean sales data 解析并清理销售数据
        df_csv = pd.DataFrame(products_csv['df_SALES'])
        df_csv = df_csv[2:]
        df_csv.reset_index(inplace=True, drop=False)
        df_csv.rename(columns={'index': 'date'}, inplace=True)
        df_csv['date'] = pd.to_datetime(df_csv['date'], errors='coerce').dt.date

        # Aggregate data by date and fill missing days 按日期聚合数据并补全缺失日期
        date_index = pd.date_range(start=df_csv['date'].min(), end=df_csv['date'].max(), freq='D')
        df_csv = df_csv.groupby('date')['value'].max().reset_index(drop=False)
        df_csv = df_csv.set_index('date').reindex(date_index)
        df_csv.reset_index(inplace=True, drop=False)
        df_csv.rename(columns={'index': 'date'}, inplace=True)
        df_csv['date'] = pd.to_datetime(df_csv['date'], errors='coerce')

        # Calculate growth rate and average sales 计算增长率和平均销量
        df_csv["daily_growth_rate"] = df_csv["value"].pct_change()
        df_csv = df_csv.tail(day)
        average_daily_growth_rate = df_csv["daily_growth_rate"].mean()
        sales = df_csv["value"].mean()
        print(average_daily_growth_rate, sales)

        if average_daily_growth_rate is None or sales is None:
            print("Condition triggered: One or both values are None. 条件触发：一个或两个值为空。")
            return None, None
        return average_daily_growth_rate, sales
    except Exception as e:
        print(f"Error in compute_growth_rate: {e} 错误：增长率计算函数出错")
        return None, None

def process_and_flatten_data(products, key_list, min_sales_length=2, invalid_sales_values=[-1],
                             output_file="output.xlsx"):
    """
    Extract, filter, and flatten product data into a single row per product 根据关键字段提取、过滤并整合所有数据到一行中

    :param products: List of product dictionaries 产品字典列表
    :param key_list: Keys to extract for each product 需要提取的关键字段
    :param min_sales_length: Minimum length for valid SALES data SALES数据的最小长度
    :param invalid_sales_values: Invalid values in SALES data SALES中无效的值
    :param output_file: Output file name 输出文件名
    """
    extracted_product_data = []

    for product in products:
        if isinstance(product, dict):
            # Extract specified keys 提取指定字段
            flattened_product = {key: product.get(key, None) for key in key_list}

            # Check 'data' section 检查'data'部分
            data_section = product.get("data", {})
            if isinstance(data_section, dict):
                sales_data = data_section.get("SALES", [])
                if len(sales_data) >= min_sales_length and any(v not in invalid_sales_values for v in sales_data):
                    flattened_product["SALES"] = sales_data
                else:
                    flattened_product["SALES"] = "Invalid or Insufficient Data 无效或数据不足"

            extracted_product_data.append(flattened_product)
            flattened_df = pd.DataFrame(extracted_product_data)

            return flattened_df

def contains_keyword_recursive(data, keyword):
    """
    Recursively check for a keyword in nested data 递归检查嵌套数据中的关键词

    :param data: Nested data 嵌套数据
    :param keyword: Keyword to search for 要搜索的关键词
    :return: True if keyword is found 含关键词则返回True
    """
    if isinstance(data, dict):
        return any(contains_keyword_recursive(value, keyword) for value in data.values())
    elif isinstance(data, list):
        return any(contains_keyword_recursive(item, keyword) for item in data)
    elif isinstance(data, str):
        return keyword in data
    return False

def Organize_raw_data_and_create_CSV():
    """
    Process raw dictionary data and create a CSV 整理原始字典数据并生成CSV
    """
    csv_list = get_dict_list()
    all_processed_data = pd.DataFrame()
    for i in csv_list:
        try:
            print(f'Processing product code: {i}')
            dictfile = open(i, 'rb')
            products = pickle.load(dictfile)
            dictfile.close()
            products_csv = keepa.parse_csv(products[0]['csv'])
            key_list = ["categories", "asin", "productType", "trackingSince", "lastPriceChange", "variations",
                        "productGroup", "LISTPRICE", "description", "availabilityAmazon", "fbaFees", "categoryTree"]
            final_df = process_and_flatten_data(products, key_list, output_file="extracted_product_data.xlsx")
            if 'Invalid or Insufficient Data' in str(final_df['SALES'][0]):
                print('bad data')
                print(final_df['SALES'][0])
                continue
            if 'df_SALES' in products_csv.keys() and len(products_csv['df_SALES']) > 30:
                rate, sales = compute_growth_rate(products_csv, day=day)
                final_df['average_daily_growth_rate'] = rate
                final_df['average_sales'] = sales
            all_processed_data = pd.concat([all_processed_data, final_df], ignore_index=True)
        except Exception as err:
            error_message = f"Error processing product code {i}: {err}"
            logging.error(error_message)  # 记录错误日志
            print(error_message)

    # Add ranking columns 添加排名列
    for col, ascending in zip(feature_list, ranking_order_list):
        rank_col_name = f"{col}_rank"
        all_processed_data[rank_col_name] = all_processed_data[col].rank(ascending=ascending, method="min")

    all_processed_data["weight"] = all_processed_data[[f"{col}_rank" for col in feature_list]].sum(axis=1)
    all_processed_data = all_processed_data.sort_values(by="weight", ascending=True).reset_index(drop=True)
    filtered_file = os.path.join(OUTPUT_PATH, f"df_Amazon_{'average_sales'}.csv")
    all_processed_data.to_csv(filtered_file, index=False)

def read_and_deal():
    """
    Read processed data and filter by keyword 读取处理后的数据并通过关键词筛选
    """
    filtered_file = os.path.join(OUTPUT_PATH, f"df_Amazon_{'average_sales'}.csv")
    df = pd.read_csv(filtered_file)
    filtered_df = df[df['categoryTree'].apply(lambda x: contains_keyword_recursive(x, market_keywords))]
    filtered_df.reset_index(inplace=True, drop=True)
    filtered_df['Market Monopoly Rate'] = (filtered_df['average_sales'] / filtered_df['average_sales'].sum()) * 100
    filtered_file = os.path.join(OUTPUT_PATH, f"market_select_Amazon_{market_keywords}.csv")
    filtered_df.to_csv(filtered_file, index=False)

def main():
    """
    Main function 主函数
    """
    user_input_csv = input("Do you want to execute Organize_raw_data_and_create_CSV? (y/n): ").strip().lower()
    user_input_read = input("Do you want to execute read_and_deal? (y/n): ").strip().lower()
    if user_input_csv == 'y':
        print("Executing Organize_raw_data_and_create_CSV...")
        Organize_raw_data_and_create_CSV()
    else:
        print("Skipped Organize_raw_data_and_create_CSV.")
    if user_input_read == 'y':
        print("Executing read_and_deal...")
        read_and_deal()
    else:
        print("Skipped read_and_deal.")

if __name__ == '__main__':
    main()
