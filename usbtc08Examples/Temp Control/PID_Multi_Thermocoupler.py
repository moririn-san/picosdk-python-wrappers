import ctypes
import numpy as np
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
csv_dir = '/Users/shingo/Documents/Temperature_Controller/picosdk-python-wrappers/usbtc08Examples/Temp Control/Data/PI_control'
csv_filename = os.path.join(csv_dir, 'Kp12R5_Ki0R01_Kd0.csv')

# CSVファイルを作成してヘッダーを書き込む
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Ave_Temp', 'Volt', 'Temp1', 'Temp2','Temp3', 'Room_Temp'])
#########################


###### set for PMX70-1A ######
# Initialize the resource manager and open the connection
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource('USB0::0x0B3E::0x1029::DP000053::INSTR')

# Turn on the output
my_instrument.write('OUTP ON')
time.sleep(1)

# Set the current and voltage
my_instrument.write('CURR 1')
my_instrument.write('VOLT 20')
time.sleep(1)  # Wait
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
for channel in range(1, num_channels + 1):
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
styles = ['-', '--', '-.', ':']
colors = ['black', 'black', 'black', 'red']  # All black for simplicity
labels = ['Temp1', 'Temp2', 'Temp3', 'Ave_Temp']
for i in range(4):  # Four lines for three temps and one average
    line, = ax.plot([], [], linestyle=styles[i], color=colors[i], label=labels[i])
    lines.append(line)

ax.set_xlim(0, 10000)  # Set timestamp range
ax.set_ylim(43, 52)    # Set temperature range
ax.axhline(50, color='blue', linewidth=0.8)  # 50°Cの位置に水平線を引く
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Temperature (°C)')
ax.legend()

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    global timestamps, temperatures
    for i, line in enumerate(lines):
        if i < 3:
            line.set_data(timestamps, [temp[i] for temp in temperatures])  # Plot each temperature
        else:
            line.set_data(timestamps, [np.mean(temp[:3]) for temp in temperatures])  # Plot average temperature
    ax.set_xlim(min(timestamps), max(timestamps))  # Update the X-axis dynamically
    return lines

# Start animation
ani = FuncAnimation(fig, update, init_func=init, blit=True)

##########################


###### set for PID ######
# PID parameters
set_temp = 50  # Set temperature
Kp = 12.5         # Propotinal gain
Ki = 0.01       # Integral gain
Kd = 0.0      # differential gain

# PID variables initialization
integral = 0.0
previous_error = 0.0
sample_time = 0.5  # サンプル時間 #1channel: 0.2sec #4channels: 0.5sec

# PID control logic
def calculate_pid(temp):
    global integral, previous_error
    error = set_temp - temp
    integral += error * sample_time
    derivative = (error - previous_error) / sample_time

    previous_error = error
    output = Kp * error + Ki * integral + Kd * derivative
    output = round(output, 2) # Round output to 2 decimal places
    output = max(0, min(output, 70)) # PMX70-1A Voltage is from 0 to 73.5V
    return output
#########################


# Collect and display data in real-time
try:
    while True:
        # TC08 measures the temperature
        time.sleep(sample_time)  # Wait for the sample
        overflow = ctypes.c_int16()
        times_ms_buffer = (ctypes.c_int32 * 1)()  # Buffer for one timestamp

        current_temperatures = []
        for channel in range(1, num_channels + 1):
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

        # Calculate PID
        ave_temp = sum(current_temperatures[:3]) / 3
        volt = calculate_pid(ave_temp)

        # Apply the voltage to the instrument
        my_instrument.write(f'VOLT {volt}')

        # CSVファイルにデータを追記
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time_sec, ave_temp, volt] + current_temperatures)


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