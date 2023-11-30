import tkinter as tk
from tkinter import ttk
import ctypes
import time
import random
from turtle import screensize
import ctypes
import pyautogui #PyAutoGUI
from win32api import GetMonitorInfo, MonitorFromPoint #pywin23
from PIL import Image #PIL
from screeninfo import get_monitors #ScreenInfo
import threading #Thread6
from PIL import Image, ImageTk
import os


Version = "Beta 1.3.2"

mass = None


#ScreenStuff
monitorwidth = 0
tempm = 0
#Gets Length Of Monitor(s)
for m in get_monitors():
    monitorwidth += get_monitors()[tempm].width
    tempm += 1

#Directional Stuff
LookingRight = True
x = -200
y = -50
WalkToPosition = None
speed = 0.08
Gravity = 0
GroundYPosition = 0
Velocity = [0,0]

#Image Stuff
frame = 5
img = Image.open("pictures/ratwalk.gif")
IMGHEIGHT = img.height
IMGWIDTH = img.width

#states
CurrentState = "Walking"
DragState = "Walking"
MenuOpen = False
LeastTime = 60
MostTime = 180
storedstate = "1"
newstate = "1"


cheesepos = 0

#Settings
LimitedVelocity = True
AutomatedActions = True

print("Rat Starting...")

