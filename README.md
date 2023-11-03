# PY-ADB

<i style="font-weight:200">
    This is a package to command android device with Python, it use <b>ADB</b>, so if you don't have it, plaese install it before.
</i>

Tested on <code>Windows 11</code>, <code>Linux Ubuntu 22.04.1</code> and <code>Linux Mint 21.1</code>

## <code>REQUIREMENTS</code>

* [Python > 3.10](https://www.python.org/)
* [ADB](https://developer.android.com/tools/adb?hl=it) 

```bash
# WINDOWS
choco install adb

# LINUX
sudo apt-get install android-tools-adb

# MAC
brew install android-platform-tools
```

<i style="font-weight:200">
    Using PY-ADB is simple, just clone the repo <a href="https://github.com/Giuseppe7887/py-adb" >py-adb</a> then move to PY-ADB directory just created, then create new script to use it
</i>

<hr/>

```bash
git clone https://github.com/Giuseppe7887/py-adb
cd PY-ADB
# create main.py file
```

## <code>EXAMPLES</code>

```python
# in main.py
from py_adb import Py_adb

adb_connector = Py_adb() 

print(adb_connector.ADB_VERSION) #  1.0.41
print(adb_connector.ADB_EXECUTABLE) # /usr/bin/adb
```

#### <code>BASIC INFO</code>

```python
adb_connector.list_devices()
# [ { "id":"fh8swx9cs", "status":"device" }, { "id":"2439vjsacs", "status":"unauthorized" } ]

adb_connector.is_adb_running() # it runs on every action and raise exception if adb is not running
# True

adb_connector.get_first_avaiable_device()
# { "id":"fh8swx9cs", "status":"device" }

adb_connector.phone_data()
# {
#    "battery_data":{ "is_charging":True, "level":64 },
#    "device_data":{ "model":"AS3D24SS", "android_version":13,"brand":"Redmi" },
#    "status":{ "is_locked":True, "is_awake":False },
#    "packages":{ "count":130, "list":["com.android.google.youtube", ... ] }
# }

adb_connector.start_logcat() # start android log
adb_connector.start_logcat(term="Flutter") # only return log containing Flutter string
# This can be useful for debug, for example creating a custom error and ther looking for it
```

#### <code>MANAGING APK</code>

```python
adb_connector.install_apk(path="path/to/apk")

adb_connector.uninstall_apk(
    package_name="com.android.google.youtube",
    device_id="2439vjsacs"
    )
```

#### <code>SCREEN ACTIONS</code>

```python
# swipe on the screen from points x100 y100 to x300 y300
adb_connector.swipe(
    x_from=100,y_from=100,
    y_to=300,y_to=300
)

# tap on screen at cordinates x100 y100
adb_connector.tap(x=100,y=100)

adb_connector.home() # return to device home
adb_connector.back() # go back 
adb_connector.foreground_apps() # background app check
```

#### <code>OPEN APPS</code>

```python
adb_connector.open_call_log()
adb_connector.open_calendar()
adb_connector.open_music()
adb_connector.open_calculator()
adb_connector.open_email()
adb_connector.open_browser()
adb_connector.open_camera()

# to see all supported app run
adb_connector.SUPPORTED_APPS
```

#### <code>USER ACTIONS</code>

```python
# phone call
adb_connector.call(phone_number="xxxxxxxx")

# send sms
adb_connector.send_sms(phone_number="xxxxxxxx",message="hello world")

# unlock screen
adb_connector.unlock_screen(password="12345")

# lock screen
adb_connector.power_button() 

# take screenshot
adb_connector.screenshot()

# input text 
adb_connector.insert_text("important data")

# take a picture with frontal camera zoomming 5 times
adb_connector.take_picture(frontal_camera=True, zoom_in=5)

# video capture with external camera for 10 seconds, zoomming 3 times 
adb_connector.video_capture(zoom_out=3, duration=10 )

# activate voice assistant (ok google)
adb_connector.voice_assistant()

# toggle notification center
adb_connector.notification_center()
```

#### <code>OTHER ACTIONS</code>

```python
# turn off device in 2 seconds
adb_connector.turn_off(countdown=2)

# reboot device in 10 seconds
adb_connector.reboot(countdown=10)

# raise / low volume
adb_connector.volume_up()
adb_connector.volume_down(times=7) # do it 7 times

# raise / low brightness
adb_connector.brightness_up(times=2) # do it 2 times
adb_connector.brightness_down()
```