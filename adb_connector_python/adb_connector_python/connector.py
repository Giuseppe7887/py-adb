from subprocess import check_output, CalledProcessError
from os import system
from sys import platform
from time import sleep
from termcolor import colored


# INPUTS
BASIC_INPUT_KEYEVENT: str = "adb -s {0} shell input keyevent {1}"
COMMAND_INFO_SCREEN: str = "adb -s {0} shell dumpsys window"
COMMAND_INFO_BATTERY: str = "adb -s {0} shell dumpsys battery"
COMMAND_INFO_DEVICE: str = "adb -s {0} shell getprop"
COMMAND_LIST_PACKAGES: str = "adb -s {0} shell pm list packages"
COMMAND_INSTALL_APK: str = "adb -s {0} install {1}"
COMMAND_UNINSTALL_APK: str = "adb -s {0} uninstall -k --user 0 {1}"
COMMAND_LOGCAT: str = "adb -s {0} logcat"
COMMAND_INSERT_TEXT: str = "adb -s {0} shell input text {1}"
COMMAND_TURN_OFF: str = "adb -s {0} shell reboot -p"
COMMAND_REBOOT: str = "adb -s {0} shell reboot"

# GESTURES
COMMAND_SWIPE: str = "adb -s {0} shell input swipe {1} {2} {3} {4}"
COMMAND_TAP: str = "adb -s {0} shell input tap {1} {2}"


# INTENTS
INTENT_TAKE_PICTURE_INTENT:str ="adb -s {0} shell am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING {1}"
INTENT_VIDEO_CAPTURE_INTENT:str ="adb -s {0} shell am start -a android.media.action.VIDEO_CAPTURE --ei android.intent.extras.CAMERA_FACING {1}"
INTENT_CALLTO: str = "adb -s {0} shell am start -a android.intent.action.CALL -d tel:'{1}'"
INTENT_SENDTO: str = "adb -s {0} shell am start -a android.intent.action.SENDTO -d sms:'{1}' --es sms_body '{2}'"


# queries
query_product_brand: str = "[ro.product.brand]:"
query_product_model: str = "[ro.product.model]:"
query_product_version: str = "[ro.build.version.release]:"

# KEYEVENTS
KEYEVENT_SCREENSHOT: int = 120
KEYEVENT_POWER_BUTTON: int = 26
KEYEVENT_TAB: int = 61
KEYEVENT_RETURN: int = 66
KEYEVENT_ZOOM_IN:int = 168
KEYEVENT_ZOOM_OUT:int = 169
KEYEVENT_VOLUME_UP:int = 24
KEYEVENT_VOLUME_DOWN:int = 25
KEYEVENT_BRIGHTNESS_UP:int = 221
KEYEVENT_BRIGHTNESS_DOWN:int = 220

# APP KEYEVENTS
KEYEVENT_CALL_LOG:int =  207
KEYEVENT_CALENDAR:int =208
KEYEVENT_MUSIC:int = 209
KEYEVENT_CALCULATOR:int = 210
KEYEVENT_EMAIL:int = 65
KEYEVENT_BROWSER:int = 84
KEYEVENT_CAMERA:int = 259


# NAVIGATION KEYEVENTS
KEYEVENT_HOME:int = 3
KEYEVENT_BACK:int = 4
KEYEVENT_FOREGROUND:int = 82
KEYEVENT_NOTIFICATION_CENTER:int=83
KEYEVENT_VOICE_ASSISTANT:int =118


# adb command
CMD_START_ADB: str = "adb start-server"
CMD_KILL_ADB: str = "adb kill-server"
CMD_LIST_DEVICES: str = "adb devices"



def IS_ADB_RUNNING_CMD() -> str:
    match platform:
        case "win32":
            return "tasklist | findstr adb"
        case "linux" | "darwin":
            return "ps aux | grep adb"
        case _:
            raise RuntimeError("os not supported")


def execute(CMD:str):
    return check_output(CMD, shell=True).decode("utf8")

def execute_keyevent(CMD_KEYEVENT:str)->bool:
    return check_output(CMD_KEYEVENT, shell=True).decode("utf8") == ""

