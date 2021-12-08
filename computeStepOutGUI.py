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
		cfd.searchStepOutFrequency(float(EntryMoment.get()),float(EntryVoltage.get()),float(EntryResistance.get()),float(EntryInductance.get()),float(EntryConstant.get()),float(EntryNbEM.get()),float(EntryTol.get()))

def configureFiles():
	
	formatCorrect=True
	
	try:
		float(EntryMoment.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Magnetic moment must be a float number")
		
	try:
		float(EntryTol.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Tolerance must be a float number")
	
	try:
		float(EntryResistance.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Resistance must be a float number")

	try:
		float(EntryInductance.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Inductance must be a float number")
		
	try:
		float(EntryVoltage.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Voltage must be a float number")
		
	try:
		float(EntryConstant.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Electromagnet flux density constant must be a float number")
		
	try:
		float(EntryNbEM.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Number of electromagnet per axis must be a float number")

	if formatCorrect:
		cmd = "./Allclean"
		os.system(cmd)
		cfd.setForwardVelcoity(0)	
	return formatCorrect
	

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

LabelMoment = tk.Label(GUI,text="Magnetic moment [A.m^2]: ")
EntryMoment = tk.Entry(GUI)
EntryMoment.insert(0,"0.000001") #default value

LabelInductance = tk.Label(GUI,text="Electromagnet inductance [H]: ")
EntryInductance = tk.Entry(GUI)
EntryInductance.insert(0,"0.01") #default value

LabelResistance = tk.Label(GUI,text="Electromagnet resistance [H]: ")
EntryResistance = tk.Entry(GUI)
EntryResistance.insert(0,"7") #default value

LabelVoltage = tk.Label(GUI,text="Voltage (peak) [V]: ")
EntryVoltage = tk.Entry(GUI)
EntryVoltage.insert(0,"100") #default value

LabelConstant = tk.Label(GUI,text="Electromagnet flux density constant [T/A]: ")
EntryConstant = tk.Entry(GUI)
EntryConstant.insert(0,"0.0005") #default value

LabelNbEM = tk.Label(GUI,text="Number of electromagnet per axis: ")
EntryNbEM = tk.Entry(GUI)
EntryNbEM.insert(0,"2") #default value

LabelTol = tk.Label(GUI,text="Result tolerance [Hz]: ")
EntryTol = tk.Entry(GUI)
EntryTol.insert(0,"1") #default value

ButtonCompute = tk.Button(GUI, text ="Compute", command = computeCFD)

ButtonClose = tk.Button(GUI, text ="Close", command = closeWindow)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

LabelMoment.grid(row=i,column=k)
EntryMoment.grid(row=i,column=k+1)

i=i+1

LabelInductance.grid(row=i,column=k)
EntryInductance.grid(row=i,column=k+1)

i=i+1

LabelResistance.grid(row=i,column=k)
EntryResistance.grid(row=i,column=k+1)

i=i+1

LabelVoltage.grid(row=i,column=k)
EntryVoltage.grid(row=i,column=k+1)

i=i+1

LabelConstant.grid(row=i,column=k)
EntryConstant.grid(row=i,column=k+1)

i=i+1

LabelNbEM.grid(row=i,column=k)
EntryNbEM.grid(row=i,column=k+1)

i=i+1

LabelTol.grid(row=i,column=k)
EntryTol.grid(row=i,column=k+1)

i=i+1
ButtonCompute.grid(row=i,column=k)

ButtonClose.grid(row=i,column=k+1)




#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()
