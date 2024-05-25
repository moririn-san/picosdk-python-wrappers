import numpy as np
import matplotlib.pyplot as plt

def generalized_logistic(t, k, T, a, v, b):
    """ 一般化されたロジスティック関数 """
    return k / ((1 + np.exp(-(t - a) / T))**v) + b

# パラメータの設定
k = 10    # 最大値
T = 32   # 時間定数
a = 50    # オフセット時間
v = 1     # 形状パラメータ
b = 42    # ベースライン

# 時間データの生成
t = np.linspace(0, 1000, 1000)  # 0 から 200 までの値を 400 点で生成

# 関数の評価
y = generalized_logistic(t, k, T, a, v, b)

# グラフの描画
plt.figure(figsize=(10, 6))
plt.plot(t, y, label='Generalized Logistic Model')
plt.xlabel('Time')
plt.ylabel('Response')
plt.title('Generalized Logistic Function')
plt.legend()
plt.grid(True)
plt.show()
