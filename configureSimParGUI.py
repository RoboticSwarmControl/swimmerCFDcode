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


def configureFiles():
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles") #TODO: fix bug when running for second time
	
	#check if all entries have the correct format
	formatCorrect=True

	try:
		float(EntryCellLength.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Cell length must be a float number")
		
	try:
		float(EntryCourantNumber.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Courant number must be a float number")
		
	try:
		int(EntrySwimmerRefinment.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Swimmer refnment level must be an int number")
		
	try:
		int(EntryInnerCylRefinment.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Rotating domain refinment level must be an int number")
		
	try:
		float(EntryOuterBoundaryDiameter.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Outer boundary diameter must be a float number")
		
	try:
		float(EntryOuterBoundaryLength.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Outer boundary diameter must be a float number")
		
	try:
		float(EntryRotatingBoundaryDiameter.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Rotating domain diameter must be a float number")
		
	try:
		float(EntryRotatingBoundaryLength.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Rotating domain length must be a float number")
		

	if formatCorrect:
		cmd = "./Allclean"
		os.system(cmd)
		cfd.setMaxCourantNumber(float(EntryCourantNumber.get()))
		cfd.setSwimmerRefinment(int(EntrySwimmerRefinment.get()))
		cfd.setRotatingDomainRefinment(int(EntryInnerCylRefinment.get()))
		cfd.setOuterCylinderSize(0.001*float(EntryOuterBoundaryDiameter.get()),0.001*float(EntryOuterBoundaryLength.get()))
		cfd.setInnerCylinderSize(0.001*float(EntryRotatingBoundaryDiameter.get()),0.001*float(EntryRotatingBoundaryLength.get()))
		cfd.setBlockMesh(max(float(EntryOuterBoundaryDiameter.get())*0.501/1000,float(EntryOuterBoundaryLength.get())*0.501/1000),float(EntryCellLength.get())/1000 )#blockmesh creates the initial mesh - setBlockMesh(blockSize,maxElementSize)
		
	return formatCorrect
	

   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

LabelCellLength = tk.Label(GUI,text="Max cell length [mm]: ")
EntryCellLength = tk.Entry(GUI)
EntryCellLength.insert(0,"0.5") #default value

LabelSwimmerRefinment = tk.Label(GUI,text="Swimmer mesh refinment: ")
EntrySwimmerRefinment = tk.Entry(GUI)
EntrySwimmerRefinment.insert(0,"2") #default value

LabelInnerCylRefinment = tk.Label(GUI,text="Rotating domain mesh refinment: ")
EntryInnerCylRefinment = tk.Entry(GUI)
EntryInnerCylRefinment.insert(0,"1") #default value

LabelCourantNumber = tk.Label(GUI,text="Max courant number: ")
EntryCourantNumber = tk.Entry(GUI)
EntryCourantNumber.insert(0,"5") #default value

LabelOuterBoundaryDiameter = tk.Label(GUI,text="Outer boundary diameter [mm]: ")
EntryOuterBoundaryDiameter = tk.Entry(GUI)
EntryOuterBoundaryDiameter.insert(0,"15") #default value

LabelOuterBoundaryLength = tk.Label(GUI,text="Outer boundary length [mm]: ")
EntryOuterBoundaryLength = tk.Entry(GUI)
EntryOuterBoundaryLength.insert(0,"22") #default value

LabelRotatingBoundaryDiameter = tk.Label(GUI,text="Rotating boundary diameter [mm]: ")
EntryRotatingBoundaryDiameter = tk.Entry(GUI)
EntryRotatingBoundaryDiameter.insert(0,"5") #default value

LabelRotatingBoundaryLength = tk.Label(GUI,text="Rotating boundary length [mm]: ")
EntryRotatingBoundaryLength = tk.Entry(GUI)
EntryRotatingBoundaryLength.insert(0,"12") #default value

ButtonSet = tk.Button(GUI, text ="Configure files", command = configureFiles)

ButtonClose = tk.Button(GUI, text ="Close", command = closeWindow)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

LabelCellLength.grid(row=i,column=k)
EntryCellLength.grid(row=i,column=k+1)
i=i+1

LabelSwimmerRefinment.grid(row=i,column=1)
EntrySwimmerRefinment.grid(row=i,column=k+1)
i=i+1

LabelInnerCylRefinment.grid(row=i,column=1)
EntryInnerCylRefinment.grid(row=i,column=k+1)
i=i+1

LabelCourantNumber.grid(row=i,column=1)
EntryCourantNumber.grid(row=i,column=k+1)
i=i+1

LabelOuterBoundaryDiameter.grid(row=i,column=1)
EntryOuterBoundaryDiameter.grid(row=i,column=k+1)
i=i+1

LabelOuterBoundaryLength.grid(row=i,column=1)
EntryOuterBoundaryLength.grid(row=i,column=k+1)
i=i+1

LabelRotatingBoundaryDiameter.grid(row=i,column=1)
EntryRotatingBoundaryDiameter.grid(row=i,column=k+1)
i=i+1

LabelRotatingBoundaryLength.grid(row=i,column=1)
EntryRotatingBoundaryLength.grid(row=i,column=k+1)
i=i+2

ButtonSet.grid(row=i,column=k)

ButtonClose.grid(row=i,column=k+1)

#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()