def execute_intent(CMD_INTENT:str) ->bool:
    res = check_output(CMD_INTENT, shell=True).decode("utf8")
    
    if "Starting: Intent" in  res:
        return True 
    else:
        return False
    

def clear_cmd():
    match platform:
        case "win32":
            system("cls")
        case "linux" | "darwin":
            system("clear")


class Py_adb:
    """
this is a simple low level ADB connector, you can use it for every task, such as
debugging, automatism and even fun!
a list of avaiable function and methods with description

    * ADB_DATA : get some adb data such as version and main ADB executable path
    * ADB_VERSION : return only the version of ADB
    * ADB_EXECUTABLE : only return main executable ADB path
    * is_adb_running : to check if adb is actualy running
    * list_devices : to check all avaiable devices
    * display_status : check if display is awake or locked
    * get_first_avaiable_device : to get a a dict of first avaiable device
    * phone_data : a rich dict with some of the most important phone data
    * install_apk : try to insrall install apk on device
    * uninstall_apk : try to unistall apk by its package name
    * start_logcat : very interesting feature for debugging app, current device log
    * screenshot : to take a screenshot
    * power_button : to lock or unlock the screen
    * call : to start a call
    * send_sms : to send a sms to someone
    * insert_text : to input some text
    * unlock_screen : to try to unlock the screen, you may provide a password if needed
    * take_picture : take a photo, you can even provide the zoom_in<int> and zoom_out<int>
    * video_capture start a video capture, you can even provide the zoom_in<int> and zoom_out<int> and duration<int> to define video duration
    * swipe : to swipe on the screen 
    * tap : to tap on the screen giving x and y
    * turn_off : turn off the device
    * reboot : reboot device
    * open_call_log : open the system default call-log app
    * open_calendar : open the system default calendar app
    * open_calulator : open the system default calculator app
    * open_email : open the system default email
    * open_browser : open the system default browser
    * open_camera : open the system default camera, specify 'frontal_camera=True' to use frontal camera
    * home : go to the device home screen
    * back : go back in the previous screen
    * foreground_apps : toggle the app in background
    * notification_center : toggle the notification center
    * voice_assistant : toggle voice assistant, like saying 'ok google'
    * volume_up / volume_down : to raise or low the volume, provide 'times' to define how many times repeat the action
    * brightness_up / brightness_down : to raise or low brightness, provide 'times' to define how many times repeat the action
    """

    def __init__(self) -> None:
        # if adb shell is not running, raise a RuntimeError exception
        if not self.is_adb_running():
            raise RuntimeError(
                "ADB is not running, please start it with 'adb start-server'")

        self.ADB_DATA = execute("adb --version")
        self.ADB_VERSION = self.ADB_DATA.split()[4]
        self.ADB_EXECUTABLE = self.ADB_DATA.split()[9]
        self.SUPPORTED_APPS = {
            "call_log":KEYEVENT_CALL_LOG,
            "calendar":KEYEVENT_CALENDAR,
            "music":KEYEVENT_MUSIC,
            "calculator":KEYEVENT_CALCULATOR,
            "email":KEYEVENT_EMAIL,
            "browser":KEYEVENT_BROWSER,
            "camera":KEYEVENT_CAMERA
        }
        self.SUPPORTED_NAVIGATION_ACTIONS = {
            "home":KEYEVENT_HOME,
            "back":KEYEVENT_BACK,
            "foreground":KEYEVENT_FOREGROUND,
            "notification_center":KEYEVENT_NOTIFICATION_CENTER
        }

    # ADB FUNCTIONS

    def is_adb_running(self) -> bool:
        """
this function return boolean value True if adb is runnig else it raises
a RuntimeError exception, to solve this issue just run in CMD 'adb start-server'
        """
        try:
            return execute_keyevent(IS_ADB_RUNNING_CMD()) != ""
        except CalledProcessError:
            return False

    def list_devices(self) -> list:
        """
this function return a list containing a dict with name and status of each devices
        """
        devices: list = []
        match platform:
            case "win32":
                res: list = execute(CMD_LIST_DEVICES).split()
                tmp: str = res[res.index("attached") + 1:]
                i: int = 0
                while i < len(tmp):
                    devices.append({"id": tmp[i], "status": tmp[i+1]})
                    i += 2
            case "linux" | "darwin":
                res: list = execute(CMD_LIST_DEVICES).split("\n")[1:]

                clean: list = [x for x in res if x]
                for el in clean:
                    s: list = el.split("\t")
                    devices.append({"id": s[0], "status": s[1]})
        return devices

    def get_first_avaiable_device(self) -> dict:
        """
this function just returns a dict of first device avaiable
        """
        # use this on every function to check if there is a device else raise exception
        d: list = self.list_devices()
        if len(d):
            return d[0]
        else:
            return {}
     
    def _basic_device_check(self,device_id:str="") ->None:
        """
this is an internal function just to check if some devices are unauthorized, this may cause fatal errors
        """
        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        
        if "unauthorized" in execute("adb devices"):
            print(colored(" > ERROR - some of your devices are tagged with 'unauthorized' status, this may cause problems, please get developer mode in android settings","red"))

    # PHONE DATA

    def display_status(self, device_id: str = None) -> dict:
        """
this function can be called to check if display is awake and unlocked
        """
        
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()['id']

            screen_data: str = execute(COMMAND_INFO_SCREEN.format(device_id))

            return {
                "is_locked": "mDreamingLockscreen=true" in screen_data,
                "is_awake": "screenState=SCREEN_STATE_ON" in screen_data,
            }

    def phone_data(self, device_id=None) -> dict:
        """
this function return the most part of phone data that you could need,
the parameterdevice_id is optionally, it will take as default the first device avaiable
if you want to use another device just call
the 'get_first_avaiable_device[\'id'] function and use theDEVICE_ID to refer to device'
        """

        # riase exception if there is no device
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            # if not providedDEVICE_ID take thedevice_id of the first avaiable
            if not device_id:
                device_id = self.get_first_avaiable_device()['id']

            screen_data: str = execute_keyevent(
                COMMAND_INFO_SCREEN.format(device_id))
            battery_data: list = execute_keyevent(
                COMMAND_INFO_BATTERY.format(device_id)).split()
            general_data: list = execute_keyevent(
                COMMAND_INFO_DEVICE.format(device_id)).split()
            package_list_tmp: list = execute_keyevent(
                COMMAND_LIST_PACKAGES.format(device_id)).split("\n")

            package_list: list = []
            i = 0
            while i < len(package_list_tmp):
                if package_list_tmp[i]:
                    package_list.append(package_list_tmp[i].removesuffix("\r"))
                i += 1

            model: str = general_data[general_data.index(
                query_product_model) + 1]
            version: str = general_data[general_data.index(
                query_product_version) + 1]
            brand: str = general_data[general_data.index(
                query_product_brand) + 1]

            device_data_object = {
                "model": model.removeprefix("[").removesuffix("]"),
                "android_version": f"{version.removeprefix('[').removesuffix(']')}",
                "brand": brand.removeprefix("[").removesuffix("]")
            }

            battery_object: dict = {
                "level": battery_data[battery_data.index("level:") + 1],
                "is_charging": battery_data[battery_data.index("USB")] == "true"
            }

            phone_status_object: dict = {
                "is_locked": "mDreamingLockscreen=true" in screen_data,
                "is_awake": "screenState=SCREEN_STATE_ON" in screen_data,
            }

            return {
                "battery_data": battery_object,
                "device_data": device_data_object,
                "status": phone_status_object,
                "packages": {
                    "list": package_list,
                    "count": len(package_list)
                }
            }

    # FUNCTIONS

    def install_apk(self, path: str, device_id: str = None) -> bool:
        """
this function try to install apk it needs a path to apk
and optionalyDEVICE_ID, if notDEVICE_ID is provided it will take the first device as default,
you have to allow the operation from the device
        """

        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            # path check
            real_path: str = path.realpath(path)
            if not path.exists(real_path):
                raise RuntimeError(f"no such apk file: '{real_path}'")

            if not device_id:
                device_id = self.get_first_avaiable_device()['id']

            print(" > request sent to device")
            return execute_keyevent(COMMAND_INSTALL_APK.format(device_id, path))

    def uninstall_apk(self, package_name: str, device_id=None) -> bool:
        """
this function try to uninstall a package by its name, you have to pass into attribute 'path'
a package name like 'com.package.app' in order to uninstall it, to get a list of
packages present on this device run 'phone_data()['packages']'
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()['id']

            system(COMMAND_UNINSTALL_APK.format(
                device_id, package_name.removeprefix("package:")))
            return True

    def start_logcat(self, term: str = None, device_id: str = None):
        """
