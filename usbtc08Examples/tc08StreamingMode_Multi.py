#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# TC-08 STREAMING MODE EXAMPLE


import ctypes
import numpy as np
import time
from picosdk.usbtc08 import usbtc08 as tc08
from picosdk.functions import assert_pico2000_ok

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
num_channels = 2
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

# Collect and display data in real-time
try:
    while True:
        time.sleep(2)  # Wait for the sample
        overflow = ctypes.c_int16()

        for channel in range(1, num_channels + 1):
            temp_buffer = (ctypes.c_float * 1)()  # Buffer for one channel
            times_ms_buffer = (ctypes.c_int32 * 1)()  # Buffer for one timestamp
            
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
            
            # Print the temperature and timestamp for the current channel
            print(f"Channel {channel}: T = {temp_buffer[0]} °C, Time = {times_ms_buffer[0]} ms")
except KeyboardInterrupt:
    # stop unit
    status["stop"] = tc08.usb_tc08_stop(chandle)
    assert_pico2000_ok(status["stop"])

    # close unit
    status["close_unit"] = tc08.usb_tc08_close_unit(chandle)
    assert_pico2000_ok(status["close_unit"])
    print(status)