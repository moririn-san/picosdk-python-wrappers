import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルの読み込み
df = pd.read_csv('/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Multi_5secAve/Kp10R5_Ki0R0175_Kd350.csv')

# 指定した時間範囲でデータをフィルタリング
filtered_df = df[(df['Time'] >= 1500) & (df['Time'] <= 4000)]

fig, ax1 = plt.subplots()

# Temp2を主軸にプロット
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Ave_Temp (°C)', color='tab:red')
ax1.plot(filtered_df['Time'], filtered_df['Ave_Temp'], color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

# Integral_Valueを副軸にプロット
ax2 = ax1.twinx()  # 共有X軸で新たなY軸を作成
ax2.set_ylabel('Integral Value', color='tab:blue')
ax2.plot(filtered_df['Time'], filtered_df['Integral_Value'], color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# グラフの表示
plt.title('Temperature and Integral Value')
plt.show()
