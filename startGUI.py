import tkinter as tk
import os

#///////////////////////////////////////////////////////////////////////
#Create main window
GUI = tk.Tk()


#///////////////////////////////////////////////////////////////////////
#Define callback functions

def CreateNewGeometry():
	GUI.destroy()
	cmd = "python3 createSwimmerGUI.py"
	os.system(cmd)
	
def ConfigureSimParameters():
	GUI.destroy()
	cmd = "python3 configureSimParGUI.py"
	os.system(cmd)
	
def RunSingleSim():
	GUI.destroy()
	cmd = "python3 runSingleSimGUI.py"
	os.system(cmd)
	
def RunStepOut():
	GUI.destroy()
	cmd = "python3 computeStepOutGUI.py"
	os.system(cmd)
	
def OptimizeSwimmer():
	GUI.destroy()
	cmd = "python3 optimizeSwimmerGUI.py"
	os.system(cmd)

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

ButtonCreateNewGeometry = tk.Button(GUI, text ="Create new swimmer geometry", command = CreateNewGeometry)

ButtonConfigure = tk.Button(GUI, text ="Configure simulation settings", command = ConfigureSimParameters)

ButtonRunSingleSim = tk.Button(GUI, text ="Compute for a given rotational speed", command = RunSingleSim)

ButtonStepOut = tk.Button(GUI, text ="Compute step out frequency", command = RunStepOut)

ButtonOptimize = tk.Button(GUI, text ="Optimize swimmer geometry", command = OptimizeSwimmer)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

ButtonCreateNewGeometry.grid(row=i,column=k)

i=i+2;

ButtonConfigure.grid(row=i,column=k)

i=i+2;

ButtonRunSingleSim.grid(row=i,column=k)

i=i+2;

ButtonStepOut.grid(row=i,column=k)

i=i+2;

ButtonOptimize.grid(row=i,column=k)




#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()