this function is useful if you need to debug your app in production, you can
see the entire log of your phone, it may look very messy, so you can pass
in the attribute 'term' a word that you want to find inside the log,
so you can create a custom error and isolate it
        """

        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if notdevice_id:
                device_id = self.get_first_avaiable_device()['id']

            if term:
                system(COMMAND_LOGCAT.format(device_id) + f" --regex={term}")
            else:
                system(COMMAND_LOGCAT.format(device_id))

    # ACTIONS

    def screenshot(self, device_id: str = None) -> bool:
        """
this command take a screenshot, it will not awake the screen,
to do it, use the 'power_button' function
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            return execute_keyevent(BASIC_INPUT_KEYEVENT.format(
                device_id, KEYEVENT_SCREENSHOT))

    def power_button(self, device_id: str = None) -> bool:
        """
this command simulate the pressing of power button
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            return execute_keyevent(BASIC_INPUT_KEYEVENT.format(
                device_id, KEYEVENT_POWER_BUTTON))

    def call(self, phone_number: str, device_id: str = None) -> bool:
        """
this function start a call even if the device is locked
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id: str = self.get_first_avaiable_device()["id"]
            return execute_intent(INTENT_CALLTO.format(device_id, phone_number))


    def send_sms(self, phone_number: str, message: str, device_id: str = None) -> bool:
        """
this function send a sms, but the phone need to be locked
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            execute_intent(INTENT_SENDTO.format(device_id, phone_number, message))

            status: str = self.display_status(device_id)
            if status["is_locked"] or not status["is_awake"]:
                print(colored(" > ERROR : the phone need to be unlocked","red"))
                return False
            else:
                for i in range(3):
                    execute_keyevent(BASIC_INPUT_KEYEVENT.format(
                        device_id, KEYEVENT_TAB))
                return True

    def insert_text(self, text: str, device_id: str = None) -> bool:
        """
