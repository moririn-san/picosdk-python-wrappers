import os
import pandas as pd
import matplotlib.pyplot as plt

# CSVファイル名
csv_filename = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Multi/Kp13R2_Ki0R06_Kd363.csv'

# データを読み込む関数
def read_data_from_csv(csv_filename):
    # Pandasを使ってCSVデータを読み込む
    df = pd.read_csv(csv_filename)
    return df

# 温度グラフをプロットして保存する関数
def plot_temperature(df, save_path, csv_filename):
    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Temp'
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 温度データをプロット
    ax1.plot(df['Time'], df['Channel2'], label='Channel2', color='orange')
    ax1.plot(df['Time'], df['Channel3'], label='Channel3', color='blue')
    ax1.plot(df['Time'], df['Channel4'], label='Channel4', color='green')
    ax1.plot(df['Time'], df['Ave_Temp'], label='Ave Temp', color='red')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title(base_filename)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Integral Valueを副軸にプロット
    ax2 = ax1.twinx()
    ax2.plot(df['Time'], df['Integral'], label='Integral', color='purple', linestyle='--')
    ax2.set_ylabel('Integral Value')
    ax2.legend(loc='upper right')

    # グラフを保存
    plt.savefig(os.path.join(save_path, graph_filename))
    plt.close()


# 電圧グラフをプロットして保存する関数
def plot_voltage(df, save_path, csv_filename):
    base_filename = os.path.splitext(os.path.basename(csv_filename))[0]
    graph_filename = base_filename + '_Volt'
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Volt'], label='Voltage', color='purple')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')
    plt.title(base_filename)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, graph_filename))
    plt.close()

# 保存先ディレクトリの指定
save_path = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Multi'

# データを読み込む
df = read_data_from_csv(csv_filename)

# 温度グラフをプロットして保存
plot_temperature(df, save_path, csv_filename)

# 電圧グラフをプロットして保存
plot_voltage(df, save_path, csv_filename)