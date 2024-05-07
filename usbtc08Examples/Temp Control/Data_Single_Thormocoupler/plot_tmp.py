import os
import csv
import matplotlib.pyplot as plt

csv_filename = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler/Kp12R5_Ki0R05_Kd0.csv'
# 開始時間を設定
start_time = 600  # 例: 200秒後からのデータを表示

def read_data_from_csv(csv_filename):
    times = []
    temp1 = []
    temp2 = []
    temp3 = []
    volts = []

    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # ヘッダーをスキップ
        for row in csv_reader:
            times.append(float(row[0]))
            temp1.append(float(row[1]))
            volts.append(float(row[2]))
            temp2.append(float(row[3]))
            temp3.append(float(row[4]))

    return times, temp1, temp2, temp3, volts

def plot_temperature(times, temp1, temp2, temp3, save_path, csv_filename, start_time=0):
    # フィルタリング
    filtered_indices = [i for i, time in enumerate(times) if time >= start_time]
    filtered_times = [times[i] for i in filtered_indices]
    filtered_temp1 = [temp1[i] for i in filtered_indices]
    filtered_temp2 = [temp2[i] for i in filtered_indices]
    filtered_temp3 = [temp3[i] for i in filtered_indices]

    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Temp.png'
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_times, filtered_temp1, label='Temp1', color='red')
    plt.plot(filtered_times, filtered_temp2, label='Temp2', color='blue')
    plt.plot(filtered_times, filtered_temp3, label='Temp3', color='green')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (°C)')
    plt.title(base_filename)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, graph_filename))
    plt.close()

def plot_voltage(times, volts, save_path, csv_filename, start_time=0):
    # フィルタリング
    filtered_indices = [i for i, time in enumerate(times) if time >= start_time]
    filtered_times = [times[i] for i in filtered_indices]
    filtered_volts = [volts[i] for i in filtered_indices]

    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Volt.png'
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_times, filtered_volts, label='Voltage', color='purple')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.title(base_filename)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, graph_filename))
    plt.close()

# 保存先ディレクトリの指定
save_path = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler'

# データを読み込む
times, temp1, temp2, temp3, volts = read_data_from_csv(csv_filename)

# 温度グラフをプロットして保存
plot_temperature(times, temp1, temp2, temp3, save_path, csv_filename, start_time)

# 電圧グラフをプロットして保存
plot_voltage(times, volts, save_path, csv_filename, start_time)
