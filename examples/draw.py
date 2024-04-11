# this code qllow you to draw a star on the screen of your device

# notice that the data may changes between devices
# tested on Mi 12 lite

from adb_connector_python.connector import Py_adb

device = Py_adb()



# change with your device specific points
def draw():
    center = 550
    right = 275
    left = 800
    bottom = 1600
    top = 700
    
    device.swipe(
        from_x=right,
        from_y=bottom,
        to_x=center,
        to_y=top
    )

    device.swipe(
        from_x=center,
        from_y=top,
        to_x=left,
        to_y=bottom
    )

    device.swipe(
        from_x=left,
        from_y=bottom,
        to_x=right - right/1.5,
        to_y=top + top /1.8
    )

    device.swipe(
        from_x=right - right/1.5,
        from_y=top + top /1.8,
        to_x=left + left/5,
        to_y=top + top /1.8
    )

    device.swipe(
        from_x=left + left/5,
        from_y=top + top /1.8,
        to_x=right,
        to_y=bottom
    )
           

draw()
