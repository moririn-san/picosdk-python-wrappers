import csv
import matplotlib.pyplot as plt

# PIDコントローラのパラメータ
Kp = 12.5
Ki = 1
Kd = 0.05

# ファイル名に使うパラメータをフォーマット
def format_parameter(value):
    return str(value).replace('.', 'R')

# コントロールタイプの選択
# Uncomment the line corresponding to the folder you want to use
# control_type = "P_control"
# control_type = "PI_control"
# control_type = "PD_control"
control_type = "PID_control"

# 保存先のパス
save_path = f'/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data/{control_type}'

# CSVファイル名の生成
csv_filename = f'{save_path}/Kp{format_parameter(Kp)}_Ki{format_parameter(Ki)}_Kd{format_parameter(Kd)}.csv'

# データを格納するためのリスト
full_times = []
times = []
temperatures = []
voltages = []
full_temperatures = []
full_voltages = []

# CSVファイルを開いてデータを読み込む
with open(csv_filename, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # ヘッダー行をスキップ
    for row in csv_reader:
        time = float(row[0])
        temperature = float(row[1])
        voltage = float(row[2])
        full_times.append(time)
        full_temperatures.append(temperature)
        full_voltages.append(voltage)
        if time >= 250:  # 250秒以降のデータのみ追加
            times.append(time)
            temperatures.append(temperature)
            voltages.append(voltage)

def plot_graph(times, data, ylabel, target, target_label, color, title_suffix, filename_suffix):
    filename = f'Kp{format_parameter(Kp)}_Ki{format_parameter(Ki)}_Kd{format_parameter(Kd)}_{ylabel}_{filename_suffix}.png'
    plt.figure(figsize=(10, 5))
    plt.scatter(times, data, label=f'{ylabel} ({ylabel[0]})', color=color)
    plt.axhline(target, color='green', linestyle='--', linewidth=1, label=f'Target {target_label} ({target}{ylabel[0]})')
    plt.xlabel('Time (seconds)')
    plt.ylabel(f'{ylabel} ({ylabel[0]})')
    plt.title(f'Kp = {Kp}, Ki = {Ki}, Kd = {Kd}, {title_suffix}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{save_path}/{filename}')

# 全時間の温度グラフ
plot_graph(full_times, full_temperatures, 'Temperature', 50, 'Temperature', 'blue', 'Full Time', 'Temp_Full')
# 250秒以降の温度グラフ
plot_graph(times, temperatures, 'Temperature', 50, 'Temperature', 'blue', '250s and Beyond', 'Temp_250s')
# 全時間の電圧グラフ
plot_graph(full_times, full_voltages, 'Voltage', 70, 'Voltage', 'red', 'Full Time', 'Volt_Full')
# 250秒以降の電圧グラフ
plot_graph(times, voltages, 'Voltage', 70, 'Voltage', 'red', '250s and Beyond', 'Volt_250s')