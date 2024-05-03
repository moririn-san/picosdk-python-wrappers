import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

# list for temperature and time
temperatures = []
timestamps = []

# プロット初期設定
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')  # 初期化した空のプロット
ax.set_xlim(0, 10000)  # set timestamp range
ax.set_ylim(20, 100)  # set temperature range
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

# Collect and display data in real-time
try:
    while True:
        time.sleep(0.2)  # Wait for the sample
        temp_buffer = (ctypes.c_float * 1)()  # 1 channel buffer
        times_ms_buffer = (ctypes.c_int32 * 1)()
        overflow = ctypes.c_int16()
        status["get_temp"] = tc08.usb_tc08_get_temp(chandle, ctypes.byref(temp_buffer), ctypes.byref(times_ms_buffer), 1, ctypes.byref(overflow), 1, 0, 1)
        assert_pico2000_ok(status["get_temp"])
        print(f"Temperature = {temp_buffer[0]} °C, Timestamp = {times_ms_buffer[0]} ms")

        # データをリストに追加
        time_sec = times_ms_buffer[0] / 1000
        temperatures.append(temp_buffer[0])
        timestamps.append(time_sec)
        plt.pause(0.01)  # グラフを更新

except KeyboardInterrupt:
    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)