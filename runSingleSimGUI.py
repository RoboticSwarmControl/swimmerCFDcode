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

def computeCFD():
	inputFormatCorrect=configureFiles()
	if inputFormatCorrect:
		averagedTimeWindow=1/(4*float(EntryRotationalSpeed.get()))
		cfd.runCaseUntilStable(4,averagedTimeWindow,1,3)
	forceY=cfd.getForce()[0]
	print('ForceY: {} N'.format(forceY[len(forceY)-1]))
	tkMessageBox.showinfo("Result","Propulsive force: {} N".format(forceY))
	
def configureFiles():
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles") #TODO: fix bug when running for second time
	
	#check if all entries have the correct format
	formatCorrect=True
	try:
		float(EntryRotationalSpeed.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Rotational speed must be a float number")

	try:
		float(EntryForwardVelocity.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Forward velocity must be a float number")

	
	if formatCorrect:
		cmd = "./Allclean"
		os.system(cmd)
		cfd.setRotationalSpeed(float(EntryRotationalSpeed.get()))
		cfd.setForwardVelcoity(0.001*float(EntryForwardVelocity.get()))
		
	return formatCorrect
	

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

LabelRotationalSpeed = tk.Label(GUI,text="Rotational speed [Hz]: ")
EntryRotationalSpeed = tk.Entry(GUI)
EntryRotationalSpeed.insert(0,"20") #default value

LabelForwardVelocity = tk.Label(GUI,text="Forward velocity [mm/s]: ")
EntryForwardVelocity = tk.Entry(GUI)
EntryForwardVelocity.insert(0,"0") #default value


ButtonCompute = tk.Button(GUI, text ="Compute", command = computeCFD)

ButtonClose = tk.Button(GUI, text ="Close", command = closeWindow)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

LabelRotationalSpeed.grid(row=i,column=k)
EntryRotationalSpeed.grid(row=i,column=k+1)

i=i+1

LabelForwardVelocity.grid(row=i,column=k)
EntryForwardVelocity.grid(row=i,column=k+1)

i=i+1
ButtonCompute.grid(row=i,column=k)

ButtonClose.grid(row=i,column=k+1)




#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()
