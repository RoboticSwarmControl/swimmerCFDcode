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
	
def ConfigureComputeSingleCase():
	GUI.destroy()
	cmd = "python3 configureRunSingleCaseGUI.py"
	os.system(cmd)

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

ButtonCreateNewGeometry = tk.Button(GUI, text ="Create new swimmer geometry", command = CreateNewGeometry)

ButtonConfigureComputeSingleCase = tk.Button(GUI, text ="Configure / Compute single case", command = ConfigureComputeSingleCase)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

ButtonCreateNewGeometry.grid(row=i,column=k)

i=i+2;

ButtonConfigureComputeSingleCase.grid(row=i,column=k)




#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()

