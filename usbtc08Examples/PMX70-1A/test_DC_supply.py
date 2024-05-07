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
my_instrument.write('VOLT 60')
time.sleep(60)  # Wait

# Set to 0 to stop the flow
my_instrument.write('CURR 0')
my_instrument.write('VOLT 0')
time.sleep(1)  # Ensure commands are received

# Turn off the output
my_instrument.write('OUTP OFF')
time.sleep(1)  # Ensure commands are received

my_instrument.close()