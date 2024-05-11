import ctypes
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyvisa
import csv
import os


###### set for CSV ######
# CSVファイルの保存先ディレクトリ
csv_dir = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data_Single_Thormocoupler'
csv_filename = os.path.join(csv_dir, 'Dead_Time3.csv')

# CSVファイルを作成してヘッダーを書き込む
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Temp2', 'Temp3', 'Temp4'])
#########################


###### set for PMX70-1A ######
# Initialize the resource manager and open the connection
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource('USB0::0x0B3E::0x1029::DP000053::INSTR')
time.sleep(1)

# # Turn on the output
# my_instrument.write('OUTP ON')
# time.sleep(1)
##############################


###### set for tc08 ######
# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# open unit
status["open_unit"] = tc08.usb_tc08_open_unit()
assert_pico2000_ok(status["open_unit"])
chandle = status["open_unit"]

# set mains rejection to 50 Hz
status["set_mains"] = tc08.usb_tc08_set_mains(chandle,0)
assert_pico2000_ok(status["set_mains"])

# set up channel
num_channels = 4
# therocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
typeK = ctypes.c_int8(75)
for channel in range(2, num_channels + 2):
    status[f"set_channel_{channel}"] = tc08.usb_tc08_set_channel(chandle, channel, typeK)
    assert_pico2000_ok(status[f"set_channel_{channel}"])

# get minimum sampling interval in ms
status["get_minimum_interval_ms"] = tc08.usb_tc08_get_minimum_interval_ms(chandle)
assert_pico2000_ok(status["get_minimum_interval_ms"])

# set tc-08 running
status["run"] = tc08.usb_tc08_run(chandle, status["get_minimum_interval_ms"])
assert_pico2000_ok(status["run"])
##########################


###### set for Matplotlib ######
# list for temperature and time
temperatures = []
timestamps = []

# プロット初期設定
fig, ax = plt.subplots()
lines = []
styles = ['-', '--', '-.']
colors = ['red', 'black', 'black']
labels = ['Temp2', 'Temp3', 'Temp4']
num_lines = 3
for i in range(num_lines):  # Four lines for three temps and one average
    line, = ax.plot([], [], linestyle=styles[i], color=colors[i], label=labels[i])
    lines.append(line)

ax.set_xlim(0, 10000)  # Set timestamp range
ax.set_ylim(38, 50)    # Set temperature range
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Temperature (°C)')

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    global timestamps, temperatures
    if timestamps:
        ax.set_xlim(min(timestamps), max(timestamps))  # Update the X-axis dynamically based on timestamps
    for i, line in enumerate(lines):
        line.set_data(timestamps, [temp[i] for temp in temperatures])  # Plot each temperature
    return lines

# Start animation
ani = FuncAnimation(fig, update, init_func=init, blit=True)
##########################

# Collect and display data in real-time
try:
    my_instrument.write('OUTP ON')
    time.sleep(1)
    my_instrument.write('CURR 1')
    my_instrument.write('VOLT 60')
    while True:
        # TC08 measures the temperature
        time.sleep(0.5)  # Wait for the sample
        overflow = ctypes.c_int16()
        times_ms_buffer = (ctypes.c_int32 * 1)()  # Buffer for one timestamp

        current_temperatures = []
        for channel in range(2, num_channels + 2):
            temp_buffer = (ctypes.c_float * 1)()  # Buffer for one channel
            status["get_temp"] = tc08.usb_tc08_get_temp(
                chandle,
                ctypes.byref(temp_buffer),
                ctypes.byref(times_ms_buffer),
                1,  # Number of samples to collect
                ctypes.byref(overflow),
                channel,  # Current channel number
                0,  # Units: Celsius
                1   # Fill missing
            )
            assert_pico2000_ok(status["get_temp"])
            current_temperatures.append(temp_buffer[0])

        temperatures.append(current_temperatures)
        time_sec = times_ms_buffer[0] / 1000  # ms -> sec
        timestamps.append(time_sec)
        plt.pause(0.01)  # Reload graph

        # CSVファイルにデータを追記
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time_sec, current_temperatures[0], current_temperatures[1], current_temperatures[2]])

except KeyboardInterrupt:
    ###### close for tc08 ######
    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)
    ############################

    ###### close for PMX70-1A ######
    # Set to 0 to stop the flow
    my_instrument.write('CURR 0')
    my_instrument.write('VOLT 0')
    time.sleep(1)  # Ensure commands are received

    # Turn off the output
    my_instrument.write('OUTP OFF')
    time.sleep(1)  # Ensure commands are received

    # Close the connection
    my_instrument.close()
    ################################