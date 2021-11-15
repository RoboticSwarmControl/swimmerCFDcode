import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
FREECADPATH = '/lib/freecad/lib'
FREECADPATH = '/usr/lib/freecad-python3/lib'
import sys
sys.path.append(FREECADPATH)
import FreeCAD
import FreeCADGui
App=FreeCAD
import time

#This script create a .obj file of a custom swimmer with the correct format for use in OpenFoam. The swimmer geometry is generated using FreeCAD.

#This script is divided into three main parts:
#PART 2: create a function that process and format the .obj file
#PART 3: Python code that uses FreeCAD to generate a custom swimmer

#//////////////////////////////////////////////////////////////////////
#BEGIN PART 2: create a function that process and format the .obj file
#/////////////////////////////////////////////////////////////////////
def processObjFile(): #funtion to correctly format the obj file before sending to openFoam
	#generate a plot if plot==True

	def frustum(left, right, bottom, top, znear, zfar):
		M = np.zeros((4, 4), dtype=np.float32)
		M[0, 0] = +2.0 * znear / (right - left)
		M[1, 1] = +2.0 * znear / (top - bottom)
		M[2, 2] = -(zfar + znear) / (zfar - znear)
		M[0, 2] = (right + left) / (right - left)
		M[2, 1] = (top + bottom) / (top - bottom)
		M[2, 3] = -2.0 * znear * zfar / (zfar - znear)
		M[3, 2] = -1.0
		return M

	def perspective(fovy, aspect, znear, zfar):
		h = np.tan(0.5*np.radians(fovy)) * znear
		w = h * aspect
		return frustum(-w, w, -h, h, znear, zfar)
	def translate(x, y, z):
		return np.array([[1, 0, 0, x],
		[0, 1, 0, y],
		[0, 0, 1, z],
		[0, 0, 0, 1]], dtype=float)

	def xrotate(theta):
		t = np.pi * theta / 180
		c, s = np.cos(t), np.sin(t)
		return np.array([[1, 0,  0, 0],
		[0, c, -s, 0],
		[0, s,  c, 0],
		[0, 0,  0, 1]], dtype=float)

	def yrotate(theta):
		t = np.pi * theta / 180
		c, s = np.cos(t), np.sin(t)
		return  np.array([[ c, 0, s, 0],
		[ 0, 1, 0, 0],
		[-s, 0, c, 0],
		[ 0, 0, 0, 1]], dtype=float)

	ObjFileOut="g propellerStem \n"
	# Data processing
	V, F = [], []
	fileData=open("SwimmerGeometryGeneration/propeller.obj","r")
	with fileData as f:
		for line in f.readlines():
			if line.startswith('#'):
				continue
			values = line.split()
			if not values:
				continue
			if values[0] == 'v':
				V.append([0.001*float(x) for x in values[1:4]])
				newLine="v {} {} {}".format(0.001*float(values[1]),0.001*float(values[3])-0.003,-0.001*float(values[2]))
				ObjFileOut=ObjFileOut+newLine+"\n"
			elif values[0] == 'f' :
				numbers=[]
				for x in values[1:4]:
					number=""
					for char in x:
						if char=='/':
							break
						else:
							number=number+char

					numbers.append(int(number))

				F.append(numbers)
				newLine="f {} {} {}".format(numbers[0],numbers[1],numbers[2])
				ObjFileOut=ObjFileOut+newLine+"\n"
		fileData.close()
	fileOut=open("OpenFoamFiles/constant/geometry/propeller.obj","w")
	fileOut.write(ObjFileOut)
	fileOut.close()
	plot=True
	if plot:
		V, F = np.array(V), np.array(F)-1

		V = (V-(V.max(0)+V.min(0))/2) / max(V.max(0)-V.min(0))

		model = xrotate(20) @ yrotate(45) 
		view  = translate(0,0,-3.5)
		proj  = perspective(25, 1, 1, 100) 
		MVP   = proj  @ view  @ model 

		V = np.c_[V, np.ones(len(V))]  @ MVP.T
		V /= V[:,3].reshape(-1,1)
		V = V[F]

		T =  V[:,:,:2]
		Z = -V[:,:,2].mean(axis=1)
		I = np.argsort(Z)
		T = T[I,:]

		# Rendering
		fig = plt.figure(figsize=(6,6))
		ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1, frameon=False)
		collection = PolyCollection(T, closed=True, linewidth=0.1,
		facecolor="0.9", edgecolor="black")
		ax.add_collection(collection)
		#plt.savefig("bunny-7.png", dpi=300)
		plt.show()
		
#//////////////////////////////////////////////////////////////////////
#END PART 2: create a function that process and format the .obj file
#/////////////////////////////////////////////////////////////////////





