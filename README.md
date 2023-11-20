# 在不知道表名和字段名的情况下，查找出哪些字段里包含“关键字”的数据。

A) 产品经理：帮我查一下数据，但我忘记是哪个表了。

B) 研发经理：我也忘记了。

### 需求：在不知道表名和字段名的情况下，查找出哪些字段里包含“关键字”的数据。

#### DBA解决思路：用python全量扫描跑批，涉及到varchar的字段都扫一遍。
--------------------------------------------------------------------
```
shell> vim find_key.py（更改数据库配置信息）
shell> python3 find_key.py
```

运行find_key.py脚本，默认并发10个线程 - 地毯式搜索，最后会在当前目录下输出符合条件的库名、表名和字段名至result.txt文件里，交付给产品经理。

```
shell> cat result.txt 
库名: test，表名: sbtest1，列名: pad
(1000000, 497681, '24370733566-51322813884-74586826122-88962939071-35932193453-18408167444-46946055568-46329009755-48767794996-38200513642', 'NBA')
-------------------------------------------------------
库名: test，表名: sbtest1_bak_20231110，列名: pad
(1000000, 497681, '24370733566-51322813884-74586826122-88962939071-35932193453-18408167444-46946055568-46329009755-48767794996-38200513642', 'NBA')
-------------------------------------------------------
```
