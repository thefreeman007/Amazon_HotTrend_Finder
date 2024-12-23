### **README**

---

#### **Project Name: Amazon HotTrend Finder**
The project is a personal skill showcase and is strictly prohibited from commercial use without my consent. This project is merely a template and requires minor adjustments tailored to specific industries and products before formal deployment. The prerequisite for usage is having relevant data. Due to legal restrictions, this project does not provide data. Please store Amazon's raw data in the `all_dict` directory.

#### **Project Overview**
This project is designed to assist businesses in identifying trending products and potential best-sellers through big data analysis. It combines programmatic data analysis with traditional research methodologies common in the investment and research industry. The program scores potential best-sellers based on user-defined evaluation criteria. Products with high scores and low monopoly rates are likely to be best-sellers.

---

### **Usage Instructions**
1. Review the data example file `data_example.py`. For legal reasons, only empty data is displayed in the example. During actual usage, data will have valid content.
   
2. **Execution Steps:**
   - **Step 1:** Run the first function: `Executing Organize_raw_data_and_create_CSV`, choose `y`. This will generate a CSV file in the `output` directory.
   - According to **Venture Capital (VC)** principles, products with high growth rates and low market monopoly rates often exhibit sustained growth potential and high investment value. 
   - To avoid markets with low volume and low profit margins, the program focuses on two key features: `["average_daily_growth_rate", "average_sales"]`, ensuring relatively high growth rates and substantial markets.
   - You can modify the code for your needs, but even with modifications, the code must not be used commercially without my permission.
   - **Key Settings:**
     ```
     feature_list = ["average_daily_growth_rate", "average_sales"]
     ranking_order_list = [False, False]  # False = descending, True = ascending
     ```
     These settings rank products higher with greater values in these features.
   - After running the program,
![images](images/pic.png)
a column `average_sales_rank` will show the product with the highest sales during the specified `day`. Features in `feature_list` are summed to calculate the overall weight, providing a comprehensive evaluation.

3. **Step 2:** Select a top-weight product, e.g., a product in the **"Shower Curtain Sets"** category, which shows high growth and significant sales, indicating a strong potential to capture market share.

4. Modify the variable `market_keywords = "Shower Curtain Sets"` and run the second function: `Executing read_and_deal`. This will generate an additional column: **Market Monopoly Rate**. 
   - Due to sample limitations (about 2,000 random products), we observe that "Shower Curtain Sets" products show extremely low monopoly rates, with each seller capturing around one-third of the market share.
   - This suggests the product category is both high-growth and low-monopoly, making it a viable market entry point.

#### **Real-World Validation**
Using older sample data from 2020–2021, the analysis highlighted potential best-sellers. Revisiting these categories after four years, many products now have hundreds to thousands of reviews. Estimating approximately 20–50 real sales per review, the selected products demonstrate significant potential. This validates the project’s ability to identify promising market opportunities.

**Disclaimer**: The data in this project is outdated and should not be used to guide current decisions.

---

### **Core Features**
1. **Data Cleaning and Integration**
   Extract useful information from raw data and organize it structurally.

2. **Growth Rate Calculation**
   Analyze product sales trends and provide average daily growth rates.

3. **Monopoly Rate Analysis**
   Calculate market share based on sales data.

4. **Product Filtering and Ranking**
   Use custom keywords to filter specific product categories, generating rankings and weight-based analyses.

**Outputs**: Save results as CSV or Excel files for further analysis.

---

### **Contact Information**
**Email**: 402868327@qq.com

---

---

### **README**

---

#### **项目名称：Amazon HotTrend Finder**
该项目为个人技能展示项目，未经许可，严禁商用。本项目为模板，需根据具体行业和商品进行少量调整后方可正式投入使用。使用前提是拥有相关数据。因法律限制，本项目不提供数据，请将亚马逊原始数据存放在 `all_dict` 目录下。

#### **项目简介**
本项目旨在通过大数据分析帮助企业寻找热点商品和潜在爆款商品。结合程序的大数据分析能力以及传统投研行业的通用分析手段，对潜在爆款商品进行评分。得分高且垄断率低的商品更可能成为爆款。

---

### **使用说明**
1. 查看示例文件 `data_example.py`，因法律原因，示例数据为空。在实际操作中，数据会包含有效内容。
   
2. **执行步骤：**
   - **步骤1**：运行第一个功能 `Executing Organize_raw_data_and_create_CSV`，选择 `y`。生成的 CSV 文件将存储在 `output` 目录中。
   - 根据 **风险投资 (VC)** 的基本原理，增长率高、垄断率低的商品往往具有高增长潜力和投资价值。
   - 为避免低市场规模和低利润商品，程序优先关注两个关键特征：`["average_daily_growth_rate", "average_sales"]`，确保高增长率且市场较大。
   - **关键设置**：
     ```
     feature_list = ["average_daily_growth_rate", "average_sales"]
     ranking_order_list = [False, False]  # False = 降序, True = 升序
     ```
     设置特征值排名方式，数值越高排名越靠前。
   - 程序运行后，
![images](images/pic.png)
    `average_sales_rank` 列为指定时期中销售额最高的商品。`feature_list` 中所有特征相加，生成综合权重 `weight`，评估商品优劣。

3. **步骤2**：选择高权重商品，如 **"Shower Curtain Sets"** 类商品。该类商品显示出高增长且销售额大，表明有机会瓜分市场份额。

4. 修改变量 `market_keywords = "Shower Curtain Sets"`，运行第二个功能 `Executing read_and_deal`。新增列 **Market Monopoly Rate**。 
   - 样本中显示 "Shower Curtain Sets" 类商品垄断率极低，每个卖家约占三分之一市场份额。
   - 表明该类商品增长率高且垄断性低，是一个理想的市场切入点。

#### **实际验证**
使用2020-2021年的历史数据分析发现潜在爆款商品，四年后复盘，多数商品评论量达数百到数千条。假设每条评论对应20-50次真实销量，这些商品展现了巨大的市场潜力，验证了项目的有效性。

**免责声明**：本项目数据为历史数据，勿将分析结果用于当前决策。

---

### **核心功能**
1. **数据清洗与整合**
   从原始数据中提取有用信息并结构化整理。

2. **增长率计算**
   分析商品销量趋势，提供平均每日增长率。

3. **垄断率分析**
   根据销量数据计算市场份额。

4. **商品筛选与排名**
   通过自定义关键词筛选特定商品类别，生成排名与权重分析。

**输出**：保存为 CSV 或 Excel 文件，便于进一步分析。

---

### **联系方式**
**邮箱**：402868327@qq.com
