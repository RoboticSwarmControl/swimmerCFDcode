import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import sys
import os
import time


#This script create a .obj file of a custom swimmer with the correct format for use in OpenFoam. The swimmer geometry is generated using FreeCAD.

#This script is divided into three main parts:
#PART 2: create a function that process and format the .obj file
#PART 3: Python code that uses FreeCAD to generate a custom swimmer

#//////////////////////////////////////////////////////////////////////
#BEGIN PART 2: create a function that process and format the .obj file
#/////////////////////////////////////////////////////////////////////
def processObjFile(plot): #funtion to correctly format the obj file before sending to openFoam
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

def createGeometry(Diam,Ptch1,Ptch2,Length,Thread,Curve, Thickness, Cut):
	
	#modify the size of the swimmer in the python file
	print("Configuring geometry...")
	
	#change folder
	
	os.chdir('..')
	textFile=open("SwimmerGeometryGeneration/GeometryGenerationFreeCADPython2.py","r")
	newTextFile=""
	
	changeMade=False
	for line in textFile:
		line=line.strip()
		if 'Diam=' in line:
			line="Diam={}".format(Diam)
			changeMade=True
			
		if 'Ptch1=' in line:
			line="Ptch1={}".format(Ptch1)
			changeMade=True

		if 'Ptch2=' in line:
			line="Ptch2={}".format(Ptch2)
			changeMade=True

		if 'Length=' in line:
			line="Length={}".format(Length)
			changeMade=True
			
		if 'Thread=' in line:
			line="Thread={}".format(Thread)
			changeMade=True
			
		if 'Curve=' in line:
			line="Curve={}".format(Curve)
			changeMade=True
			
		if 'Thickness=' in line:
			line="Thickness={}".format(Thickness)
			changeMade=True
			
		if 'Cut=' in line:
			line="Cut={}".format(Cut)
			changeMade=True
						
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("SwimmerGeometryGeneration/GeometryGenerationFreeCADPython2.py","w")
	textOut.write(newTextFile)
	textOut.close()
		
	cmd = "freecad SwimmerGeometryGeneration/GeometryGenerationFreeCADPython2.py"
	os.system(cmd)
	processObjFile(False)


