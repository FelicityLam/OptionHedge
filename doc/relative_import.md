<!--
 * @Author: LetheYE
 * @email: mengjie_ye@stu.pku.edu.cn
 * @Date: 2022-11-26 14:11:18
 * @LastEditTime: 2022-11-26 14:18:37
 * @FilePath: \QTA_option_proj\doc\relative_import.md
-->
# 对于项目管理里面的import说明

## 参考资料
1. [Python 3.x | 史上最详解的 导入（import）](https://blog.csdn.net/weixin_38256474/article/details/81228492?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-81228492-blog-77734346.pc_relevant_recovery_v2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-81228492-blog-77734346.pc_relevant_recovery_v2&utm_relevant_index=3)

## 心得体会
1. python test_data.py 这个test_data.py要在根目录QTA_option_proj下面
2. test_data里面import的东西 按照root下的路径 进行
   1. 比如 `from src.MarketData import MarketData`
3. 对于test_date.py里面import的module： 它里面的import用相对于这个module的相对路径点点点，但是存储读取文件的时候路径以root开始
   1. 比如我们在test_data里面import single_stock_data的时候
      -  `from src.MarketData.single_stock_data import single_stock_data`
         - 在single_stock_data里面的import是用的`from .MarketData import MarketData`和 `from ..tools import date_time_to_int` 
         - 同时，这里面save_file的时候，用的是从root开始的路径`data.to_csv('data/MarketData/single_stock_data.csv')`