#//////////////////////////////////////////////////////////////////////
#BEGIN  PART 3: Python code that uses FreeCAD to generate a custom swimmer
#/////////////////////////////////////////////////////////////////////
"""
Created on Tue Oct  6 04:08:36 2020
@author: Joclyn Ramos
"""
# This script edits thread depth and pitch of a swimmer geometry from a premade 
# file (SwimmerModel7.FCStd), from user input. Certain dimensions combinations that are 
# not physically possible may produce errors, but rerunning with SwimmerModel7 
# dimensions should fix it. 

# Save each design iteration as a new file and export as a new stl file, so 
# edits can be made from the original file without overwriting with a
# backup of any errors.

# BEFORE RUNNING (if running from the python console): Import the file path by copy pasting below code, 
# then call a script by typing 'import scriptname' into the python console 

# Example parameters within SwimmerModel7 range:
# Enter model diameter: 2.5
# Enter thread depth: 0.6
# Enter base pitch: 2
# Enter tip pitch: 4
# Enter tip curvature (value between 0.01 and cylinder radius): 0.3
# Enter total length: 6.5
# Total radius is: 1.25

# Which returns...

# Cylinder radius is: 0.65
# Thread depth is: 0.6
# Base pitch is: 2
# Tip pitch is: 4
# Total length is: 6.5




