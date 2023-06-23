import argparse
from pythonosc import udp_client
import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk

HOUR = 0
MINUTE = 0
TIMERON = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=9000, help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

# ボタンが押されたときの処理

def buttonON_click():
    client.send_message("/avatar/parameters/reactorState", 0)
    print("ON")

def buttonOFF_click():
    client.send_message("/avatar/parameters/reactorState", 1)
    print("OFF")

def buttonFlash_click():
    client.send_message("/avatar/parameters/reactorState", 2)
    print("Flash")

def buttonFlashFast_click():
    client.send_message("/avatar/parameters/reactorState", 3)
    print("Flash(Fast)")

def buttonActive_click():
    client.send_message("/avatar/parameters/reactorState", 0)
    client.send_message("/avatar/parameters/closeemi", 0.5)
    client.send_message("/avatar/parameters/allemi", 0.5)
    print("Active")

def buttonPassive_click():
    client.send_message("/avatar/parameters/reactorState", 1)
    client.send_message("/avatar/parameters/closeemi", 0.0)
    client.send_message("/avatar/parameters/allemi", 0.0)
    print("Passive")

def timer():
    global HOUR
    global MINUTE
    global TIMERON
    dt_set = datetime.datetime.now()
    dt_set = dt_set.replace(hour=HOUR, minute=MINUTE, second=0, microsecond=0)
    dt_now = datetime.datetime.now()
    dt_timedelta = 10
    print("モードは" + str(flashMode.get()) + "です")
    if(TIMERON == True):
        print("["+str(dt_now.hour) + ":" + str(dt_now.minute) + "]" + "タイマーはONです " + str(HOUR) + ":" + str(MINUTE) + "に消灯します")
        if(flashMode.get() == 1):
            dt_timedelta = 20
        elif(flashMode.get() == 2):
            dt_timedelta = 30
        else:
            dt_timedelta = 10
        # 点滅状態10分前
        dt_tmp = dt_set + datetime.timedelta(minutes=-dt_timedelta)
        print("10分前は" + str(dt_tmp.hour) + ":" + str(dt_tmp.minute))
        if dt_now.hour == dt_set.hour and dt_now.minute == dt_tmp.minute:
            client.send_message("/avatar/parameters/reactorState", 2)
            print("消灯10分前です")
        # はやい点滅状態5分前
        dt_tmp = dt_set + datetime.timedelta(minutes=-dt_timedelta/2)
        if dt_now.hour == dt_set.hour and dt_now.minute == dt_tmp.minute:
            client.send_message("/avatar/parameters/reactorState", 3)
            print("消灯5分前です")
        # 消灯
        if dt_now.hour == dt_set.hour and dt_now.minute == dt_set.minute:
            client.send_message("/avatar/parameters/reactorState", 1)
            client.send_message("/avatar/parameters/closeemi", 0.0)
            client.send_message("/avatar/parameters/allemi", 0.0)
            print("時間なので消灯します")
    else:
        
        print("[" + str(dt_now.hour) + ":" + str(dt_now.minute) + "]" + "タイマーはOFFです")
    baseGround.after(1000, timer)

def buttonSetTime_click():
    global HOUR
    global MINUTE
    global TIMERON
    if(TIMERON == False):
        if(entryHour.get().isnumeric() and int(entryHour.get()) <= 23 and int(entryHour.get()) >= 0):
            HOUR = int(entryHour.get())
            if(entryMinute.get().isnumeric() and int(entryMinute.get()) <= 59 and int(entryMinute.get()) >= 0):
                MINUTE = int(entryMinute.get())
                labelErrorTime.grid_forget()
                labelTimePassiveTimer.grid_forget()
                labelTimeActiveTimer.grid(row=11, column=0, columnspan=4,sticky=tk.W)
                TIMERON = True
            else:
                labelErrorTime.grid(row=11, column=0, columnspan=4,sticky=tk.W)
                labelTimeActiveTimer.grid_forget()
                labelTimePassiveTimer.grid_forget()
                TIMERON = False
        else:
            labelErrorTime.grid(row=11, column=0, columnspan=4,sticky=tk.W)
            labelTimeActiveTimer.grid_forget()
            labelTimePassiveTimer.grid_forget()
            TIMERON = False
    else:
        TIMERON = False
        labelTimeActiveTimer.grid_forget()
        labelTimePassiveTimer.grid(row=11, column=0, columnspan=4,sticky=tk.W)
    

# 画面の描画
baseGround = tk.Tk()
baseGround.geometry("305x230")
baseGround.resizable(width=False, height=False)
baseGround.title("ReactorControler")
flashMode = IntVar()
labelReactorState = ttk.Label(text='リアクター手動制御', foreground='black').grid(row=0, column=0, columnspan=4,sticky=tk.W)
buttonON = ttk.Button(
    baseGround, text = 'Active', command=buttonON_click).grid(row=1, column=0)
buttonOFF = ttk.Button(
    baseGround, text = 'Passive', command=buttonOFF_click).grid(row=1, column=1)
buttonFlash = ttk.Button(
    baseGround, text = 'Flash', command=buttonFlash_click).grid(row=1, column=2)
buttonFlashFast = ttk.Button(
    baseGround, text = 'Flash(Fast)', command=buttonFlashFast_click).grid(row=1, column=3)
labelAllState = ttk.Label(text='全身の状態', foreground='black').grid(row=2, column=0, columnspan=4,sticky=tk.W)
buttonActive = ttk.Button(
    baseGround, text = 'Active', command=buttonActive_click).grid(row=3, column=0)
buttonPassive = ttk.Button(
    baseGround, text = 'Passive', command=buttonPassive_click).grid(row=3, column=1)
labelSleepTime = ttk.Label(text='リアクターをPassiveにする時間', foreground='black').grid(row=5, column=0, columnspan=4,sticky=tk.W)
entryHour = tk.Entry(width=3)
entryHour.insert(0,str(HOUR))
entryHour.grid(row= 6, column=0)
labelTimeSeparator = ttk.Label(text=':', foreground='black').grid(row=6, column=1)
entryMinute = tk.Entry(width=3)
entryMinute.insert(0,str(MINUTE))
entryMinute.grid(row= 6, column=2)
buttonSet = ttk.Button(
    baseGround, text = 'Set!', command=buttonSetTime_click).grid(row=7, column=0)
radioTimeselect1 = ttk.Radiobutton(baseGround, text="10分前に点滅を開始する",
                        variable=flashMode,
                        value=0).grid(row=8, column=0, columnspan=4, sticky=tk.W)
radioTimeselect2 = ttk.Radiobutton(baseGround, text="20分前に点滅を開始する",
                        variable=flashMode,
                        value=1).grid(row=9, column=0, columnspan=4, sticky=tk.W)
radioTimeselect3 = ttk.Radiobutton(baseGround, text="30分前に点滅を開始する",
                        variable=flashMode,
                        value=2).grid(row=10, column=0, columnspan=4, sticky=tk.W)
flashMode.set(0)
labelErrorTime = ttk.Label(text='時間は0~23,分は0~59で入力してください', foreground='red')
labelTimeActiveTimer = ttk.Label(text='タイマーを有効化しました', foreground='black')
labelTimePassiveTimer = ttk.Label(text='タイマーを無効化しました', foreground='black')
baseGround.after(1000, timer)
baseGround.mainloop()
        