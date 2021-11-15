import tkinter as tk
import os
import GeometryFunctions as GF

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
	GF.generateNewGeometry(float(EntryPitchTop.get()),float(EntryPitchTop.get()),float(EntryPitchBottom.get()),20,1.05,0.1,0.8,2.1824)
	
	
   
#///////////////////////////////////////////////////////////////////////
#Create UI elements

LabelDiameter = tk.Label(GUI,text="Diameter [mm]: ")
EntryDiameter = tk.Entry(GUI)
EntryDiameter.insert(0,"2.5") #default value

LabelPitchTop = tk.Label(GUI,text="Top pitch [mm]: ")
EntryPitchTop = tk.Entry(GUI)
EntryPitchTop.insert(0,"10") #default value

LabelPitchBottom = tk.Label(GUI,text="Bottom pitch [mm]: ")
EntryPitchBottom = tk.Entry(GUI)
EntryPitchBottom.insert(0,"10") #default value

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

ButtonGenerateGeometry.grid(row=i,column=k)

i=i+1

ButtonCloseWindow.grid(row=i,column=k)



#///////////////////////////////////////////////////////////////////////
#Start GUI
GUI.mainloop()

