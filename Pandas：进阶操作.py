import pandas as pd
import numpy as np

# 1. 有一列整数列A的DataFrame，删除数值重复的行
df = pd.DataFrame({'A': [1, 2, 2, 3, 4, 5, 5, 5, 6, 7, 7]})
print(df)
df1 = df.loc[df['A'].shift() != df['A']]
# 方法二
# df1 = df.drop_duplicates(subset='A')
print(df1)

# 2. 一个全数值DataFrame，每个数字减去该行的平均数
df = pd.DataFrame(np.random.random(size=(5, 3)))
print(df)
df1 = df.sub(df.mean(axis=1), axis=0)
print(df1)

# 3. 一个有5列的DataFrame，求哪一列的和最小
df = pd.DataFrame(np.random.random(size=(5, 5)), columns=list('abcde'))
print(df)
print(df.sum().idxmin())

# 4. 给定DataFrame，求A列每个值的前3大的B的和
df = pd.DataFrame({'A': list('aaabbcaabcccbbc'),
                   'B': [12, 345, 3, 1, 45, 14, 4, 52, 54, 23, 235, 21, 57, 3, 87]})
print(df)
df1 = df.groupby('A')['B'].nlargest(3).sum(level=0)
print(df1)

# 5. 给定DataFrame，有列A, B，A的值在1-100（含），对A列每10步长，求对应的B的和
df = pd.DataFrame({'A': [1, 2, 11, 11, 33, 34, 35, 40, 79, 99],
                   'B': [1, 2, 11, 11, 33, 34, 35, 40, 79, 99]})
print(df)
df1 = df.groupby(pd.cut(df['A'], np.arange(0, 101, 10)))['B'].sum()
print(df1)

# 6. 一个全数值的DataFrame，返回最大3值的坐标
df = pd.DataFrame(np.random.random(size=(5, 3)))
print(df)
print(df.unstack().sort_values()[-3:].index.tolist())

# 7. 给定DataFrame，计算每个元素至左边最近的0（或者至开头）的距离，生成新列y
df = pd.DataFrame({'X': [7, 2, 0, 3, 4, 2, 5, 0, 3, 4]})
# 标记0的位置
izero = np.r_[-1, (df['X'] == 0).to_numpy().nonzero()[0]]
idx = np.arange(len(df))
df['Y'] = idx - izero[np.searchsorted(izero - 1, idx) - 1]
print(df)

# 方法二
# x = (df['X'] != 0).cumsum()
# y = x != x.shift()
# df['Y'] = y.groupby((y != y.shift()).cumsum()).cumsum()

# 方法三
# df['Y'] = df.groupby((df['X'] == 0).cumsum()).cumcount()
#first_zero_idx = (df['X'] == 0).idxmax()
# df['Y'].iloc[0:first_zero_idx] += 1