this function input a text only if the device is locked
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id: str = self.get_first_avaiable_device()["id"]
            return execute(COMMAND_INSERT_TEXT.format(device_id, text))


    def unlock_screen(self, password: str = None, device_id: str = None) -> bool:
        """
this function try to unlock the screen, you may provide a password if needed
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id: str = self.get_first_avaiable_device()["id"]

            status: dict = self.display_status()

            # if already locked return True
            if not status["is_locked"]:
                return True
            else:
                # if is in sleep press power button and swipe
                if not status["is_awake"]:
                    execute_keyevent(BASIC_INPUT_KEYEVENT.format(
                        device_id, KEYEVENT_POWER_BUTTON))
                    sleep(0.5)

                self.swipe(from_x=200, from_y=500, to_x=200, to_y=0)
                sleep(0.5)

                # if password write it

                if password:
                    self.insert_text(password)

                sleep(0.5)

                # check if unlocked

                if self.display_status()["is_locked"]:
                    return False
                else:
                    return True

    def take_picture(self,frontal_camera:bool=False,zoom_in:int=0,zoom_out:int=0,device_id:str="")->bool:
        """
this function just take photo, serveral arguments ca be provided such as:
        * frontal_camera : <bool> if True open the frontal camera
        * zoom_in : <int> if specified it zoom in the camera 'n' times
        * zoom_in : <int> if specified it zoom out the camera 'n' times
        """
        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        
            

        if self.open_camera(device_id=device_id,camera_type=1,frontal_camera=1 if frontal_camera else 0):
            # zoom in events
            for el in range(zoom_in):
                sleep(0.5)
                execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id, KEYEVENT_ZOOM_IN))
            # zoom out events
            for el in range(zoom_out):
                sleep(0.5)
                execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id, KEYEVENT_ZOOM_OUT))

            sleep(1)
            execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_RETURN))
            sleep(1)
            return execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_RETURN))
        else:
            return False


    def video_capture(self,frontal_camera:bool=False,zoom_in:int=0,zoom_out:int=0,duration:int=0,device_id:str=""):
        """
