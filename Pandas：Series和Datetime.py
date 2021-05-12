import pandas as pd
import numpy as np

# 1. 创建Series，将2020所有工作日作为随机值的索引
dti = pd.date_range(start='2020-01-01', end='2020-12-31', freq='B')
s = pd.Series(np.random.rand(len(dti)), index=dti)
print(s.head(10))

# 2. 所有礼拜三的值求和
print(s[s.index.weekday == 2].sum())

# 3. 求每个自然月的平均数
print(s.resample('M').mean())

# 4. 每连续4个月为一组，求最大值所在的日期
print(s.groupby(pd.Grouper(freq='4M')).idxmax())

# 5. 创建2020-2021每月第三个星期四的序列
print(pd.date_range('2020-01-01', '2021-12-31', freq='WOM-3THU'))
