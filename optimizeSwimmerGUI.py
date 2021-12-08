#///////////////////////////////////////////////////////////////////////
#Import libraries

import tkinter as tk
import tkinter.messagebox as tkMessageBox
import os
import math
import subprocess
import csv
import time
import CFDFunctions as cfd
import OptimizeFunctions as opt
file_path = os.path.dirname(os.path.realpath(__file__))


#///////////////////////////////////////////////////////////////////////
#Create main window
GUI = tk.Tk()


#///////////////////////////////////////////////////////////////////////
#Define callback functions
def closeWindow():
	os.chdir(file_path)
	GUI.destroy()
	cmd = "python3 startGUI.py"
	os.system(cmd)

def optimizeSwimmer():
	opt.gradientDescent(3,3)
	
	

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

ButtonCompute = tk.Button(GUI, text ="Compute", command = optimizeSwimmer)

ButtonClose = tk.Button(GUI, text ="Close", command = closeWindow)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number


ButtonCompute.grid(row=i,column=k)

ButtonClose.grid(row=i,column=k+1)




#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()