call this function if you want to capture video, you can provide some data like:
        * frontal_camera : <bool> if True open the frontal camera
        * zoom_in : <int> if specified it zoom in the camera 'n' times
        * zoom_in : <int> if specified it zoom out the camera 'n' times
        * duration : <int> in seconds of the duration of the video
        """
        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]

        if self.open_camera(device_id=device_id,camera_type=2,frontal_camera=1 if frontal_camera else 0):
              # zoom in events
            for el in range(zoom_in):
                sleep(0.5)
                execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id, KEYEVENT_ZOOM_IN))
            # zoom out events
            for el in range(zoom_out):
                sleep(0.5)
                execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id, KEYEVENT_ZOOM_OUT))

            sleep(1)
            execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_RETURN))
            sleep(1)
            execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_RETURN))
            if duration:
                i = 0 
                while i < duration:
                    print(f"video will be stopped in {duration -i}")
                    i+=1
                    sleep(1)
                    clear_cmd()


            return execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_RETURN))
        else:
            return False


        
    # GESTURES

    def swipe(self, from_x: int, from_y: int, to_x: int, to_y: int, device_id: str = None) -> bool:
        """
this function simulate a swipe on the screen, the device has to be awake,
you need to pass:
    * from_x : the x starting point on the screen
    * from_y : the y starting point on the screen
    * to_x : the x ending point on the screen
    * to_y : the y ending point on the screen
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if self.display_status():
                if not device_id:
                    device_id: str = self.get_first_avaiable_device()["id"]
                return execute_keyevent(COMMAND_SWIPE.format(
                    device_id, from_x, from_y, to_x, to_y))
            else:
                print(colored(" > ERROR : phone need to be awake","red"))
                return False

    def tap(self, x: int, y: int, device_id: str = None) -> bool:
        """
You can use this function to tap on the screen giving x and y
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            return execute_keyevent(COMMAND_TAP.format(device_id, x, y))

    # POWER

    def turn_off(self, countdown: int = 0, see_countdown: bool = True, device_id: str = None) -> bool:
        """
just turn off the phone, you can provide 'countdown' as timer for shutdown
        """

        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:

            self._basic_device_check()

            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            if countdown:
                i = 1
                while i <= countdown:

                    clear_cmd()
                    if see_countdown:
                        if countdown - i == 0:
                            print(f" > SHUTDOWN ")
                        else:
                            print(f" > SHUTDOWN IN {countdown - i}")
                    sleep(1)
                    i += 1

            return execute_keyevent(COMMAND_TURN_OFF.format(device_id))

    def reboot(self, countdown: int = 0, see_countdown: bool = True, device_id: str = None) -> bool:
        """
