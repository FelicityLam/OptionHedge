#### MarketData

<img src="/Users/linbeibei/Library/Application Support/typora-user-images/image-20221128164233661.png" alt="image-20221128164233661" style="zoom:50%;" />

* **主要功能**：记录对冲端资产的市场行情数据

* **属性**：

    1. asset_category：list，说明MarketData所包含的资产类型（eg. stock, future, index, bond, interest, etc.）
    2. lot_size：list，记录每个asset最小交易的单位，比如股票就是100股为1手
    3. data：dict，key为资产类型和代码，value为对应的行情数据DataFrame

* **方法**：

    1. get_data(asset_type, code_list, start_date, end_date)：输入资产类型、代码以及起始日期，返回市场行情数据

* **股票数据示例**

    <img src="/Users/linbeibei/Library/Application Support/typora-user-images/image-20221128170345497.png" alt="image-20221128170345497" style="zoom:50%;" />

    1. 开盘价、收盘价、成交量、股票分红事件以及调整因子
    2. 考虑到股票分红会影响后续收益分析的计算，使用调整因子adj_factor对收益进行调整
        1. ISP_with_factor = ISP 累乘 adj_factor
        2. 调整后的期权收益 = notional *（Final Spot Price - ISP_with_factor * Strike）/ ISP_with_factor

