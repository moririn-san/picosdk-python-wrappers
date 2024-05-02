import pyvisa
import time

# Initialize the resource manager and open the connection
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource('USB0::0x0B3E::0x1029::DP000053::INSTR')

# Turn on the output
my_instrument.write('OUTP ON')

# Set the current
my_instrument.write('CURR 1')
# Set the voltage
my_instrument.write('VOLT 65')
time.sleep(180)  # Wait

# Set to 0 to stop the flow
my_instrument.write('CURR 0')
my_instrument.write('VOLT 0')

# Turn off the output
my_instrument.write('OUTP OFF')