import tkinter as tk
from tkinter import ttk
import ctypes
import time
import random
from turtle import screensize
import ctypes
import win32gui
import pyautogui #PyAutoGUI
from win32api import GetMonitorInfo, MonitorFromPoint #pywin23
from screeninfo import get_monitors #ScreenInfo
import threading #Thread6
import imageio #imageio
from PIL import Image, ImageTk, ImageDraw, ImageSequence #PIL
import pygetwindow as gw #pygetwindow
import sys
import os
from tkinter import colorchooser
import pickle

Version = "1.3.0"
app = None
Use = False

#ScreenStuff
monitorwidth = 0
monitorMinmum = 0
tempm = 0

Monitors = []
#Gets Length Of Monitor(s)
for m in get_monitors():
    # print(get_monitors()[tempm])
    if  get_monitors()[tempm].x < 0:
        monitorMinmum -= get_monitors()[tempm].width
    else:
        monitorwidth += get_monitors()[tempm].width
    Monitors.append([get_monitors()[tempm].x, get_monitors()[tempm].width, get_monitors()[tempm].y, get_monitors()[tempm].height])

    tempm += 1
# print(Monitors)

#Directional Stuff
LookingRight = True
x = -120
y = -50
WalkToPosition = None
speed = 0.08
Gravity = 0
GroundYPosition = 0
Velocity = [0,0]
cheesepos = 0

#Image Stuff
frame = 5
img = Image.open("data/pictures/ratwalk.gif")
IMGHEIGHT = img.height
IMGWIDTH = img.width
BlackOTLN = False

#states
CurrentState = "Walking"
DragState = "Walking"
LeastTime = 60
MostTime = 120
storedstate = "1"
newstate = "1"
menuopen = False

#Settings
LimitedVelocity = True
VelocityLimit = 40
AutomatedActions = True
speedoff = 1

d = None
#Hats
hatDir = None

DefaultSET = [(64, 64, 64),(48, 48, 48),(24, 24, 24),(128, 128, 128),
                 (255, 158, 221),(188, 139, 171),(188, 146, 173),(130, 104, 121)]

# with open('pictures/DefaultColor.pkl', 'wb') as file:
#     pickle.dump(Default, file)

# Read the data from the file
Default = None

