__author__ = "Jonathan Braun"
__version__ = "1.0"
__maintainer__ = "Jonathan Braun"
__email__ = "jonathan.braun@eduvaud.ch"
__status__ = "Prototype"
__date__ = "February 2023"

#-----------------------------------------------------
# Importing libraries and modules
#-----------------------------------------------------
import datetime                                                             # Library for date and time related stuff
import math                                                                 # Library for math stuff
import csv                                                                  # Library for csv handling stuff

from sensirion_i2c_driver import I2cConnection                              # Sensor driver
from sensirion_i2c_sht.sht4x import Sht4xI2cDevice                          # Sensor driver
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver  # Sensor driver

#-----------------------------------------------------
# Declaring the sensor object
#-----------------------------------------------------
sht40 = Sht4xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-2')))

#-----------------------------------------------------
# Declaring functions
#-----------------------------------------------------
def read_sensor():
    try:
        t, rh = sht40.single_shot_measurement()
        # Watch out! t and rh are variable that contain not only the values but also the units.
        # You can print the values with the units (print(t)) or you can also recover only the value
        # by specifying which one: t.degrees_celsius or rh.percent_rh
    except Exception as ex:
        print("Error while recovering sensor values:", ex)
    else:
        return t, rh

    return 0 # In case something went wrong

# def calculate_dew_point(temp, humidity):
#     # Calculate dew point here
#     return dp
#
# def csv_write_row(file_path, data_row):
#     try:
#     # Write csv here
#     except Exception as ex:
#         return 0, ex
#     else:
#         return 1

#-----------------------------------------------------
# Main script
#-----------------------------------------------------
if __name__ == "__main__":  # Runs only if called as a script but not if imported
    print("Hello and welcome to EMSY")

#    temperature, humidity = read_sensor()
#    dew_point = calculate_dew_point(temperature.degrees_celsius, humidity.percent_rh)







