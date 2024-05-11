import numpy as np
import matplotlib.pyplot as plt

# CSVファイルのパス
csv_file = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler/Dead_Time1.csv'

# データの読み込み
data = np.loadtxt(csv_file, delimiter=',', skiprows=1)  # ヘッダー行をスキップ

# 時刻と温度データを分割
time_data = data[:, 0]
temp_data = data[:, 1:]  # Temp2, Temp3, Temp4 のデータ

# 移動平均のウィンドウサイズ
window_size = 5

# 移動平均を計算する関数
def moving_average(temp, window_size):
    return np.convolve(temp, np.ones(window_size) / window_size, mode='valid')

# 移動平均を適用
smoothed_temp_data = np.array([moving_average(temp, window_size) for temp in temp_data.T]).T

# 移動平均後の時間データ調整
adjusted_time_data = time_data[(window_size // 2):-(window_size // 2) or None]

# 無駄時間の算出関数
def find_first_change(time, temp, threshold=0.03):
    initial_temp = np.mean(temp[:7])
    for i in range(1, len(temp)):
        if abs(temp[i] - initial_temp) > threshold:
            return time[i] - 1  #オフセットを引く
    return None  # 変化が見つからない場合、Noneを返す

# 無駄時間の算出
dead_times = []
for i in range(smoothed_temp_data.shape[1]):
    dead_time = find_first_change(adjusted_time_data, smoothed_temp_data[:, i])
    dead_times.append(dead_time)

print("無駄時間:", dead_times)

def find_time_constant(time, temp):
    initial_temp = np.mean(temp[:7])
    final_temp = np.mean(temp[-600:])  # 最後の100点の平均を最終温度として使用
    target_temp = initial_temp + 0.632 * (final_temp - initial_temp)
    for i in range(len(temp)):
        if temp[i] >= target_temp:
            return time[i]
    return time[-1]  # 目標温度に達しない場合、最後の時刻を返す

time_constants = []
for i in range(smoothed_temp_data.shape[1]):
    time_constant = find_time_constant(adjusted_time_data, smoothed_temp_data[:, i])
    time_constants.append(time_constant)

print("一次遅れ時定数:", time_constants)

# # プロット
# plt.figure(figsize=(10, 6))
# for i in range(smoothed_temp_data.shape[1]):
#     plt.plot(adjusted_time_data, smoothed_temp_data[:, i], label=f'Smoothed Temp{i+2}')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Temperature (°C)')
# plt.title('Smoothed Temperature vs Time')
# plt.legend()
# plt.show()

# # グラフ2: オリジナルデータのプロット (最初の300個のデータ点)
# plt.figure(figsize=(12, 6))
# num_points_to_plot = 100  # 最初の300個のデータ点を表示
# for i in range(temp_data.shape[1]):
#     plt.plot(time_data[:num_points_to_plot], temp_data[:num_points_to_plot, i], label=f'Original Temp{i+2}')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Temperature (°C)')
# plt.title('Original Temperature Data (First 300 Points)')
# plt.legend()
# plt.show()