if os.path.exists("data/DefaultColor.pkl"):
    with open('data/DefaultColor.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    Default = loaded_data
else:
    with open('data/DefaultColor.pkl', 'wb') as file:
        pickle.dump(DefaultSET, file)
    with open('data/DefaultColor.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
        Default = loaded_data
        

# Print the loaded data


#Colors
Gray = [(64, 64, 64),(48, 48, 48),(24, 24, 24),(128, 128, 128),
                 (255, 158, 221),(188, 139, 171),(188, 146, 173),(130, 104, 121)]
Brown = [(122, 88, 68),(98, 72, 57),(82, 58, 43),(29, 7, 3),
                 (181, 129, 119),(172, 122, 113),(160, 109, 99),(143, 89, 79)]
White = [(210, 210, 210), (183, 183, 183), (151, 151, 151), (0, 0, 0),
                 (255, 158, 221),(188, 139, 171),(188, 146, 173),(130, 104, 121)]
Remy = [(81, 125, 174), (75, 100, 158), (66, 87, 138), (222, 141, 103),
                 (255, 158, 221), (188, 139, 171), (188, 146, 173),(130, 104, 121)]
Blue = [(100, 129, 196), (102, 102, 193), (112, 121, 184), (0, 0, 0), 
        (255, 158, 221), (188, 139, 171), (188, 146, 173), (130, 104, 121)]


CurrentColor = Default.copy()

NewCo = Default.copy()

print("Rat Starting...")

# Main Rat Class
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

class Rat():
    
    def AddHat(self, image):
        global hatDir
        if hatDir != None:
            hat = Image.open(str(hatDir))
            # print(hatDir)
            for i in range(8):
                frame = ImageTk.getimage(image[i])
                g = Image.alpha_composite(frame,hat)
                # frame.paste(hat, (0,0))
                h= ImageTk.PhotoImage(g)
                pyimage5 = tk.PhotoImage()
                pyimage5.tk.call(pyimage5, 'copy', h)
                image[i] = pyimage5
            return
    
    def AniColor(self, frames, image):
        global CurrentColor
        global NewCo
        global Default
        global Brown
        global BlackOTLN
        # print(image)
        for f in range(frames):
            # print(f)
            for x in range(IMGWIDTH):
                for y in range(IMGHEIGHT):
                    # Get the current pixel's color
                    # print(x)
                    # print(y)
                    # print(f"{x} / {y}")
                    pixel = image[f].get(x, y)
                    for c in range(8):
                        if str(pixel) == str(DefaultSET[c]):
                            color = rgb_to_hex(NewCo[c])
                            image[f].put(color ,(x, y))
                        # print(pixel)
                        if str(pixel) == "(255, 255, 255)" and BlackOTLN:
                            # print("test")
                            color = "#000000"
                            image[f].put(color ,(x, y))
        CurrentColor = NewCo.copy()       
    
    def SetColor(self):
        
        
        self.Rolling = [tk.PhotoImage(
            file="data/pictures/RatRoll.gif", format='gif -index %i' % (i)) for i in range(4)]
        self.AniColor(4, self.Rolling)
        
        self.walking_right = [tk.PhotoImage(
            file="data/pictures/ratwalk.gif", format='gif -index %i' % (i)) for i in range(8)]
        # print(";;;;;;;;;;;;;;;;;;;;")
        # print(self.walking_right)
        
        self.AddHat(self.walking_right)
        self.AniColor(8, self.walking_right)
        
        self.walking_left = [tk.PhotoImage(
            file="data/pictures/ratwalkleft.gif", format='gif -index %i' % (i)) for i in range(8)]
        # self.AniColor(8, self.walking_left)
        for i in range(8):
            self.walking_left[i] = self.walking_right[i].subsample(x=-1, y=1)
        
        self.lay = [tk.PhotoImage(
            file="data/pictures/LayDown.png", format='png')]
        self.AniColor(1, self.lay)
        
        self.laying = [tk.PhotoImage(
            file="data/pictures/layingdown.gif", format='gif -index %i' % (i)) for i in range(6)]
        self.AniColor(6, self.laying)
        
        self.Ballooning = [tk.PhotoImage(
            file="data/pictures/Balloon.gif", format='gif -index %i' % (i)) for i in range(7)]
        self.AniColor(7, self.Ballooning)
    
        return

    #Runs On Start
    def __init__(self, window):
        #Sets the Window and image
        
        self.window = window
        self.roll_index = 0
        self.frame_index = 0
        
        print("Setting-Up Colors")
        self.SetColor()
        
        self.img = self.walking_right[self.frame_index]
        self.timestamp = time.time()
        self.timestamp2 = time.time()
        
        self.changeaction = time.time()
        global LeastTime
        global MostTime
        self.changeaction += random.randrange(LeastTime,MostTime)
        
        #Removes the background Colors
        self.window.config(highlightbackground='#418EE4')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', '#418EE4')
        self.label = tk.Label(self.window, bd=0, bg='#418EE4')
        
        #Finalizes Window
        self.x = 0

        self.wind = None
        self.window.geometry('138x144+{x}+0'.format(x=str(self.x)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(0, self.update)

        global x
        global monitorMinmum
        x = monitorMinmum - 120
        
        print("Rat Started")


    #Gravity Functions When Called Causes Gravity
    def Gravity(self):
        global Gravity
        global GroundYPosition
        global y
        if y < GroundYPosition:
            y += 1 * Gravity
            Gravity += 1
        elif y > GroundYPosition:
            y = GroundYPosition
        else:
            Gravity = 0
        return
    


    #Called Every Seconds or So
    def update(self):
        #Image
        global IMGHEIGHT
        global IMGWIDTH
        global frame
        #Screen
        global monitorwidth
        global monitorMinmum
        global GroundYPosition
        #Position
        global x
        global y
        global Gravity
        global Velocity
        #RatVar
        global CurrentState
        global LeastTime
        global MostTime
        global storedstate
        global newstate
        global LookingRight
        global WalkToPosition
        global speed
        #Settings
        global LimitedVelocity
        global AutomatedActions


        #Gets any Variables about ScreenSizes and the ground and keeps them updated
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        global Monitors
        size = screensize[1]
        Top = 0
        for arry in Monitors:
            if x > arry[0] and x < arry[0] + arry[1]:
                size = arry[2] + arry[3]
                Top = arry[2]
        GroundYPosition = int(size - IMGHEIGHT - (monitor_area[3]-work_area[3]))
        mousepos = pyautogui.position()

        #Calls Stuff INvolving The Mouse
        self.label.bind("<Button-2>", self.popup)
        self.label.bind("<Button-3>", self.dis)
        self.label.bind("<ButtonPress-1>", self.Drag)
        self.label.bind("<ButtonRelease-1>", self.StopDrag)

        #checks if the rat is under the ground
        if y > GroundYPosition:
            y = GroundYPosition
        
        #automates actions
        if AutomatedActions == True:
            if self.changeaction <= time.time():
                self.changeaction = time.time()
                self.changeaction += random.randrange(LeastTime,MostTime)
                randomoptions = ["Walking", "Sitting", "Chasing", "Rolling", "Cheese", "Balloon"]
                storedstate = CurrentState
                newstate = random.choice(randomoptions)
                self.frame_index = 0
                if storedstate == "Sitting" and newstate != "Sitting":
                    frame = 6
                    CurrentState = "Standing"
                elif storedstate == "Sitting" and newstate == "Sitting":
                    pass
                else:
                    CurrentState = newstate
                    if CurrentState == "Sitting":
                        frame = 0
                        
                        
        if CurrentState == "Balloon":
            if self.frame_index == 6:
                if y > Top:
                    y -= 1
                else:
                    CurrentState = "Walking"
            if time.time() > self.timestamp + 0.1 and self.frame_index !=6:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 7
                self.img = self.Ballooning[self.frame_index]
                        
        global speedoff
        #Walking Function
        if CurrentState == "Walking":
            self.Gravity()
            if time.time() > self.timestamp2 + speed:
                if WalkToPosition == None:
                    WalkToPosition = random.randrange(monitorMinmum, monitorwidth - int(IMGWIDTH/2))
                if WalkToPosition > x:
                    LookingRight = True
                    x += 1
                elif WalkToPosition < x:
                    LookingRight = False
                    x -= 1
                self.timestamp2 = time.time()



                if x >= WalkToPosition - 5 and x <= WalkToPosition + 5:
                    WalkToPosition = None
            #Updates The Rat Image
            if time.time() > self.timestamp + 0.1:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 8
                if LookingRight == True:
                    self.img = self.walking_right[self.frame_index]
                else:
                    self.img = self.walking_left[self.frame_index]

        if CurrentState == "Rolling":
            if x >= monitorwidth - int(IMGWIDTH):
                CurrentState = "Walking"
            LookingRight = True
            x += 5
            if time.time() > self.timestamp + 0.1:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.roll_index = (self.roll_index + 1) % 4
                self.img = self.Rolling[self.roll_index]

        #Dragging Function
        if CurrentState == "Dragging":
            global VelocityLimit
            TempVelocity = [x,y]
            x = mousepos.x - int(IMGWIDTH/2)
            y = mousepos.y - int(IMGHEIGHT/2)
            Velocity = [x - TempVelocity[0],y - TempVelocity[1]]
            if LimitedVelocity == True:
                if Velocity[0] > VelocityLimit:
                    Velocity[0] = VelocityLimit
                if Velocity[0] < -VelocityLimit:
                    Velocity[0] = -VelocityLimit
                if Velocity[1] > VelocityLimit:
                    Velocity[1] = VelocityLimit
                if Velocity[1] < -VelocityLimit:
                    Velocity[1] = -VelocityLimit

        
            if time.time() > self.timestamp + 0.05:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 8
                if LookingRight == True:
                    self.img = self.walking_right[self.frame_index]
                else:
                    self.img = self.walking_left[self.frame_index]
                    
            if y >= GroundYPosition + 1000:
                global DragState
                CurrentState = DragState

        #Falling/Throwing Function
        if CurrentState == "Falling":
            if Velocity[1] == 0:
                Velocity[1] = 1
            x += Velocity[0]
            y += Velocity[1]

            #allows for bouncing off walls
            if x >= monitorwidth:
                x = monitorwidth
                Velocity[0] = -Velocity[0]
            if x <= monitorMinmum:
                x = monitorMinmum
                Velocity[0] = -Velocity[0]
            if y <= 0:
                y = 0
                Velocity[1] = 0
                
                
                
            #Lossens Velocity
            if Velocity[0] > 0:
                Velocity[0] -= 1
            if Velocity[0] < 0:
                Velocity[0] += 1
                
            if Velocity[1] > 0:
                Velocity[1] += 1
            elif Velocity[1] < 0:
                Velocity[1] += 1
                
            if y >= GroundYPosition:
                CurrentState = DragState


        #Laying Down Function
        if CurrentState == "Sitting":
            if time.time() > self.timestamp + 0.1: 
                self.timestamp = time.time()
                    # advance the frame by one, wrap back to 0 at the end
                self.img = self.laying[frame]
                if frame < 5:
                    frame += 1
        #Stinding Up Function
        if CurrentState == "Standing":
            if time.time() > self.timestamp + 0.1: 
                self.timestamp = time.time()
                    # advance the frame by one, wrap back to 0 at the end
                frame -= 1
                if frame >= 0:
                    self.img = self.laying[frame]
                else:
                    CurrentState = newstate
        
        #Chasing Function
        if CurrentState == "Chasing":
            self.Gravity()
            if time.time() > self.timestamp:
                WalkToPosition = mousepos.x - int(IMGWIDTH/2)
                if x >= WalkToPosition - 30 and x <= WalkToPosition + 30:
                    self.img = self.laying[5]
                else:
                    if WalkToPosition > x:
                        LookingRight = True
                        x += 3
                    elif WalkToPosition < x:
                        LookingRight = False
                        x -= 3
            
                    #Updates The Rat Image
                    if time.time() > self.timestamp + 0.06:
                        self.timestamp = time.time()
                        # advance the frame by one, wrap back to 0 at the end
                        self.frame_index = (self.frame_index + 1) % 8
                        if LookingRight == True:
                            self.img = self.walking_right[self.frame_index]
                        else:
                            self.img = self.walking_left[self.frame_index]

        #Cheesing Function
        if CurrentState == "Cheese":
            self.Gravity()
            if AutomatedActions == True:
                AutomatedActions = False
                thread1 = threading.Thread(target=Cheese)
                thread1.start()
                
            global cheesepos
            if time.time() > self.timestamp:
                if cheesepos > x:
                    LookingRight = True
                    x += 3
                elif cheesepos < x:
                    LookingRight = False
                    x -= 3
            
            #Updates The Rat Image
            if time.time() > self.timestamp + 0.08:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 8
                if LookingRight == True:
                    self.img = self.walking_right[self.frame_index]
                else:
                    self.img = self.walking_left[self.frame_index]

        #Sets Window positions and INformation
        self.window.geometry('{width}x{height}+{x}+{y}'.format(x=x, y=y, width=str(img.width), height=str(img.height)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(10, self.update)

    #Debug Pop-up
    def popup(self, event):
        #Variables
        global WalkToPosition
        global LimitedVelocity
        LVSub = tk.BooleanVar()
        LVSub.set(LimitedVelocity)
        global AutomatedActions
        AASub = tk.BooleanVar()
        AASub.set(AutomatedActions)
        #Menu Settings
        my_menu = tk.Menu(self.window, tearoff=False, background='white', fg='black', activeforeground="black")
        ActionsSub = tk.Menu(my_menu, tearoff=0)
        SettingsSub = tk.Menu(my_menu, tearoff=0)
        DebugsSub = tk.Menu(my_menu, tearoff=0)
        
        #Actions
        my_menu.add_cascade(label="Actions", menu=ActionsSub)
        ActionsSub.add_separator()
        ActionsSub.add_command(label="Walk", command=self.JustWalk)
        ActionsSub.add_command(label="Roll", command=self.Roll)
        #ACT-Chase
        ActionsSub.add_command(label="Chase", command=self.Chase)
        #ACT-Sit/Stand
        if CurrentState == "Sitting":
            ActionsSub.add_command(label="Stand", command=self.Sit)
        else:
            ActionsSub.add_command(label="Sit", command=self.Sit)
        #cheese
        ActionsSub.add_command(label="Summon Cheese", command=self.Cheese)        
        ActionsSub.add_command(label="Balloon", command=self.Balloon)        
        ActionsSub.add_separator()
              
        # #Settings
        # my_menu.add_cascade(label="Settings", menu=SettingsSub)
        # SettingsSub.add_separator()
        # SettingsSub.add_checkbutton(label="Limit Throw Velocity", variable=LVSub, command=self.ToggleLimitedVelocity)
        # SettingsSub.add_checkbutton(label="Automate Actions", variable=AASub, command=self.ToggleAutoA)
        # SettingsSub.add_separator()
        
        # #Debugs
        # my_menu.add_cascade(label="Debugs", menu=DebugsSub)
        # DebugsSub.add_separator()
        # DebugsSub.add_command(label=f"[ Current State: ({CurrentState}) ]")
        # DebugsSub.add_command(label=f"[ Current WalkToPosition: ({WalkToPosition}) ]")
        # # if AutomatedActions == True:
        #     # DebugsSub.add_command(label=f"[ AutoStates: {int(self.changeaction)}/{int(time.time())}]")
        # DebugsSub.add_command(label=f"New Random WalkToPosition", command=self.newposition)
        # DebugsSub.add_separator()
        
        #Extra Parts
        my_menu.add_command(label="KILL", command=self.quit)
        my_menu.tk_popup(event.x_root, event.y_root)

    #Pop Up Functions
    def newposition(self):
        global WalkToPosition
        WalkToPosition = None
    def quit(self):
        exit()
    def Sit(self):
        self.frame_index = 0
        global CurrentState
        global frame
        if CurrentState != "Sitting":
            frame = 0
            CurrentState = "Sitting"
        else:
            frame = 6
            CurrentState = "Standing"
    def Roll(self):
        self.frame_index = 0
        global CurrentState
        CurrentState = "Rolling"
    def Chase(self):
        self.frame_index = 0
        global CurrentState
        CurrentState = "Chasing"
    def ToggleLimitedVelocity(self):
        global LimitedVelocity
        LimitedVelocity = not LimitedVelocity
    def ToggleAutoA(self):
        global AutomatedActions
        AutomatedActions = not AutomatedActions
    def JustWalk(self):
        self.frame_index = 0
        global CurrentState
        CurrentState = "Walking"
    def Balloon(self):
        global CurrentState
        self.frame_index = 0
        CurrentState = "Balloon"

    def Cheese(self):
        global CurrentState
        CurrentState = "Cheese"
    def dis(self, event):
        global menuopen
        global d
        if menuopen == False:
            menuopen = True
            d = Display()
        else:
            menuopen = False


    #Start/Stop Drag Functions
    def Drag(self, event):
        global CurrentState
        global DragState
        if CurrentState == "Balloon":
            DragState = "Walking"
        else:
            DragState = CurrentState
        CurrentState = "Dragging"
    def StopDrag(self, event):
        global CurrentState
        global DragState
        CurrentState = "Falling"

class Cheese():

    def __init__(self):
        self.grav = 0
        self.CheeseState = "Normal"
        self.window = tk.Toplevel()
        self.img = [tk.PhotoImage(
            file="data/pictures/food.png")]
        food = Image.open("data/pictures/food.png")
        self.window.config(highlightbackground='#418EE4')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', '#418EE4')
        self.label = tk.Label(self.window, bd=0, bg='#418EE4')
        global monitorwidth
        global x
        self.x = x
        while self.x > x - 500 and self.x < x + 500:
            self.x = random.randrange(monitorMinmum, monitorwidth - int(img.width))
        self.y = -1000000000010
        self.gravy = 0
        self.window.geometry(
            '{width}x{height}+{x}+{y}'.format(x=str(self.x), y=str(self.y), width=str(food.width), height=str(food.height)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(0, self.update)
        self.personalallowrandom = True
        self.gp = 0

    def gravity(self):
        if self.y >= self.gp:
            self.y = self.gp
            self.grav = 0
        else:
            self.y += self.grav
            self.grav += 1
        
        return

    def update(self):
        food = Image.open("data/pictures/food.png")
        
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        global Monitors
        size = screensize[1]
        for arry in Monitors:
            if self.x > arry[0] and self.x < arry[0] + arry[1]:
                size = arry[2] + arry[3]
        GroundYPosition = int(size - food.height - (monitor_area[3]-work_area[3]))
        self.gp = GroundYPosition
        UnderYPosition = int(screensize[1] - (monitor_area[3]-work_area[3]))
        
        mousepos = pyautogui.position()

        self.label.bind("<ButtonPress-1>", self.Drag)
        self.label.bind("<ButtonRelease-1>", self.StopDrag)
        
        if self.y < -1000000000000:
            self.y = size
            self.grav = 0
        
        if self.y < GroundYPosition and self.CheeseState != "Dragging":
            self.gravity()
        else:
            self.grav = 0
            
        if self.y > GroundYPosition:
            self.y -= 1
        

            
        global cheesepos
        cheesepos = self.x
        
        if self.CheeseState == "Dragging":
            self.x = mousepos.x - int(food.width/2)
            self.y = mousepos.y - int(food.height/2)    
            
        global CurrentState
        global AutomatedActions
            
        if x > cheesepos -5 and x < cheesepos + 5 and self.CheeseState != "Dragging" and self.y == GroundYPosition:
            CurrentState = "Walking"
            AutomatedActions = True
            self.window.destroy()
        else:
                # Windows Settings
            self.window.geometry(
                        '{width}x{height}+{x}+{y}'.format(x=self.x, y=self.y, width=str(food.width), height=str(food.height)))
            self.label.configure(image=self.img)
            self.label.pack()
            self.window.after(10, self.update)
                
    def Drag(self, event):
        self.CheeseState = "Dragging"
    def StopDrag(self, event):
        self.CheeseState = "Normal"

class Display():

    def DBTab(self):
        #Debug Stuff
        CSLABEL = tk.Label(self.DBug, text="Current State:")
        CSLABEL.grid(row=0, column=0, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=1, column=0, sticky=tk.NSEW)
        self.CSMNT = tk.Label(self.DBug, text="Walking")
        self.CSMNT.grid(row=0, column=1, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=1, column=1, sticky=tk.NSEW)
        
        WTLABEL = tk.Label(self.DBug, text="Walk-To-Position:")
        WTLABEL.grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=3, column=0, sticky=tk.NSEW)
        self.WTMNT = tk.Label(self.DBug, text="12")
        self.WTMNT.grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=3, column=1, sticky=tk.NSEW)

        CPLABEL = tk.Label(self.DBug, text="Rat Position:")
        CPLABEL.grid(row=4, column=0, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=5, column=0, sticky=tk.NSEW)
        self.CPMNT = tk.Label(self.DBug, text="12")
        self.CPMNT.grid(row=4, column=1, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=5, column=1, sticky=tk.NSEW)

        MPLABEL = tk.Label(self.DBug, text="Cursor Position:")
        MPLABEL.grid(row=6, column=0, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=7, column=0, sticky=tk.NSEW)
        self.MPMNT = tk.Label(self.DBug, text="12")
        self.MPMNT.grid(row=6, column=1, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=7, column=1, sticky=tk.NSEW)
        
        tk.Button(self.DBug, text="New Walk-Position:", command=self.newwalktoposition).grid(row=80, column=0, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=90, column=0, sticky=tk.NSEW)
        self.DWNLWC = tk.Button(self.DBug, text="Download Walk", command=self.download)
        self.DWNLWC.grid(row=80, column=1, sticky=tk.NSEW)
        ttk.Separator(self.DBug).grid(row=90, column=1, sticky=tk.NSEW)
        
        return
        
    def STTab(self):
        
        global LimitedVelocity
        global VelocityLimit
        global AutomatedActions
                
        #Setting Variables
        LMV = tk.IntVar()
        LMV.set(LimitedVelocity)
        LVMT = tk.IntVar()
        LVMT.set(VelocityLimit)
        
        #Notebook Stuff
        self.Settingsnotebook = ttk.Notebook(self.Sett, style="TNotebook")
        self.IdleSett = tk.Frame(self.Settingsnotebook, background="#f0f0f0")
        self.ActionSett = tk.Frame(self.Settingsnotebook, background="#f0f0f0")
        self.IdleSett.rowconfigure(100, weight=4)
        self.IdleSett.columnconfigure(1, weight=4)
        self.ActionSett.rowconfigure(100, weight=1)
        self.ActionSett.columnconfigure(1, weight=1)
        self.Settingsnotebook.add(self.IdleSett, text="Idle")
        self.Settingsnotebook.add(self.ActionSett, text="Action")
        
        # Action Settings
        LTVLabel = tk.Label(self.ActionSett, text="Limit Throw Velocity")
        LTVLabel.grid(row=0, column=0, sticky=tk.NSEW)
        ttk.Separator(self.ActionSett).grid(row=1, column=0, sticky=tk.NSEW)
        

        self.LTVCheck = tk.Button(self.ActionSett, text="Toggle OFF", command=self.LMTV, width=100)
        # if LimitedVelocity:
            # self.LTVCheck.config(text="   Toggle OFF  ")
        
        self.LTVCheck.grid(row=0, column=1, sticky=tk.NSEW)
        ttk.Separator(self.ActionSett).grid(row=1, column=1, sticky=tk.NSEW)
        
        LTVLabel2 = tk.Label(self.ActionSett, text="Throw Velocity Limit")
        LTVLabel2.grid(row=2, column=0, sticky=tk.NSEW)
        LTVSlide = tk.Scale(self.ActionSett, orient=tk.HORIZONTAL, length=150, showvalue=0, variable=LVMT, command=self.LVMT, to=300)
        LTVSlide.grid(row=3, column=0, sticky=tk.NSEW)
        ttk.Separator(self.ActionSett).grid(row=4, column=0, sticky=tk.NSEW)
        
        self.LTVAMT = tk.Label(self.ActionSett, text="100")
        self.LTVAMT.grid(row=3, column=1, sticky=tk.NSEW)
        ttk.Separator(self.ActionSett).grid(row=4, column=1, sticky=tk.NSEW)
        
        
        #Idle Settings
        global MostTime
        global LeastTime
        self.minvar= tk.StringVar()
        self.minvar.set(str(LeastTime))
        self.maxvar= tk.StringVar()
        self.maxvar.set(str(MostTime))
        
        AALabel = tk.Label(self.IdleSett, text="Automate Actions")
        AALabel.grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Separator(self.IdleSett).grid(row=3, column=0, sticky=tk.NSEW)
        self.AACheck = tk.Button(self.IdleSett,text="Toggle OFF",command=self.AA)
        self.AACheck.grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Separator(self.IdleSett).grid(row=3, column=1, sticky=tk.NSEW)
        
        tk.Label(self.IdleSett, text="Min Auto Time").grid(row=4, column=0, sticky=tk.NSEW)
        tk.Label(self.IdleSett, text="Max Auto Time").grid(row=5, column=0, sticky=tk.NSEW)
        self.mnsboxlst = tk.Spinbox(self.IdleSett, from_=10, to=300, increment=1, textvariable=self.minvar)
        self.mnsboxlst.grid(row=4, column=1, sticky=tk.NSEW)
        
        self.mxsboxlst = tk.Spinbox(self.IdleSett, from_=10, to=301, increment=1, textvariable=self.maxvar)
        self.mxsboxlst.grid(row=5, column=1, sticky=tk.NSEW)
        ttk.Separator(self.IdleSett).grid(row=6, column=0, sticky=tk.NSEW)
        ttk.Separator(self.IdleSett).grid(row=6, column=1, sticky=tk.NSEW)
                
    def CTab(self):
        global Default
        global Brown
        global CurrentColor

        

        self.Rst = tk.Button(self.Looks, text="Reset", command=self.Reset)

        self.Apply = tk.Button(self.Looks, text="Apply", command=self.ApplyCo)

        self.Looksnotebook = ttk.Notebook(self.Looks, style="TNotebook")
        self.Colors = tk.Frame(self.Looksnotebook, background="#f0f0f0")
        self.Caps = tk.Frame(self.Looksnotebook, background="#f0f0f0")
        self.Colors.rowconfigure(100, weight=4)
        self.Colors.columnconfigure(1, weight=4)
        self.Caps.rowconfigure(100, weight=1)
        self.Caps.columnconfigure(1, weight=1)
        self.Looksnotebook.add(self.Colors, text="Colors")
        self.Looksnotebook.add(self.Caps, text="Caps & Details")
        
        #Fur Colors
        tk.Label(self.Colors, text="Fur Color 1: ", width=12).grid(row=2, column=0, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=3, column=0, sticky=tk.NSEW)
        self.Fc1 = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[0]), text="", command=lambda: self.pick_color(0, self.Fc1), width=4)
        self.Fc1.grid(row=2, column=1, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=3, column=1, sticky=tk.NSEW)
        tk.Label(self.Colors, text="Fur Color 2: ").grid(row=4, column=0, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=5, column=0, sticky=tk.NSEW)
        self.Fc2 = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[1]), text="", command=lambda: self.pick_color(1, self.Fc2))
        self.Fc2.grid(row=4, column=1, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=5, column=1, sticky=tk.NSEW)
        tk.Label(self.Colors, text="Fur Color 3: ").grid(row=6, column=0, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=7, column=0, sticky=tk.NSEW)
        self.Fc3 = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[2]), text="", command=lambda: self.pick_color(2, self.Fc3))
        self.Fc3.grid(row=6, column=1, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=7, column=1, sticky=tk.NSEW) 
        tk.Label(self.Colors, text="Eye Color: ").grid(row=8, column=0, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=9, column=0, sticky=tk.NSEW)

        #Eye Colors
        self.Ec = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[3]), text="", command=lambda: self.pick_color(3, self.Ec))
        self.Ec.grid(row=8, column=1, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=9, column=1, sticky=tk.NSEW) 

        #Ear Colors
        tk.Label(self.Colors, text="Ear/Nose Color: ", width=12).grid(row=2, column=2, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=3, column=2, sticky=tk.NSEW)
        self.Erc = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[4]), text="", command=lambda: self.pick_color(4, self.Erc), width=4)
        self.Erc.grid(row=2, column=3, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=3, column=3, sticky=tk.NSEW)

        # Tail Color
        tk.Label(self.Colors, text="Tail Color: ").grid(row=4, column=2, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=5, column=2, sticky=tk.NSEW)
        self.Tc = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[5]), text="", command=lambda: self.pick_color(5, self.Tc))
        self.Tc.grid(row=4, column=3, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=5, column=3, sticky=tk.NSEW)

        # Feet Color
        tk.Label(self.Colors, text="Feet Color 1: ").grid(row=6, column=2, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=7, column=2, sticky=tk.NSEW)
        self.Ftc1 = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[6]), text="", command=lambda: self.pick_color(6, self.Ftc1))
        self.Ftc1.grid(row=6, column=3, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=7, column=3, sticky=tk.NSEW)

        tk.Label(self.Colors, text="Feet Color 2: ").grid(row=8, column=2, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=9, column=2, sticky=tk.NSEW)
        self.Ftc2 = tk.Button(self.Colors, background=rgb_to_hex(CurrentColor[7]), text="", command=lambda: self.pick_color(7, self.Ftc2))
        self.Ftc2.grid(row=8, column=3, sticky=tk.NSEW)
        ttk.Separator(self.Colors).grid(row=9, column=3, sticky=tk.NSEW)
        

        self.ColorList = ["None"]
        self.ColorDirList = [None]

        directory = os.fsencode("data/Colors")

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".pkl"):
                Name_1 = filename.split(".")[0]
                Name_2 = Name_1.replace("_", " ")
                test = str((str(os.fsdecode(directory)) + "/" + str(filename)))

                self.ColorList.append(Name_2)
                self.ColorDirList.append(test)

        self.v = tk.StringVar()
        self.v.set(self.ColorList[0])
        self.om = tk.OptionMenu(self.Looks, self.v, *self.ColorList, command=self.ReFresh)

        self.name_var=tk.StringVar()
        self.name_var.set("Preset Name")
        tk.Entry(self.Colors, width=10, textvariable=self.name_var).grid(row=13, column=0, sticky=tk.NSEW)
        tk.Button(self.Colors, text="Create Preset", command=self.presetdownload).grid(row=13, column=2, sticky=tk.NSEW)

        #Caps
        self.Hatlist = ["None"]
        self.DirList = [None]

        directory = os.fsencode("data/pictures/Hats")

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".png"):
                Name_1 = filename.split(".")[0]
                Name_2 = Name_1.replace("_", " ")
                test = str((str(os.fsdecode(directory)) + "/" + str(filename)))
                imagetest = Image.open(test)
                if imagetest.width == 113:
                    if imagetest.height == 60:
                        self.Hatlist.append(Name_2)
                        self.DirList.append(test)

        self.cpvar = tk.StringVar()
        self.cpvar.set(self.Hatlist[0])
        tk.Label(self.Caps, text="Hats: ").grid(row=2, column=0)
        self.cplt = tk.OptionMenu(self.Caps, self.cpvar, *self.Hatlist)
        self.cplt.grid(row=2, column=1, sticky=tk.NSEW)

        ttk.Separator(self.Caps).grid(row=3, column=0, sticky=tk.NSEW)
        ttk.Separator(self.Caps).grid(row=3, column=1, sticky=tk.NSEW)

        tk.Label(self.Caps, text="Black Outline: ").grid(row=4, column=0, sticky=tk.NSEW)
        global BlackOTLN
        self.IsBlack = tk.Checkbutton(self.Caps, variable=False, command=self.BLKOLN)
        self.IsBlack.grid(row=4, column=1, sticky=tk.NSEW)

    def pick_color(self, btnid, btn):
        global CurrentColor
        global NewCo
        global Default
        global Brown
        color = colorchooser.askcolor(title="Choose a color")
        if color[1]:  # Check if a color was chosen (not canceled)
            NewCo[btnid] = color[0]

            btn.config(bg=color[1])
            
        return

    def ApplyCo(self):
        global app
        global NewCo
        with open('data/DefaultColor.pkl', 'wb') as file:
            pickle.dump(NewCo, file)
        app.SetColor()

    def Reset(self):
        global CurrentColor
        global Default
        global NewCo
        for c in range(8):
            NewCo[c] = CurrentColor[c]
        self.Fc1.config(bg=rgb_to_hex(CurrentColor[0]))
        self.Fc2.config(bg=rgb_to_hex(CurrentColor[1]))
        self.Fc3.config(bg=rgb_to_hex(CurrentColor[2]))
        self.Ec.config(bg=rgb_to_hex(CurrentColor[3]))
        self.Erc.config(bg=rgb_to_hex(CurrentColor[4]))
        self.Tc.config(bg=rgb_to_hex(CurrentColor[5]))
        self.Ftc1.config(bg=rgb_to_hex(CurrentColor[6]))
        self.Ftc2.config(bg=rgb_to_hex(CurrentColor[7])) 

    def ReFresh(self, g):
        global CurrentColor
        global Default
        global NewCo
        if self.v.get() != "None":
            num = 0
            for i in range(len(self.ColorList)):
                if self.ColorList[i] == self.v.get():
                    num = i
                    break
            cur = []
            with open(self.ColorDirList[i], 'rb') as file:
                loaded_data = pickle.load(file)
                cur = loaded_data
            for c in range(8):
                NewCo[c] = cur[c]
        self.Fc1.config(bg=rgb_to_hex(NewCo[0]))
        self.Fc2.config(bg=rgb_to_hex(NewCo[1]))
        self.Fc3.config(bg=rgb_to_hex(NewCo[2]))
        self.Ec.config(bg=rgb_to_hex(NewCo[3]))
        self.Erc.config(bg=rgb_to_hex(NewCo[4]))
        self.Tc.config(bg=rgb_to_hex(NewCo[5]))
        self.Ftc1.config(bg=rgb_to_hex(NewCo[6]))
        self.Ftc2.config(bg=rgb_to_hex(NewCo[7]))

    def presetdownload(self):
        global CurrentColor
        name = self.name_var.get()
        if name == "Preset Name":
            name = str(int(time.time())) 
        with open(f'data/Colors/{name}.pkl', 'wb') as file:
            pickle.dump(NewCo, file)
        self.close()

    def __init__(self):
        self.t = time.time()
        #sets up Window
        master = tk.Toplevel()
        master.overrideredirect(True)
        self.master = master

        global Use
        COLOR_GREEN = "#B9B9B9"
        COLOR_RED = "#f0f0f0"
        COLOR_BG = "#808B96"
        self.style = ttk.Style()
        if Use == False:
            self.style.theme_create("Main", parent="alt", settings={
                        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": COLOR_BG, "tabposition": 'n' } },
                        "TNotebook.Tab": {
                        "configure": {"padding": [8, 5], "background": COLOR_GREEN},
                        "map":       {"background": [("selected", COLOR_RED)],
                        "expand": [("selected", [1, 1, 1, 0])] } } } )

            Use = True
        self.style.theme_use("Main")

        


        self.notebook = ttk.Notebook(self.master)

        #Settings Tab
        self.Sett = tk.Frame(self.notebook, background="#f0f0f0")
        self.Sett.pack(expand=True, fill="both")
        
        
        #Debug Tab
        self.DBug = tk.Frame(self.notebook, background="#f0f0f0")
        self.KILL = tk.Frame(self.notebook, background="#f0f0f0")
        self.DBug.pack(expand=True, fill="both")
        self.DBug.rowconfigure(100, weight=1)
        self.DBug.columnconfigure(1, weight=1)


        self.Close = tk.Frame(self.notebook, background="#f0f0f0")

        self.Looks = tk.Frame(self.notebook, background="#f0f0f0")
        self.Looks.pack(expand=True, fill="both")
        self.Looks.rowconfigure(100, weight=1)
        self.Looks.columnconfigure(3, weight=1)
        

        
        # Create tabs for the notebook
        self.notebook.add(self.Looks, text="Looks")
        self.notebook.add(self.Sett, text="Settings")
        self.notebook.add(self.DBug, text="Debug")
        self.notebook.add(self.KILL, text="Kill Rat")
        self.notebook.add(self.Close, text="X")
        
        
        self.DBTab()
        self.STTab()
        self.CTab()

        global x
        global y
        self.x = x
        self.y = y

        global monitorwidth
        global monitorMinmum
        if self.x <= monitorMinmum + 80:
            self.x = monitorMinmum + 100

        if self.x >= monitorwidth-230:
            self.x = monitorwidth-300

        global hatDir
        for h in range(len(self.DirList)):
            if hatDir == self.DirList[h]:
                self.cpvar.set(self.Hatlist[h])


        # Pack the notebook
        self.Settingsnotebook.pack(expand=1, fill="both")
        self.Apply.pack(side="top", fill="both")
        self.Rst.pack(side="top", fill="both")
        self.om.pack(side="top", fill="both")
        self.Looksnotebook.pack(expand=1, fill="both")
        self.notebook.pack(expand=1, fill="both")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_select)
        self.master.geometry("180x165")
        self.master.after(10, self.update)
        self.master.mainloop()
        
    def kill(self):
        sys.exit()
    def on_tab_select(self, event):
        self.t = time.time()
        selected_tab = self.notebook.index(self.notebook.select())

        if selected_tab == 4:
            self.close()  # Close the window    
        if selected_tab == 3:
            self.kill()
    def close(self):
        global menuopen
        menuopen = False
        self.master.destroy()
    def LVMT(self, var):
        global VelocityLimit
        VelocityLimit = int(var)
    def SWT(self, variable):
        print("Swi")
        print(variable)
        variable = not variable
        print(variable)
    def LMTV(self):
        global LimitedVelocity
        LimitedVelocity = not LimitedVelocity
    def AA(self):
        global AutomatedActions
        AutomatedActions = not AutomatedActions
    def BLKOLN(self):
        global BlackOTLN
        BlackOTLN = not BlackOTLN
        
    def download(self):
        global app
        image = []
        for i in range(8):
            image.append(ImageTk.getimage(app.walking_right[i]))
            
        name = str(int(time.time()))
        imageio.mimsave(f"{name}.gif", image, fps=10, disposal=2, loop=0)
    def newwalktoposition(self):
        global WalkToPosition
        WalkToPosition = None

    def update(self):
        global menuopen
        global CurrentState
        global WalkToPosition
        global VelocityLimit
        global speedoff
        global LimitedVelocity
        global AutomatedActions
        
        global MostTime
        global LeastTime

        global hatDir
        for h in range(len(self.Hatlist)):
            if self.cpvar.get() == self.Hatlist[h]:
                hatDir = self.DirList[h]
                break
            else:
                hatDir = None
        
        LeastTime = int(self.mnsboxlst.get())
        MostTime = int(self.mxsboxlst.get())
        if LeastTime >= MostTime:
            self.maxvar.set(LeastTime+1)
        
        mousepos = pyautogui.position()
        
        
        if LimitedVelocity:
            self.LTVCheck.config(text="Toggle OFF")
        else:
            self.LTVCheck.config(text="Toggle ON")
        
        if AutomatedActions:
            self.AACheck.config(text="Toggle OFF")
        else:
            self.AACheck.config(text="Toggle ON")
        
        #debugs
        self.LTVAMT.configure(text=f"{VelocityLimit}")
        self.CSMNT.configure(text=f"{CurrentState}")
        self.WTMNT.configure(text=f"{WalkToPosition}")
        self.CPMNT.configure(text=f"({x} , {y})")
        self.MPMNT.configure(text=f"({mousepos.x} , {mousepos.y})")
        
        self.master.lift()
        self.master.geometry('{width}x{height}+{x}+{y}'.format(x=self.x+int(img.width/2) - 128 , y=self.y-330, width=str(256), height=str(300)))
        self.master.after(10, self.update)
        
        if menuopen == False:
            self.master.destroy()
        
        


# Display()
print(f"Version: {Version}")
window = tk.Tk()
app = Rat(window)
window.mainloop()


