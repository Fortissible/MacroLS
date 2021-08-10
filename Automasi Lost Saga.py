import win32gui, win32api, win32con, ctypes
import re,os,time,autoit,random
from pynput.mouse import Button, Controller
from pynput import keyboard
import keyboard
from pynput.keyboard import Key, Listener

mouse = Controller()

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def get_hwnd(self):
        """returns hwnd for further use"""
        return self._handle

w = WindowMgr()
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def press_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008

    ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()

    flags = 0x0008 | 0x0002

    ii_.ki = KeyBdInput(0, key, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def get_game_window():
    w.find_window_wildcard("Lost Saga*")  # Game window is named 'Minecraft 1.13.1' for example.
    w.set_foreground()

state_right = win32api.GetKeyState(0x02)

# Character map
char_map = {
    'q': 0x10, 'w': 0x11, 'e': 0x12, 'r': 0x13, 't': 0x14, 'z': 0x15, 'u': 0x16, 'i': 0x17, 'o': 0x18, 'p': 0x19,
    'a': 0x1E, 's': 0x1F, 'd': 0x20, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
    'y': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30, 'n': 0x31, 'm': 0x32}

#-----------------------Sending the message using the character map-----------------------------
'''
keypress :
press_key(hexCode)
time.sleep(0.1)
release_key(hexCode)
'''
#------------------------------------Main Function----------------------------------------------
print("1. Makro Basic Training\n"
      "2. Makro ambil reward\n"
      "3. Makro Jual Gear\n----Klik Kanan Untuk Keluar Makro 2 & 3----")
makro=int(input("tipe makro: "))
if (makro==1):
    cnt_train=int(input("Jumlah Pengulangan: "))
elif (makro == 2):
    cnt_reward = int(input("Jumlah Pengulangan: "))
elif (makro == 3):
    cnt_gear = int(input("Jumlah Pengulangan: "))
get_game_window()
dir = "C:\Program Files (x86)\Lost Saga Origin\info\pp.log"
file=open(dir, "r")
chck = ""
cnt_jointr=0
cnt_fail =0
first=0
afktime=0
chk_retry=0
looping_dummy=5
cnt_clear=0
counter2=0

if (makro==1):
    time.sleep(1)
    autoit.mouse_move(95, 185,10)
    autoit.mouse_click("left", 95, 185, 1)
    time.sleep(0.1)
    autoit.mouse_click("left", 95, 185, 1)
    autoit.mouse_move(375, 255,10)
    autoit.mouse_click("left", 375, 255, 1)
    autoit.mouse_move(690, 535,10)
    autoit.mouse_click("left", 690, 535, 1)

    while(cnt_train):
        lineList = file.readlines()
        if (afktime>400000):
            lineList = ["12:07.33 lv0 ModeType : 24 - Mode State Change: 1\n","\n"]
        if (len(lineList)>1):
            #print(lineList[-2][13:49], end='')
            print(lineList[-2],end='')
            chck = lineList[-2][13:]
            print(chck)
            #arr = bytes(chck, 'utf-8')
            #print (arr)
            if (chck == "ModeType : 24 - Mode State Change: 1\n" and first!=0):
                print ("ini lobby!")
                afktime=0
                cnt_jointr=0
                cnt_clear=0
                time.sleep(2)
                # buatskip afk lobby
                autoit.mouse_click("left", 95, 185, 1)
                autoit.mouse_click("left", 95, 185, 1)
                while(looping_dummy):
                    x = random.randint(10, 780)
                    y = random.randint(50, 550)
                    z = random.randint(3,10)
                    autoit.mouse_move(x, y, z)
                    looping_dummy-=1
                autoit.mouse_click("left", 418, 148, 1)
                autoit.mouse_click("left", 690, 535, 1)
            if (chck == "ModeType : 29 - Mode State Change: 1\n"):
                afktime=0
                cnt_jointr+=1
                if (cnt_jointr >= 1):
                    time.sleep(4)
                    first=1
                    print ("masuk mode training")
                    print("sisa pengulangan: "+str(cnt_train)+" Gagal Sebanyak: "+str(cnt_fail))
                    time.sleep(4.5)
                    press_key(0x4D)
                    time.sleep(0.1)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(2.9)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x48)
                    time.sleep(0.1)
                    release_key(0x48)
                    time.sleep(0.01)
                    press_key(0x48)
                    time.sleep(1.5)
                    release_key(0x48)
                    time.sleep(0.01)
                    press_key(0x1E)
                    time.sleep(0.1)
                    release_key(0x1E)
                    press_key(0x48)
                    time.sleep(0.8)
                    release_key(0x48)
                    press_key(0x49)
                    time.sleep(0.1)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x49)
                    time.sleep(0.4)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(0.1)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(1.8)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x1E)
                    time.sleep(0.1)
                    release_key(0x1E)
                    press_key(0x4d)
                    time.sleep(0.6)
                    release_key(0x4d)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(0.1)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(0.8)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x51)
                    time.sleep(0.1)
                    release_key(0x51)
                    time.sleep(0.01)
                    press_key(0x51)
                    time.sleep(2.6)
                    release_key(0x51)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(0.1)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x4D)
                    time.sleep(1.3)
                    release_key(0x4D)
                    time.sleep(0.01)
                    press_key(0x49)
                    time.sleep(0.1)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x49)
                    time.sleep(2.8)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x1E)
                    time.sleep(0.1)
                    release_key(0x1E)
                    time.sleep(0.01)
                    press_key(0x49)
                    time.sleep(0.6)
                    release_key(0x49)
                    time.sleep(0.05)
                    press_key(0x49)
                    time.sleep(0.1)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x49)
                    time.sleep(0.2)
                    release_key(0x49)
                    time.sleep(0.01)
                    press_key(0x48)
                    time.sleep(0.1)
                    release_key(0x48)
                    time.sleep(0.01)
                    press_key(0x48)
                    time.sleep(0.5)
                    release_key(0x48)
                    time.sleep(0.01)
                    press_key(0x47)
                    time.sleep(0.1)
                    release_key(0x47)
                    time.sleep(0.01)
                    press_key(0x47)
                    time.sleep(2.9)
                    release_key(0x47)
                    time.sleep(0.01)
                    press_key(0x1E)
                    time.sleep(0.1)
                    release_key(0x1E)
                    time.sleep(0.01)
                    press_key(0x47)
                    time.sleep(0.7)
                    release_key(0x47)
                    time.sleep(0.01)
                    press_key(0x47)
                    time.sleep(0.1)
                    release_key(0x47)
                    time.sleep(0.01)
                    press_key(0x47)
                    time.sleep(1)
                    release_key(0x47)
                    if (cnt_clear==0):
                        time.sleep(0.2)
                        press_key(0x39)
                        time.sleep(0.1)
                        release_key(0x39)
                        cnt_jointr = 0
                        cnt_clear += 1
                        cnt_train-=1
                    elif (cnt_clear==1):
                        time.sleep(0.2)
                        press_key(0x39)
                        time.sleep(0.1)
                        release_key(0x39)
                        time.sleep(0.3)
                        press_key(0x0A)
                        time.sleep(0.1)
                        release_key(0x0A)
                        time.sleep(0.1)
                        press_key(0x0A)
                        time.sleep(0.1)
                        release_key(0x0A)
                        time.sleep(0.1)
                        press_key(0x1c)
                        time.sleep(0.1)
                        release_key(0x1c)
                        cnt_jointr = 0
                        looping_dummy = 5
                        cnt_train -= 1
            if (lineList[-2][13:24]=="PENGUIN_LOG" and len(lineList)!=0):
                afktime=0
                chk_retry+=1
                if (chk_retry>1):
                    time.sleep(1)
                    autoit.mouse_click("left", 715, 557, 1)
                    autoit.mouse_click("left", 715, 557, 1)
                    chk_retry =0
                    cnt_jointr=0
                    cnt_clear-=1
                    if (cnt_clear<0):
                        cnt_clear=0
                    cnt_train-=1
                    cnt_fail+=1
        else:
            print(afktime)
            afktime+=1

