#### BaseOption

<img src="/Users/linbeibei/Desktop/截屏2022-11-28 上午11.53.23.png" alt="截屏2022-11-28 上午11.53.23" style="zoom:50%;" />

* **主要功能**
    1. 接收用户通过BackTest类传入的期权参数，根据BS公式计算期权价格，并在此基础上计算期权的希腊字母值
    2. 看涨看跌期权的价格、希腊字母计算公式不同，设置子类VanillaCall和VanillaOption继承BaseOption类

* **属性**
    1. underlying_asset：标的资产类型，对应MarketData类中的asset_category
    2. underlying_code：标的资产代码
    3. strike_date：起息日
    4. maturity：到期日
    5. ISP：Initial Spot Price $S_0$
    6. KSratio：K/ISP
    7. strike_level：根据KSratio判定OTM, ATM, ITM
    8. greeks：交易期间的希腊字母值delta, gamma, theta, vega
    9. BS_params：BS模型参数值spot_price, d1, d2, Nd1, Nd2, sigma, remain_period
    10. sigma_period：向前rolling sigma_period天，计算历史波动率替代隐含波动率

* **方法**
    1. cal_BS_params(): 计算BS公式参数，并存入BS_params
    2. cal_greeks()：基于BS_params计算希腊字母值，并存入greeks
* **子类：VanillaCall & VanillaPut**
    1. 拓展cal_BS_params()：除Call和Put的价格计算方法不同，剩余参数相同
    2. 重写cal_greeks()：Call和Put的部分希腊字母计算方法不同