reboot the phone, you can provide 'countdown' as timer for shutdown
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            if countdown:
                i = 1
                while i <= countdown:
                    clear_cmd()
                    if see_countdown:
                        if countdown - i == 0:
                            print(f" > REBOOT ")
                        else:
                            print(f" > REBOOT IN {countdown - i}")
                    sleep(1)
                    i += 1

            res =execute(COMMAND_REBOOT.format(device_id))
            if res:
                print(res)
                return False
            else:
                return True

    def open_app(self,app_name:str, device_id:str="",)->bool:
        """
open system app, you have to provide app_name, to see all supported app, call SUPPORTED_APPS.keys(),
actually are included : 'call_log', 'calendar', 'music', 'calculator', 'email', 'browser', 'camera',
you can use specific function like open_calendar, open_music, ecc..
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            
            if self.display_status(device_id)["is_locked"]:
                raise RuntimeError("the device need to be unlocked")
            else:
                if not app_name.lower() in self.SUPPORTED_APPS:
                    print(f"app not supported yet choose one of these {list(self.SUPPORTED_APPS.keys())}")
                    return False
                else:
                    return execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,self.SUPPORTED_APPS[app_name]))

    # OPEN APPS
    def open_call_log(self,device_id:str="")->bool: return self.open_app(app_name="call_log")

    def open_calendar(self,device_id:str="")->bool: return self.open_app(app_name="calendar")
        
    def open_music(self,device_id:str="")->bool: return self.open_app(app_name="music")
    
    def open_calculator(self,device_id:str="")->bool: return self.open_app(app_name="calculator")

    def open_email(self,device_id:str="")->bool: return self.open_app(app_name="email")

    def open_browser(self,device_id:str="")->bool: return self.open_app(app_name="browser")

    def open_camera(self,frontal_camera:bool=False,camera_type:int=1,device_id:str="")->bool: 
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            if camera_type == 1:
                return execute_intent(INTENT_TAKE_PICTURE_INTENT.format(device_id,1 if frontal_camera else 0)) 
            elif camera_type == 2:
                return execute_intent(INTENT_VIDEO_CAPTURE_INTENT.format(device_id,1 if frontal_camera else 0)) 
            else:
                print(colored(f" > ERROR camera time {camera_type} not supported, try 1 for photo and 2 for video","red"))
                return False

    # navigation

    def navigate(self,action:str,device_id:str=""):
        """
use this function to move through the device, pass the 'action' parameter('home','back','foreground'),
you can also use specific function like home(), back() or foreground()
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            if not self.display_status(device_id)["is_awake"]:
                print("device need to be awake to execute naviagtion command")
                return False
            else:
                if not action.lower() in self.SUPPORTED_NAVIGATION_ACTIONS:
                    raise RuntimeError(f"navigation action not supported yet, please choose between these: {list(self.SUPPORTED_NAVIGATION_ACTIONS.keys())}")
                else:
                    return execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,self.SUPPORTED_NAVIGATION_ACTIONS[action]))
                        
    
    def home(self,device_id:str="") ->bool:
        """
simulate home gesture
        """

        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        return self.navigate("home",device_id)

    
    def back(self,device_id:str="")->bool:
        """
simulate back gesture
        """

        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        return self.navigate("back",device_id)

    def foreground_apps(self,device_id:str="") ->bool:
        """
simulate home background app gesture
        """

        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        return self.navigate("foreground",device_id)

    def notification_center(self,device_id:str="") ->bool:
        """
toggle notification center
        """

        if not device_id:
            device_id = self.get_first_avaiable_device()["id"]
        return self.navigate("notification_center",device_id)

    def voice_assistant(self,device_id:str="") ->bool:
        """
open the voice assitent, the same as saying 'ok google'
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]
            return execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_VOICE_ASSISTANT))

    def volume_up(self,times:int=1,device_id:str="") ->bool:
        """
this function simply raises the volume, you can pass the 'times' argument to
specify how many times raise the volume
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            res = False
            for n in range(times):
                if execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_VOLUME_UP)):
                    res = True
            return res


    def volume_down(self,times:int=1,device_id:str="") ->bool:
        """
this function simply lowes the volume, you can pass the 'times' argument to
specify how many times low the volume
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            res = False
            for n in range(times):
                if execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_VOLUME_DOWN)):
                    res = True
            return res

    def brightness_up(self,times:int=1,device_id:str="") ->bool:
        """
this function simply raises the brightness, you can pass the 'times' argument to
specify how many times raise the brightness
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            res = False
            for n in range(times):
                if execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_BRIGHTNESS_UP)):
                    res = True
            return res

    def brightness_down(self,times:int=1,device_id:str="") ->bool:
        """
this function simply lowes the brightness, you can pass the 'times' argument to
specify how many times low the brightness
        """
        if not self.get_first_avaiable_device():
            raise RuntimeError("no device detected")
        else:
            self._basic_device_check()
            if not device_id:
                device_id = self.get_first_avaiable_device()["id"]

            res = False
            for n in range(times):
                if execute_keyevent(BASIC_INPUT_KEYEVENT.format(device_id,KEYEVENT_BRIGHTNESS_DOWN)):
                    res = True
            return res