elif (makro==2):
    time.sleep(1)
    press_key(0x3E);
    time.sleep(0.1);
    release_key(0x3E)
    while(cnt_reward):
        print("Sisa Pengulangan: "+str(cnt_reward))
        autoit.mouse_click("left", 110, 336, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 212, 335, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 315, 338, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 426, 338, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 107, 521, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 210, 516, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 319, 519, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        autoit.mouse_click("left", 424, 517, 1)
        press_key(0x39)
        time.sleep(0.1)
        release_key(0x39)
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else:
                break
        cnt_reward-=1

elif (makro==3):
    time.sleep(1)
    press_key(0x3D);
    time.sleep(0.1);
    release_key(0x3D)
    autoit.mouse_click("left", 136, 128, 2)
    while (cnt_gear):
        b = win32api.GetKeyState(0x02)
        if b != state_right:
            state_right = b
            print(b)
            if b < 0:
                break
            else :
                break
        print("Sisa Pengulangan:"+str(cnt_gear))
        autoit.mouse_click("left", 131, 336, 2)
        '''
        time.sleep(0.1)
        press_key(0x2A)
        press_key(0x24)
        release_key(0x24)
        release_key(0x2A)

        press_key(0x16)
        release_key(0x16)

        press_key(0x1E)
        release_key(0x1E)

        press_key(0x26)
        release_key(0x26)

        press_key(0x39)
        release_key(0x39)

        press_key(0x2A)
        time.sleep(0.1)
        press_key(0x25)
        time.sleep(0.1)
        release_key(0x25)
        release_key(0x2A)

        press_key(0x18)
        time.sleep(0.1)
        release_key(0x18)

        press_key(0x1F)
        time.sleep(0.1)
        release_key(0x1F)

        press_key(0x14)
        time.sleep(0.1)
        release_key(0x14)

        press_key(0x16)
        time.sleep(0.1)
        release_key(0x16)

        press_key(0x32)
        time.sleep(0.1)
        release_key(0x32)
        '''
        autoit.mouse_click("left", 346, 440, 1)
        cnt_gear-=1

# print('The current pointer position is {0}'.format(mouse.position))

#from pynput.mouse import Button, Controller
#mouse = Controller()

# fungsi manggil window >>>         get_game_window()
#------------------------------------makro gerakan mouse---------------------------------------------
'''
get_game_window()
time.sleep(1)
while(1):
    autoit.mouse_click("left", 95, 185, 1)
    time.sleep(0.5)
    autoit.mouse_click("left", 375, 255, 1)
    time.sleep(0.5)
    autoit.mouse_click("left", 690, 535, 1)
    time.sleep(0.5)
'''

#------------------------------makro keyboard training basic att-------------------------------
'''
MACRO TRAINING BASIC MOVE
time.sleep(0.2)
#press_key(0x1C)
#release_key(0x1C)
#time.sleep(1)]
press_key(0x4D);time.sleep(0.1);release_key(0x4D)
time.sleep(0.01)
press_key(0x4D);time.sleep(3);release_key(0x4D)
time.sleep(0.01)
press_key(0x48);time.sleep(0.1);release_key(0x48)
time.sleep(0.01)
press_key(0x48);time.sleep(1.5);release_key(0x48)
time.sleep(0.01)
press_key(0x1E);time.sleep(0.1);release_key(0x1E)
press_key(0x48);time.sleep(0.8);release_key(0x48)
press_key(0x49);time.sleep(0.1);release_key(0x49)
time.sleep(0.01)
press_key(0x49);time.sleep(0.4);release_key(0x49)
time.sleep(0.01)
press_key(0x4D);time.sleep(0.1);release_key(0x4D)
time.sleep(0.01)
press_key(0x4D);time.sleep(1.7);release_key(0x4D)
time.sleep(0.01)
press_key(0x1E);time.sleep(0.1);release_key(0x1E)
press_key(0x4d);time.sleep(0.6);release_key(0x4d)
time.sleep(0.01)
press_key(0x4D);time.sleep(0.1);release_key(0x4D)
time.sleep(0.01)
press_key(0x4D);time.sleep(0.8);release_key(0x4D)
time.sleep(0.01)
press_key(0x51);time.sleep(0.1);release_key(0x51)
time.sleep(0.01)
press_key(0x51);time.sleep(2.6);release_key(0x51)
time.sleep(0.01)
press_key(0x4D);time.sleep(0.1);release_key(0x4D)
time.sleep(0.01)
press_key(0x4D);time.sleep(1.3);release_key(0x4D)
time.sleep(0.01)
press_key(0x49);time.sleep(0.1);release_key(0x49)
time.sleep(0.01)
press_key(0x49);time.sleep(2.5);release_key(0x49)
time.sleep(0.01)
press_key(0x1E);time.sleep(0.1);release_key(0x1E)
time.sleep(0.01)
press_key(0x49);time.sleep(0.6);release_key(0x49)
time.sleep(0.05)
press_key(0x49);time.sleep(0.1);release_key(0x49)
time.sleep(0.01)
press_key(0x49);time.sleep(0.4);release_key(0x49)
time.sleep(0.01)
press_key(0x48);time.sleep(0.1);release_key(0x48)
time.sleep(0.01)
press_key(0x48);time.sleep(0.5);release_key(0x48)
time.sleep(0.01)
press_key(0x47);time.sleep(0.1);release_key(0x47)
time.sleep(0.01)
press_key(0x47);time.sleep(2.9);release_key(0x47)
time.sleep(0.01)
press_key(0x1E);time.sleep(0.1);release_key(0x1E)
time.sleep(0.01)
press_key(0x47);time.sleep(0.7);release_key(0x47)
time.sleep(0.01)
press_key(0x47);time.sleep(0.1);release_key(0x47)
time.sleep(0.01)
press_key(0x47);time.sleep(1);release_key(0x47)
#time.sleep(1)
#press_key(0x1C)
#release_key(0x1C)
'''