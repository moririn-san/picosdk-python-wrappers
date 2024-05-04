import csv
import matplotlib.pyplot as plt

# CSVファイルのパス
csv_filename = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/PID/Data/P_control/Kp20_2.csv'

# データを格納するためのリスト
times = []
temperatures = []
voltages = []

# CSVファイルを開いてデータを読み込む
with open(csv_filename, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # ヘッダー行をスキップ
    for row in csv_reader:
        time = float(row[0])
        if time >= 250:  # 250秒以降のデータのみ追加
            times.append(time)
            temperatures.append(float(row[1]))
            voltages.append(float(row[2]))
    # for row in csv_reader:
    #     times.append(float(row[0]))
    #     temperatures.append(float(row[1]))
    #     voltages.append(float(row[2]))

# 温度のグラフ
plt.figure(figsize=(10, 5))
plt.scatter(times, temperatures, label='Temperature (°C)', color='blue')  # 点でプロット
plt.axhline(50, color='green', linestyle='--', linewidth=1, label='Target Temperature (50°C)')  # 50°Cに線を引く
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')
plt.title('Kp = 20, Kd = 0.1')
plt.legend()
plt.grid(True)
# plt.savefig('/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/PID/Data/P_control/Temp_Kp20_2.png')  # PNGで保存
plt.show()

# 電圧のグラフ
plt.figure(figsize=(10, 5))
plt.scatter(times, voltages, label='Voltage (V)', color='red')  # 点でプロット
plt.axhline(70, color='purple', linestyle='--', linewidth=1, label='Target Voltage (70V)')  # 70Vに線を引く
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (V)')
plt.title('Kp = 20, Kd = 0.1')
plt.legend()
plt.grid(True)
# plt.savefig('/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/PID/Data/P_control/Volt_Kp20_2.png')  # PNGで保存
plt.show()
