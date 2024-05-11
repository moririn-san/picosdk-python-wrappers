import os
import csv
import matplotlib.pyplot as plt

# CSVファイル名
csv_filename = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler/Kp12R5_Ki0R05_Kd0.csv'

def read_data_from_csv(csv_filename):
    times = []
    temp1 = []
    temp2 = []
    temp3 = []
    room_temp = []
    volts = []
    integral_values = []  # integral_value を格納するリストを追加

    with open(csv_filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # ヘッダーをスキップ
        for row in csv_reader:
            times.append(float(row[0]))
            temp1.append(float(row[1]))
            volts.append(float(row[2]))
            temp2.append(float(row[3]))
            temp3.append(float(row[4]))
            room_temp.append(float(row[5]))
            integral_values.append(float(row[6]))  # 新しい列からのデータ読み込み

    return times, temp1, temp2, temp3, volts, room_temp, integral_values

def plot_temperature(times, temp1, temp2, temp3, room_temp, integral_values, save_path, csv_filename):
    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Temp'
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 温度データをプロット
    ax1.plot(times, temp1, label='Temp1', color='red')
    ax1.plot(times, temp2, label='Temp2', color='blue')
    ax1.plot(times, temp3, label='Temp3', color='green')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title(base_filename)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # integral_value を副軸にプロット
    ax2 = ax1.twinx()
    ax2.plot(times, integral_values, label='Integral Value', color='purple', linestyle='--')
    ax2.set_ylabel('Integral Value')
    ax2.legend(loc='upper right')

    # グラフを保存
    plt.savefig(os.path.join(save_path, graph_filename))
    plt.close()

def plot_voltage(times, volts, save_path, csv_filename):
    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Volt'
    plt.figure(figsize=(10, 5))
    plt.plot(times, volts, label='Voltage', color='purple')
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
times, temp1, temp2, temp3, volts, room_temp, integral_values = read_data_from_csv(csv_filename)

# 温度グラフをプロットして保存
plot_temperature(times, temp1, temp2, temp3, room_temp, integral_values, save_path, csv_filename)

# 電圧グラフをプロットして保存
plot_voltage(times, volts, save_path, csv_filename)
