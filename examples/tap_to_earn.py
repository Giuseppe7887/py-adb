from adb_connector_python.connector import Py_adb


device = Py_adb()

device.multitap(times=0,x=700,y=1600)