# Portfolio

属性:

option_type：期权组合的类型（垂直差价组合、水平差价组合、对角组合、看涨+看跌组合）

- 类型：str

option_list: portfolio里包含的期权组合

	- 类型：list，记录Vanilla的position

 - keys: option_object, option_position
 - values: VanillaCall/VanillaPut, int

greek_df：每个交易日的希腊字母的值

- 类型: pandas.dataframe
- index: trade_dates
- columns: 'option_price', 'delta', 'gamma', 'vega', 'theta'

BS_paras_df: 按照每个交易日计算得到的时变参数信息

- 类型: pandas.dataframe
- index: trade_dates
- columns: 'sigma', 'left_days', 'left_times', 'sigma_T', 'stock_price'

decompose_df:  每个交易日的pnl

- 类型：pandas.DataFrame

- index：trade_dates

- columns：'option_pnl','delta_pnl', 'theta_pnl', 'gamma_pnl', 'vega_pnl', 'higher_order_pnl'



方法：

get_option_list：

​	根据传入的期权组合类型和参数生成对应position的Vanilla，加入option_list中

​	同时调用对应Vanilla的set_paras_by_dict(parameter)

- 参数：self, para_dict

cal_BS_params

​	调用option_list中每个Vanilla的cal_BS_params()计算参数

calculate_greeks:

​	计算期权组合的希腊值，调用Vanilla的cal_greeks()，等于Vanilla greek_df的加权平均
$$
portofolio\_greeks = \sum_{i=0}^n optioni\_greeks\times optioni\_position
$$
calculate_return_decomposition：

​	计算option_pnl和每个希腊字母上的pnl，保存到self.decompose_df中
$$
\begin{equation*}
    \begin{split}
       df & = \frac{\partial f}{\partial S} dS + \frac{1}{2}\frac{\partial^2 f}{\partial S^2}{dS}^2 + \frac{\partial f}{\partial t} dt 
       + \frac{\partial f}{\partial \sigma} d\sigma + \epsilon \\
       & = \Delta dS + \frac{1}{2}\Gamma({dS}^2) + \theta dt + vd\sigma + \epsilon \\
       & = \Delta dS + \frac{1}{2}\Gamma({dS}^2) + v d\sigma + (rf-\Delta Sr-\frac{1}{2}\Gamma S^2\sigma^2) dt
    \end{split}
\end{equation*}
$$

$$
\begin{equation*}
\begin{split}
& option\_pnl = option\_value.diff() \\
& delta\_pnl = delta\times \Delta S = delta\times\Delta r\times S = cash\_delta\times \Delta r \\
& gamma\_pnl = \frac{1}{2}\times gamma\times(\Delta S)^2 = \frac{1}{2}\times cash\_gamma/S^2\times100\times(\Delta S)^2 \\
& theta\_pnl = -\frac{1}{2}\times gamma\times S^2\times \sigma^2\times \Delta t = -\frac{1}{2}\times cash\_gamma/S^2\times100\times S^2\times \sigma^2\times \Delta t \\
& disc\_pnl = rf\times \Delta t \\
& carry\_pnl = -delta\times S\times r\times \Delta t = -cash\_delta\times r\times \Delta t
\end{split}
\end{equation*}
$$

​	用cash_delta和cash_gamma计算，度量按标的涨幅计算的现金暴露规模，

​	交易员关注1%的价格变动对组合价值变化了多少钱

​	在计算股指期货的pnl的时候还要考虑basis_pnl，对冲端的pnl一部分来自指数的损益，一部分来自基差损益

```python
def calculate_return_decomposition(self):
        self.decompose_df.loc[:, 'option_pnl'] = ...
        self.decompose_df.loc[:, 'delta_pnl'] = ...
        self.decompose_df.loc[:, 'gamma_pnl'] = ...
        self.decompose_df.loc[:, 'theta_pnl'] = ...
        self.decompose_df.loc[:, 'higher_order_pnl'] = ...
       
```



# Strategy

输入greek_df和stock_price，返回每个交易日对应标的的position

属性：

multiplier：记录标的资产的最小可交易单位，例如股票为100股

- 类型：int

position：根据notional和每日的greeks以及每日的spot_price计算出每日的position

 - 类型：pandas.Series

   

方法:

cal_position：

​	根据策略类型和每个交易日的股价计算每天的position，返回spot_position

​	例如用多个不同期限结构的future对冲，那么如何分配权重，也写在这个方法中

​	不同的strategy，重写这个方法

- 参数：self, greek_df
- 返回：position

HedgeAllStrategy: 每个交易日让投资组合达到delta中性
$$
position = -cash\_delta/stock\_price/multiplier
$$
HedgeHalfStrategy: 每天对冲一半的delta

- - 



