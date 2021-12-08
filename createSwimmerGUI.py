import tkinter as tk
import os
import sys
sys.path.append('SwimmerGeometryGeneration')
import GeometryFunctions as GF
import CFDFunctions as CFD

#///////////////////////////////////////////////////////////////////////
#Create main window
GUI = tk.Tk()


#///////////////////////////////////////////////////////////////////////
#Define callback functions

def closeWindow():
	GUI.destroy()
	cmd = "python3 startGUI.py"
	os.system(cmd)
	
def generateGeometry():
	
	formatCorrect=True
	
	try:
		Diam=float(EntryDiameter.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Diameter must be a float number")
		
	try:
		Ptch1=float(EntryPitchTop.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Top pitch must be a float number")
		
	try:
		Ptch2=float(EntryPitchBottom.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Bottom pitch must be a float number")
		
	try:
		Length=float(EntryLength.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Length must be a float number")
		
	try:
		Thread=float(EntryThread.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Thread must be a float number")
		
	try:
		Curve=float(EntryCurve.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Curve must be a float number")
		
	try:
		Thickness=float(EntryThickness.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Thickness must be a float number")
		
	try:
		Cut=float(EntryCut.get())
	except:
		formatCorrect=False
		tkMessageBox.showinfo("Incorrect input","Cut must be a float number")
		

	if formatCorrect:
		CFD.cleanCase()
		GF.createGeometry(Diam,Ptch2,Ptch1,Length,Thread,Curve, Thickness, Cut)
	
	
   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

LabelDiameter = tk.Label(GUI,text="Diameter [mm]: ")
EntryDiameter = tk.Entry(GUI)
EntryDiameter.insert(0,"2.5") #default value

LabelPitchTop = tk.Label(GUI,text="Top pitch [mm]: ")
EntryPitchTop = tk.Entry(GUI)
EntryPitchTop.insert(0,"2.5") #default value

LabelPitchBottom = tk.Label(GUI,text="Bottom pitch [mm]: ")
EntryPitchBottom = tk.Entry(GUI)
EntryPitchBottom.insert(0,"3") #default value

LabelLength = tk.Label(GUI,text="Length [mm]: ")
EntryLength = tk.Entry(GUI)
EntryLength.insert(0,"6") #default value

LabelThread = tk.Label(GUI,text="Thread [mm]: ")
EntryThread = tk.Entry(GUI)
EntryThread.insert(0,"0.5") #default value

LabelCurve = tk.Label(GUI,text="Curve [mm]: ")
EntryCurve = tk.Entry(GUI)
EntryCurve.insert(0,"0.5") #default value

LabelThickness = tk.Label(GUI,text="Thickness [mm]: ")
EntryThickness = tk.Entry(GUI)
EntryThickness.insert(0,"0.2") #default value

LabelCut = tk.Label(GUI,text="Cut [mm]: ")
EntryCut = tk.Entry(GUI)
EntryCut.insert(0,"2") #default value


ButtonGenerateGeometry = tk.Button(GUI, text ="Generate geometry", command = generateGeometry)

ButtonCloseWindow = tk.Button(GUI, text ="Close", command = closeWindow)

#///////////////////////////////////////////////////////////////////////
#Place UI elements

i=1 #index for row number
k=1 #index for column number

LabelDiameter.grid(row=i,column=k)
EntryDiameter.grid(row=i,column=k+1)
i=i+1

LabelPitchTop.grid(row=i,column=k)
EntryPitchTop.grid(row=i,column=k+1)
i=i+1

LabelPitchBottom.grid(row=i,column=k)
EntryPitchBottom.grid(row=i,column=k+1)
i=i+1

LabelLength.grid(row=i,column=k)
EntryLength.grid(row=i,column=k+1)
i=i+1

LabelThread.grid(row=i,column=k)
EntryThread.grid(row=i,column=k+1)
i=i+1

LabelCurve.grid(row=i,column=k)
EntryCurve.grid(row=i,column=k+1)
i=i+1

LabelThickness.grid(row=i,column=k)
EntryThickness.grid(row=i,column=k+1)
i=i+1

LabelCut.grid(row=i,column=k)
EntryCut.grid(row=i,column=k+1)
i=i+1

ButtonGenerateGeometry.grid(row=i,column=k)

i=i+1

ButtonCloseWindow.grid(row=i,column=k)



#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()

