
# use this code to complete geometry dash level 1
from adb_connector_python.connector import Py_adb

device = Py_adb()


# ensure this is a touchable location on your device
x = 500
y = 700

# jump one time
def jump()->None:
    device.tap(x,y)

# jumps multiple time (times) with delay of 250ms
def jumps(times:int)->None:
    device.multitap(x=x,y=y,times=times,milliseconds=250)



# for this scope the besrt tool is tap_precision
# as it is the most precise and reliable


# notice that the timing changes between device so
# you have to test and modify milliseconds
# tested on Mi 12 lite with DELL XPS 15

def main():
    instructions = [
        {"milliseconds":0,"x":x,"y":y},
        {"milliseconds":1300,"x":x,"y":y},
        {"milliseconds":1300,"x":x,"y":y},
        {"milliseconds":250,"x":x,"y":y},
        {"milliseconds":250,"x":x,"y":y},
        {"milliseconds":2000,"x":x,"y":y},
        {"milliseconds":400,"x":x,"y":y},
        {"milliseconds":700,"x":x,"y":y},
        {"milliseconds":600,"x":x,"y":y},
        {"milliseconds":600,"x":x,"y":y},
        {"milliseconds":700,"x":x,"y":y},
        {"milliseconds":500,"x":x,"y":y},
        {"milliseconds":230,"x":x,"y":y},
        {"milliseconds":230,"x":x,"y":y},
        {"milliseconds":230,"x":x,"y":y},
        {"milliseconds":230,"x":x,"y":y},
        {"milliseconds":230,"x":x,"y":y},
        {"milliseconds":600,"x":x,"y":y},
        {"milliseconds":600,"x":x,"y":y},
        {"milliseconds":1500,"x":x,"y":y},
        {"milliseconds":240,"x":x,"y":y},
        {"milliseconds":900,"x":x,"y":y},
        {"milliseconds":300,"x":x,"y":y},
        {"milliseconds":600,"x":x,"y":y},
        {"milliseconds":700,"x":x,"y":y},
        {"milliseconds":240,"x":x,"y":y},
        {"milliseconds":240,"x":x,"y":y},
        {"milliseconds":240,"x":x,"y":y},
        {"milliseconds":240,"x":x,"y":y},
    ]
    device.precision_tap(instructions)
   
    


main()

