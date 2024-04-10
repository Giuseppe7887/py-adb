# this code allow you to unlock your device and call someone
from adb_connector_python.connector import Py_adb

device = Py_adb()

# set this fields
phone_password = ""
number_to_call =""

device.unlock_screen(password=phone_password)

device.call(phone_number=number_to_call)