# Main Rat Class
class Rat():

    #Runs On Start
    def __init__(self, window):
        #Sets the Window and image
        
        self.window = window
        self.roll_index = 0
        self.Rolling = [tk.PhotoImage(
            file="pictures/RatRoll.gif", format='gif -index %i' % (i)) for i in range(4)]
        self.walking_right = [tk.PhotoImage(
            file="pictures/ratwalk_White.gif", format='gif -index %i' % (i)) for i in range(8)]
        self.walking_left = [tk.PhotoImage(
            file="pictures/ratwalkleft.gif", format='gif -index %i' % (i)) for i in range(8)]
        self.lay = [tk.PhotoImage(
            file="pictures/LayDown2.png", format='png')]
        self.laying = [tk.PhotoImage(
            file="pictures/layingdown.gif", format='gif -index %i' % (i)) for i in range(6)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]
        self.timestamp = time.time()
        self.changeaction = time.time()
        # self.changeaction += random.randrange(60, 180)
        global LeastTime
        global MostTime
        self.changeaction += random.randrange(LeastTime,MostTime)
        #Removes the background Colors
        self.window.config(highlightbackground='#418EE4')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', '#418EE4')
        # self.window.wm_attributes('#7a5844', '#d2d2d2')
        # print(self.img.width)
        for x in range(IMGWIDTH):
            for y in range(IMGHEIGHT):
                # Get the current pixel's color
                pixel = self.img.get( x, y)
                if str(pixel) == "(210, 210, 210)":
                    self.img.put("#7a5844",(x, y))
                    
                    # print(pixel)
                # new_image.putpixel((x, y), (new_color, new_color, new_color))
        self.label = tk.Label(self.window, bd=0, bg='#418EE4')
        #Finalizes Window
        self.x = 0
        self.window.geometry('138x144+{x}+0'.format(x=str(self.x)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(0, self.update)
        print("Rat Started")
        global Version
        print(f"Version: {Version}")

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
        GroundYPosition = int(screensize[1] - IMGHEIGHT - (monitor_area[3]-work_area[3]))
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
                randomoptions = ["Walking", "Sitting", "Chasing", "Rolling", "Cheese"]
                storedstate = CurrentState
                newstate = random.choice(randomoptions)
                if storedstate == "Sitting" and newstate != "Sitting":
                    frame = 6
                    CurrentState = "Standing"
                elif storedstate == "Sitting" and newstate == "Sitting":
                    pass
                else:
                    CurrentState = newstate
                    if CurrentState == "Sitting":
                        frame = 0
                        
                        
                # print(newstate)
                
        #Walking Function
        if CurrentState == "Walking":
            self.Gravity()
            if time.time() > self.timestamp + speed:
                if WalkToPosition == None:
                    WalkToPosition = random.randrange(0, monitorwidth - int(IMGWIDTH/2))
                    # print("Going To Position:" , WalkToPosition)
                if WalkToPosition > x:
                    LookingRight = True
                    x += 1
                elif WalkToPosition < x:
                    LookingRight = False
                    x -= 1
                # if x <= 0 - 110 or x >= monitorwidth + 110:
                #     WalkToPosition = None
                #     # global PipeThread
                #     PipeThread = threading.Thread(target=MarioPipe)
                #     PipeThread.start()
                #     CurrentState = "Piping"


                elif x >= WalkToPosition - 5 and x <= WalkToPosition + 5:
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
            if x >= monitorwidth - int(IMGWIDTH/2):
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
            # print(mousepos)
            TempVelocity = [x,y]
            x = mousepos.x - int(IMGWIDTH/2)
            y = mousepos.y - int(IMGHEIGHT/2)
            Velocity = [x - TempVelocity[0],y - TempVelocity[1]]
            if LimitedVelocity == True:
                if Velocity[0] > 40:
                    Velocity[0] = 40
                if Velocity[0] < -40:
                    Velocity[0] = -40
                if Velocity[1] > 40:
                    Velocity[1] = 40
                if Velocity[1] < -40:
                    Velocity[1] = -40
            # print(Velocity)

        
            if time.time() > self.timestamp + 0.05:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 8
                if LookingRight == True:
                    self.img = self.walking_right[self.frame_index]
                else:
                    self.img = self.walking_left[self.frame_index]

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
            if x <= 0:
                x = 0
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
                global DragState
                CurrentState = DragState

            # self.VGravity()

        #Laying Down Function
        if CurrentState == "Sitting":
            if time.time() > self.timestamp + 0.1: 
                self.timestamp = time.time()
                    # advance the frame by one, wrap back to 0 at the end
                frame += 1
                # print(frame)
                if frame <= 5:
                    # print(frame)
                    self.img = self.laying[frame]
        #Stinding Up Function
        if CurrentState == "Standing":
            if time.time() > self.timestamp + 0.1: 
                self.timestamp = time.time()
                    # advance the frame by one, wrap back to 0 at the end
                frame -= 1
                # print(frame)
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
        if CurrentState == "Chasing":
            ActionsSub.add_command(label="Stop Chase", command=self.Chase)
        else:
            ActionsSub.add_command(label="Chase", command=self.Chase)
        #ACT-Sit/Stand
        if CurrentState == "Sitting":
            ActionsSub.add_command(label="Stand", command=self.Sit)
        else:
            ActionsSub.add_command(label="Sit", command=self.Sit)
        #cheese
        ActionsSub.add_command(label="Summon Cheese", command=self.Cheese)        
        ActionsSub.add_separator()
        
            
        #Settings
        my_menu.add_cascade(label="Settings", menu=SettingsSub)
        SettingsSub.add_separator()
        SettingsSub.add_checkbutton(label="Limit Throw Velocity", variable=LVSub, command=self.ToggleLimitedVelocity)
        SettingsSub.add_checkbutton(label="Automate Actions", variable=AASub, command=self.ToggleAutoA)
        SettingsSub.add_separator()
        
        #Debugs
        my_menu.add_cascade(label="Debugs", menu=DebugsSub)
        DebugsSub.add_separator()
        DebugsSub.add_command(label=f"[ Current State: ({CurrentState}) ]")
        DebugsSub.add_command(label=f"[ Current WalkToPosition: ({WalkToPosition}) ]")
        # if AutomatedActions == True:
            # DebugsSub.add_command(label=f"[ AutoStates: {int(self.changeaction)}/{int(time.time())}]")
        DebugsSub.add_command(label=f"New Random WalkToPosition", command=self.newposition)
        DebugsSub.add_separator()
        
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
        global CurrentState
        global frame
        if CurrentState != "Sitting":
            frame = 0
            CurrentState = "Sitting"
        else:
            frame = 6
            CurrentState = "Standing"
    def Roll(self):
        global CurrentState
        if CurrentState == "Rolling":
            CurrentState = "Walking"
        else:
            CurrentState = "Rolling"
    def Chase(self):
        global CurrentState
        if CurrentState == "Chasing":
            CurrentState = "Walking"
        else:
            CurrentState = "Chasing"
    def ToggleLimitedVelocity(self):
        global LimitedVelocity
        LimitedVelocity = not LimitedVelocity
    def ToggleAutoA(self):
        global AutomatedActions
        AutomatedActions = not AutomatedActions
    def JustWalk(self):
        global CurrentState
        if CurrentState == "Sitting" or CurrentState == "Chasing":
            global frame
            frame = 6
            CurrentState = "Standing"
        else:
            CurrentState = "Walking"

    def Cheese(self):
        global CurrentState
        CurrentState = "Cheese"
        # thread1 = threading.Thread(target=Cheese)
        # thread1.start()

    def dis(self, event):
        # thread1 = threading.Thread(target=Display)
        # thread1.start()
        pass
        # Display()

    #Start/Stop Drag Functions
    def Drag(self, event):
        global CurrentState
        global DragState
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
        global monitorwidth
        self.window = tk.Toplevel()
        self.img = [tk.PhotoImage(
            file="pictures/food.png")]
        food = Image.open("pictures/food.png")
        self.window.config(highlightbackground='#418EE4')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', '#418EE4')
        self.label = tk.Label(self.window, bd=0, bg='#418EE4')
        global monitorwidth
        self.x = random.randrange(0, monitorwidth - int(img.width/2))
        self.y = -1000
        self.gravy = 0
        self.window.geometry(
            '{width}x{height}+{x}+{y}'.format(x=str(self.x), y=str(self.y), width=str(food.width), height=str(food.height)))
        self.label.configure(image=self.img)
        self.label.pack()
        self.window.after(0, self.update)
        # self.window.mainloop()
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
        food = Image.open("pictures/food.png")
        
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        GroundYPosition = int(screensize[1] - food.height - (monitor_area[3]-work_area[3]))
        self.gp = GroundYPosition
        UnderYPosition = int(screensize[1] - (monitor_area[3]-work_area[3]))
        
        mousepos = pyautogui.position()

        self.label.bind("<ButtonPress-1>", self.Drag)
        self.label.bind("<ButtonRelease-1>", self.StopDrag)
        
        if self.y < -200:
            self.y = screensize[1]
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
            
            global x
            global CurrentState
            global AutomatedActions
            
        if x > cheesepos -5 and x < cheesepos + 5 and CurrentState == "Cheese" and self.CheeseState != "Dragging":
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

    def __init__(self):
        master = tk.Toplevel()
        
        self.master = master
        # self.master.title("Styled Notebook App")

        # Create a styled notebook
        self.notebook_style = ttk.Style()
        self.notebook_style.configure("TNotebook", background="#638")
        self.notebook_style.configure("TNotebook.Tab", background="#263", padding=[10, 5], font=('Helvetica', 10))

        self.notebook = ttk.Notebook(self.master, style="TNotebook")

        # Create tabs for the notebook
        tab1 = tk.Frame(self.notebook, background="#ececec")
        tab2 = tk.Frame(self.notebook, background="#ececec")

        self.notebook.add(tab1, text="Tab 1")
        self.notebook.add(tab2, text="Tab 2")

        # Pack the notebook
        self.notebook.pack(expand=1, fill="both")
        self.master.geometry("300x150")
        self.master.mainloop()
    
    # def __init__(self):
        
    #     root = tk.Tk()
    #     root.title("Styled Notebook Tabs")

    #     # Create a style for the notebook tabs

    #     # Create a notebook widget
    #     notebook = ttk.Notebook(root)

    #     # Create tabs with the specified names
    #     tab = ttk.Frame(notebook)
    #     notebook.add(tab, text="tes")

    #     notebook.pack(expand=1, fill="both")

        # self.tabholder = Notebook(self.window)
        # self.tabholder.pack(side="top", expand=True, fill="both")
        # self.Tab1 = Frame(self.tabholder)
        # self.Tab1.configure(background="#637")
        # self.Tab2 = Frame(self.tabholder)
        # self.tabholder.add(self.Tab1, text="Test")
        # self.tabholder.add(self.Tab2, text="Test2")
        # self.tabholder.configure()
        # self.tabholder.pack(expand = 1, fill=BOTH)

        # button31=tk.Button(self.window, text="Ball", width = 6)
        # button31.grid(row=2,column=0, padx=5)
        # button32=tk.Button(self.window, text="Chase", width = 6, anchor='center')
        # button32.grid(row=2,column=2, pady=5)
        # button33=tk.Button(self.window, text="Stay", width = 6)
        # button33.grid(row=2,column=3, padx=5)
        # self.window.pack()
        
        
    


window = tk.Tk()
app = Rat(window)
window.mainloop()


