import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def step_response(t, k, T, a, b, v):
    """ ロジスティックステップ応答モデル """
    return k / ((1 + np.exp(-(t - a) / T))**v) + b

# CSVファイルのパスを指定
csv_filename = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler/Dead_Time1.csv'
# CSVファイルの読み込み
data = pd.read_csv(csv_filename)
time = data['Time']
response = data['Temp2']  # Temp2を例として使用

# 移動平均の適用
# response_smoothed = response.rolling(window=100, center=True).mean()
response_smoothed = response.rolling(window=100, center=True).mean()

# 移動平均でNaNが発生するので、有効なデータのみをフィットに使用
valid_indices = ~response_smoothed.isna()
time_valid = time[valid_indices]
response_smoothed_valid = response_smoothed[valid_indices]

# パラメータのフィッティング
# パラメータの境界を設定
bounds = ([10.1, 300.5, -4000, -4000, 80], [3000.1, 500.1, -1000, 43.5, 200.5])
popt, pcov = curve_fit(step_response, time_valid, response_smoothed_valid, bounds=bounds)

# フィット結果の表示
k_fit, T_fit, a_fit, b_fit, v_fit = popt
print(f"Fitted parameters: k = {k_fit}, T = {T_fit}, a = {a_fit}, b = {b_fit}, v = {v_fit}")

# フィット結果のプロット
plt.figure(figsize=(10, 6))
plt.plot(time, response, 'b-', label='Original Data')
plt.plot(time, response_smoothed, 'g-', label='Smoothed Data')  # 追加: 移動平均データのプロット
plt.plot(time_valid, step_response(time_valid, *popt), 'r--', label='Fitted Model')
plt.xlabel('Time')
plt.ylabel('Response')
plt.legend()
plt.title('Fit of Step Response Model to Data')
plt.grid(True)
plt.show()
