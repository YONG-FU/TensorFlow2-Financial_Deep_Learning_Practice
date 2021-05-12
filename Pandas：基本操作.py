import pandas as pd
import numpy as np

# 1. 导入Pandas库并简写为pd，并输出版本号
print(pd.__version__)

# 2. 从列表创建Series
arr = [0, 1, 2, 3, 4]
df = pd.Series(arr)
print(df)

# 3. 从字典创建Series
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
df = pd.Series(d)
print(df)

# 4. 从NumPy数组创建DataFrame
dates = pd.date_range('today', periods=6)  # 定义时间序列作为index
num_arr = np.random.randn(6, 4)  # 传入numpy随机数组
columns = ['A', 'B', 'C', 'D']  # 将列表作为列名
df = pd.DataFrame(num_arr, index=dates, columns=columns)
print(df)

# 5. 从CSV中创建 DataFrame，分隔符为;，编码格式为gbk
# df = pd.read_csv('test.csv', encoding='gbk, sep=';')

# 6. 从字典对象data创建DataFrame，设置索引为labels
data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
        'age': [2.5, 3, 0.5, np.nan, 5, 2, 4.5, np.nan, 7, 3],
        'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
df = pd.DataFrame(data, index=labels)
print(df)

# 7. 显示DataFrame的基础信息，包括行的数量；列名；每一列值的数量、类型
# 方法一
print(df.info())
# 方法二
# print(df.describe())

# 8. 展示df的前3行
# 方法一
print(df.iloc[:3])
# 方法二
# df.head(3)

# 9. 取出df的animal和age列
# 方法一
print(df.loc[:, ['animal', 'age']])
# 方法二
# df[['animal', 'age']]

# 10. 取出索引为[3, 4, 8]行的animal和age列
print(df.loc[df.index[[3, 4, 8]], ['animal', 'age']])

# 11. 取出age值大于3的行
print(df[df['age'] > 3])

# 12. 取出age值缺失的行
print(df[df['age'].isnull()])

# 13. 取出age在2和4间的行
print(df[(df['age'] > 2) & (df['age'] < 4)])

# 14. f行的age改为1.5
df.loc['f', 'age'] = 1.5
print(df.loc['f', 'age'])

# 15. 计算visits的总和
print(df['visits'].sum())

# 16. 计算每个不同种类animal的age的平均数
print(df.groupby('animal')['age'].mean())

# 17. 在df中插入新行k，然后删除该行
# 插入
df.loc['k'] = ['dog', 5.5, 2, 'no']
print(df)
# 删除
df = df.drop('k')
print(df)

# 18. 计算df中每个种类animal的数量
print(df['animal'].value_counts())

# 19. 先按age降序排列，后按visits升序排列
df = df.sort_values(by=['age', 'visits'], ascending=[False, True])
print(df)

# 20. 将priority列中的yes, no替换为布尔值True, False
df['priority'] = df['priority'].map({'yes': True, 'no': False})
print(df)

# 21. 将animal列中的snake替换为python
df['animal'] = df['animal'].replace('snake', 'python')
print(df)

# 22.对每种animal的每种不同数量visits，计算平均age，即，返回一个表格，行是animal种类，列是visits数量，表格值是行动物种类列访客数量的平均年龄
df = df.pivot_table(index='animal', columns='visits', values='age', aggfunc='mean')
print(df)