def generateNewGeometry(Diam,Ptch1,Ptch2,Length,Thread,Curve, Thickness, Cut):

	#Example:
	# Diam=2.5;
	# Ptch1= 10;
	# Ptch2=10;
	# Length=6;
	# Thread=1.05;
	# Curve=0.1;
	# Thickness=0.8;
	# Cut=2.1824;
	print(Length)
	time.sleep(10)

	ExportObjPath=u"SwimmerGeometryGeneration/propeller.obj";
	# Space=input("Enter spacing between tip pitch and base pitch: ");
	# Spacing between pitches isn't a defined parameter atm
	# Tip cut angle could also be a variable with width if needed

	A=Diam; # convert from string
	Rad=(A/2) # total radius

	B=Thread;
	Rad2=Rad-B; #cylinder radius (model radius - thread depth) = (1.25 - thread depth)

	FreeCAD.open(u"SwimmerGeometryGeneration/SwimmerModel7.FCStd")
	App.setActiveDocument("SwimmerModel7")
	App.ActiveDocument=App.getDocument("SwimmerModel7")
	#FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SwimmerModel7")

	# Edit thread depth (cylinder radius)
	FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Radius = Rad2

	# Changing angle of bottom pitch to align with top pitch (if we change vertical placement of threads, adjust this)
	R=360*(1-4/Ptch1)
	FreeCAD.getDocument("SwimmerModel7").getObject("Sweep").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),R))
	App.activeDocument().recompute()

	# Editing pitch

	FreeCAD.getDocument("SwimmerModel7").getObject("Helix").Pitch = Ptch1
	App.activeDocument().recompute()
	FreeCAD.getDocument("SwimmerModel7").getObject("Helix001").Pitch = Ptch2
	App.activeDocument().recompute()
	FreeCAD.getDocument("SwimmerModel7").getObject("Helix002").Pitch = Ptch2
	App.activeDocument().recompute()
	#
	#FreeCAD.getDocument("SwimmerModel7").getObject("Helix001").Pitch = 2

	# Thread thickness
	#----------

	T=(Thickness-0.2)
	App.ActiveDocument.Sketch001.setDatum(11,App.Units.Quantity(4.100000+(T/2)))
	App.ActiveDocument.Sketch001.setDatum(9,App.Units.Quantity(3.900000-(T/2)))
	App.ActiveDocument.Sketch.setDatum(11,App.Units.Quantity(0.100000+(T/2)))
	App.ActiveDocument.Sketch.setDatum(9,App.Units.Quantity(-1*(0.100000+(T/2))))
	App.ActiveDocument.Sketch002.setDatum(9,App.Units.Quantity(4.100000+(T/2)))
	App.ActiveDocument.Sketch002.setDatum(11,App.Units.Quantity(3.900000-(T/2)))
	#-------
	# Change total radius

	App.ActiveDocument.Sketch002.setDatum(8,App.Units.Quantity(-Rad))
	App.ActiveDocument.Sketch001.setDatum(10,App.Units.Quantity(Rad))
	App.ActiveDocument.Sketch.setDatum(10,App.Units.Quantity(Rad))

	# Changing tip curvature (fillet radius)

	__fillets__ = []
	__fillets__.append((1,Curve,Curve))
	FreeCAD.ActiveDocument.Fillet.Edges = __fillets__
	del __fillets__
	#FreeCADGui.ActiveDocument.Cylinder.Visibility = False

	# Changing length adds to the end length (should we also add space between tip and base pitches?)

	L=6-Length
	FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,0,1),0))
	FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Height = Length
	#FreeCAD.getDocument("SwimmerModel7").getObject("Sketch003").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(1,0,0),90))
	FreeCAD.getDocument("SwimmerModel7").getObject("Box").Placement = App.Placement(App.Vector(-2,-2,(-6+L)),App.Rotation(App.Vector(0,0,1),0))

	# Last trims (tip cut angle can also be made variable)

	Crve=Curve;
	X=Rad2-Crve
	Y=Length-Crve-0.01
	Z=Crve+0.2

	#App.ActiveDocument.Sketch003.setDatum(16,App.Units.Quantity(Rad+0.01))
	#App.ActiveDocument.Sketch003.setDatum(15,App.Units.Quantity(Crve))
	#App.ActiveDocument.Sketch003.setDatum(11,App.Units.Quantity(Z))
	#App.ActiveDocument.Sketch003.setDatum(13,App.Units.Quantity(X))
	#App.ActiveDocument.Sketch003.setDatum(17,App.Units.Quantity(X))
	#App.ActiveDocument.Sketch003.setDatum(14,App.Units.Quantity(Y))

	Web=0.05 # This is the amount of spacing at the tip for dulling the point.
	#App.ActiveDocument.Sketch003.setDatum(6,App.Units.Quantity('6.010000 mm')) # height + 0.01

	App.ActiveDocument.Sketch003.setDatum(5,App.Units.Quantity(0.01+Web)) # web
	App.ActiveDocument.Sketch003.setDatum(7,App.Units.Quantity(6.01-Cut)) # angle via height of triangle base
	#----------

	# In order to add spacing btwn tip and base pitches... (Not using this atm)

	#S=float(Space)
	#FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,0,1),0))
	#FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Height = Length
	#App.getDocument("SwimmerModel7").Sweep.Placement=App.Placement(App.Vector(0,0,-S), App.Rotation(App.Vector(0,0,1),0), App.Vector(0,0,0))

	#Change bottom cut to have the same angle for any parameters (Radius and diameter of total swimmer being constant) 
	App.ActiveDocument.Sketch004.setDatum(5,App.Units.Quantity(-Rad2))

	App.activeDocument().recompute()

	# The original file is named 'SwimmerModel7')
	# To save changes to the file itself:  App.getDocument("BasicSwimmerAttempt").save()

	# Make sure this saves to a new name for each design, to avoid overwriting with 
	# a backup of any errors.
	#App.getDocument("SwimmerModel7").saveAs(u"C:/Users/Joclyn Ramos/Desktop/UHWork/2020 Fall/Milliswimmers/FreeCAD/SwimmerModel7.FCStd")

	# Save as an stl

	#__objs__=[]
	#__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut001"))
	#import Mesh
	#Mesh.export(__objs__,ExportOBJPath)
	#Mesh.export(__objs__,ExportSTLPath)
	#del __objs__

	#__objs__=[]
	#__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut001"))
	#import Mesh
	#Mesh.export(__objs__,ExportOBJPath)
	#Mesh.export(__objs__,ExportSTLPath)
	#del __objs__

	#del __doc__, __mesh__, __part__, __shape__

	#import ObjectsFem
	#ObjectsFem.makeMeshNetgen(FreeCAD.ActiveDocument, 'FEMMeshNetgen')
	#FreeCAD.ActiveDocument.ActiveObject.Shape = FreeCAD.ActiveDocument.Cut001
	#FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)
	#import femmesh.femmesh2mesh
	#out_mesh = femmesh.femmesh2mesh.femmesh_2_mesh(FreeCAD.ActiveDocument.FEMMeshNetgen.FemMesh)
	#import Mesh
	#Mesh.Mesh(out_mesh)
	#FreeCAD.ActiveDocument.FEMMeshNetgen.ViewObject.hide()

	# __objs__=[]
	# __objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut003"))
	# import Part
	# Part.export(__objs__,ExportBrepPath) 
	# del __objs__

	#del __objs__
	#import Gui
	#Gui.SendMsgToActiveView("SaveAs")
	__objs__=[]
	__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut003"))
	import Mesh
	Mesh.export(__objs__,ExportObjPath)
	del __objs__
	App.closeDocument("SwimmerModel7")
	#//////////////////////////////////////////////////////////////////////
	#END PART 3: Python code that uses FreeCAD to generate a custom swimmer
	#/////////////////////////////////////////////////////////////////////

	processObjFile()
