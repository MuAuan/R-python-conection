import pyper
import pandas as pd

# Python で CSV のデータを読み出す
wine = pd.read_csv("wine.csv")

# R のインスタンスを作る
r = pyper.R(use_pandas='True')

# Python のオブジェクトを R に渡す
r.assign("data", wine)

# R のソースコードを実行する
r("source(file='scatter.R')")
print("wine")

# R のコードを実行する
r("res1 = cor.test(data$WRAIN, data$LPRICE2)")
r("data1 = subset(data, LPRICE2 < 0)")
r("res2 = cor.test(data1$WRAIN, data1$LPRICE2)")

# Python で R のオブジェクトを読む
res1 = pd.Series(r.get("res1"))
res2 = pd.Series(r.get("res2"))

print(res1)
"""
statistic                                     0.680681
parameter                                           25
p.value                                        0.50233
estimate                                      0.134892
null.value                                           0
alternative                                  two.sided
method            Pearson's product-moment correlation
data.name                  data$WRAIN and data$LPRICE2
conf.int       [-0.258366126613384, 0.489798400688013]
dtype: object
"""

print(res2)
"""
statistic                                    -0.129213
parameter                                           24
p.value                                       0.898266
estimate                                    -0.0263663
null.value                                           0
alternative                                  two.sided
method            Pearson's product-moment correlation
data.name                data1$WRAIN and data1$LPRICE2
conf.int       [-0.409535600260672, 0.364710477639889]
dtype: object
"""
