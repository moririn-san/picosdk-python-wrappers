import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyvisa

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
# therocouples types and int8 equivalent
# B=66 , E=69 , J=74 , K=75 , N=78 , R=82 , S=83 , T=84 , ' '=32 , X=88 
typeK = ctypes.c_int8(75)
status["set_channel"] = tc08.usb_tc08_set_channel(chandle, 1, typeK)
assert_pico2000_ok(status["set_channel"])

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
line, = ax.plot([], [], 'r-')  # 初期化した空のプロット
ax.set_xlim(0, 10000)  # set timestamp range
ax.set_ylim(20, 60)  # set temperature range
ax.set_xlabel('Time (sec)')
ax.set_ylabel('Temperature (°C)')

def init():
    line.set_data([], [])
    return line,

def update(frame):
    global temperatures, timestamps
    # プロット更新
    line.set_data(timestamps, temperatures)
    ax.set_xlim(min(timestamps), max(timestamps))  # グラフのX軸を動的に更新
    return line,

# start animation
ani = FuncAnimation(fig, update, init_func=init, blit=True)
##########################


###### set for PID ######
# PID parameters
set_temp = 50  # Set temperature
Kp = 40.0         # Propotinal gain
Ki = 0       # Integral gain
Kd = 0     # differential gain

# PID variables initialization
integral = 0.0
previous_error = 0.0
sample_time = 0.2  # サンプル時間（200ms）

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
        time.sleep(0.2)  # Wait for the sample
        temp_buffer = (ctypes.c_float * 1)()  # 1 channel buffer
        times_ms_buffer = (ctypes.c_int32 * 1)()
        overflow = ctypes.c_int16()
        status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer), ctypes.byref(times_ms_buffer), 1, ctypes.byref(overflow), 1, 0, 1)
        assert_pico2000_ok(status["get_temp"])
        # print(f"Temperature = {temp_buffer[0]} °C, Timestamp = {times_ms_buffer[0]} ms")

        # Add datas to list for Matplotlib
        time_sec = times_ms_buffer[0] / 1000 # ms -> sec, times_ms_buffer is int
        temperatures.append(temp_buffer[0])
        timestamps.append(time_sec)
        plt.pause(0.01)  # Reload graph

        ###### set for PID ######
        # Calculate PID
        voltage = calculate_pid(temp_buffer[0])
        # Apply the voltage to the instrument
        my_instrument.write(f'VOLT {voltage}') # PMX70-1A out put status is changed every 50ms
        #########################

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