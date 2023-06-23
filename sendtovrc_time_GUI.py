import argparse
from pythonosc import udp_client
import datetime
import tkinter as tk
from tkinter import ttk

hour = 0
minute = 0
timerON = False

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
    global hour
    global minute
    global timerON
    dt_set = datetime.datetime.now()
    dt_set = dt_set.replace(hour=hour, minute=minute, second=0, microsecond=0)
    dt_now = datetime.datetime.now()
    if(timerON == True):
        print("["+str(dt_now.hour) + ":" + str(dt_now.minute) + "]" + "タイマーはONです " + str(hour) + ":" + str(minute) + "に消灯します")
        # 点滅状態10分前
        dt_tmp = dt_set + datetime.timedelta(minutes=-10)
        if dt_now.hour == dt_set.hour and dt_now.minute == dt_tmp.minute:
            client.send_message("/avatar/parameters/reactorState", 2)
            print("消灯10分前です")
        # はやい点滅状態5分前
        dt_tmp = dt_set + datetime.timedelta(minutes=-5)
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
    global hour
    global minute
    global timerON
    if(timerON == False):
        if(entryHour.get().isnumeric() and int(entryHour.get()) <= 23 and int(entryHour.get()) >= 0):
            hour = int(entryHour.get())
            if(entryMinute.get().isnumeric() and int(entryMinute.get()) <= 59 and int(entryMinute.get()) >= 0):
                minute = int(entryMinute.get())
                labelErrorTime.grid_forget()
                labelTimePassiveTimer.grid_forget()
                labelTimeActiveTimer.grid(row=8, column=0, columnspan=4,sticky=tk.W)
                timerON = True
            else:
                labelErrorTime.grid(row=8, column=0, columnspan=4,sticky=tk.W)
                labelTimeActiveTimer.grid_forget()
                labelTimePassiveTimer.grid_forget()
                timerON = False
        else:
            labelErrorTime.grid(row=8, column=0, columnspan=4,sticky=tk.W)
            labelTimeActiveTimer.grid_forget()
            labelTimePassiveTimer.grid_forget()
            timerON = False
    else:
        timerON = False
        labelTimeActiveTimer.grid_forget()
        labelTimePassiveTimer.grid(row=8, column=0, columnspan=4,sticky=tk.W)
    

# 画面の描画
baseGround = tk.Tk()
baseGround.geometry("305x170")
baseGround.resizable(width=False, height=False)
baseGround.title("ReactorControler")
labelReactorState = ttk.Label(text='リアクターの状態', foreground='black').grid(row=0, column=0, columnspan=4,sticky=tk.W)
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
entryHour.insert(0,str(hour))
entryHour.grid(row= 6, column=0)
labelTimeSeparator = ttk.Label(text=':', foreground='black').grid(row=6, column=1)
entryMinute = tk.Entry(width=3)
entryMinute.insert(0,str(minute))
entryMinute.grid(row= 6, column=2)
buttonSet = ttk.Button(
    baseGround, text = 'Set!', command=buttonSetTime_click).grid(row=7, column=0)
labelErrorTime = ttk.Label(text='時間は0~23,分は0~59で入力してください', foreground='red')
labelTimeActiveTimer = ttk.Label(text='タイマーを有効化しました', foreground='black')
labelTimePassiveTimer = ttk.Label(text='タイマーを無効化しました', foreground='black')
baseGround.after(1000, timer)
baseGround.mainloop()
        