import os
import math
import statistics

def setRotationalSpeed(rotationalSpeed): #Function to set the rotational speed of the swimmer
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new omega value ...")
	textFile=open("constant/dynamicMeshDict","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'omega' in line:
			line="omega {};".format(2*math.pi*float(rotationalSpeed))
			changeMade=True
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("constant/dynamicMeshDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New omega value set")
	else :
		print("ERROR: Could not set new omega value")
		
def setForwardVelcoity(forwardVelocity): #Function to set the forward velocity of the swimmer
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new forward velocity ...")
	textFile=open("0/U","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'swimmerVelocity' in line and not(changeMade):
			line="swimmerVelocity -{};".format(forwardVelocity)
			changeMade=True
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("0/U","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New forward velocity value set")
	else :
		print("ERROR: Could not set new forward velocity")
	
def setMaxCourantNumber(maxCo): #Function to set the max courant number of the simulation
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new max courant number ...")
	textFile=open("system/controlDict","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'maxCo' in line:
			line="maxCo {};".format(maxCo)
			changeMade=True
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("system/controlDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New courant number set")
	else :
		print("ERROR: Could not set new courant number")
		
def setTimeMax(Tmax): #Function to set the max simulation time
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new simulation time ...")
	textFile=open("system/controlDict","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'endTime' in line:
			line="endTime         {};".format(Tmax)
			changeMade=True
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("system/controlDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New simulation end time set")
	else :
		print("ERROR: Could not set new simulation end time")
		
def setSwimmerRefinment(refinmentLevel): #funtion to set the swimmer surface refinment level
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new swimmer refinment level ...")
	textFile=open("system/snappyHexMeshDict","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'swimmmerBourdaryRefinmentLevel' in line and not(changeMade):
			line="swimmmerBourdaryRefinmentLevel {};".format(refinmentLevel)
			changeMade=True
			
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("system/snappyHexMeshDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New swimmer refinment level set")
	else :
		print("ERROR: Could not set new swimmer refinment level")
		
def setRotatingDomainRefinment(refinmentLevel): #function to set the rotating domain refinment level
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new rotating domain refinment level ...")
	textFile=open("system/snappyHexMeshDict","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'RotatingDomainRefinmentLevel' in line and not(changeMade):
			line="RotatingDomainRefinmentLevel {};".format(refinmentLevel)
			changeMade=True
			
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("system/snappyHexMeshDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New rotating domain refinment level set")
	else :
		print("ERROR: Could not set new rotating domain refinment level")
		
def getForce(): #funtion to calculate the force from the result data file
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	forceFile=open('postprocessing/forces/0/forces.dat')
	processedForceFile=""
	
	#remove parenthesis from file
	textOut=[]
	for line in forceFile:
		lineOut=""
		for ch in line:
			if not(ch=="(" or ch==")"):
				lineOut=lineOut+ch
		textOut.append(lineOut)
	
	forceTorqueData=[]
	for line in textOut:
		forceTorqueData.append(line.split())
		
	i=0
	forceSteadyState=[] #list to store the force computed in the last time steps
	for line in forceTorqueData:
		if i>len(forceTorqueData)-10:
			pressureForceY=float(forceTorqueData[i][2])
			viscousForceY=float(forceTorqueData[i][5])
			forceY=pressureForceY+viscousForceY
			forceSteadyState.append(forceY)
		i=i+1
	averageForceY=statistics.mean(forceSteadyState)
	stDevForceY=statistics.pstdev(forceSteadyState)
	print("Force={} N".format(averageForceY))
	return([averageForceY,stDevForceY])
	
def cleanCase(): #function to remove all temporary files generated bu OpenFoam
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	cmd = "./Allclean"
	os.system(cmd)
	
def setOuterCylinderSize(diameter,length): #function to set the size of the outer boundary cylinder
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new outer cylinder size ...")
	textFile=open("constant/geometry/propeller-outerCylinderRef.obj","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'v' in line:
			if '#' in line:
				a=1 
			else:
				#extract point poisition
				pointPositionString=""
				for ch in line:
					if not(ch=="v"):
						pointPositionString=pointPositionString+ch
				pointPositionX=diameter*float(pointPositionString.split()[0])/(0.015)
				pointPositionY=length*float(pointPositionString.split()[1])/(0.022)
				pointPositionZ=diameter*float(pointPositionString.split()[2])/(0.015)
				
				line="v {} {} {}".format(pointPositionX,pointPositionY,pointPositionZ)
						
				changeMade=True
				
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("constant/geometry/propeller-outerCylinder.obj","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New outer cylinder size set")
	else :
		print("ERROR: Could not set new outer cylinder size")
		
def setInnerCylinderSize(diameter,length): #function to set the size of the inner boundary cylinder
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Setting new inner cylinder size ...")
	textFile=open("constant/geometry/propeller-innerCylinderRef.obj","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'v' in line:
			if '#' in line:
				a=1 
			else:
				#extract point poisition
				pointPositionString=""
				for ch in line:
					if not(ch=="v"):
						pointPositionString=pointPositionString+ch
				pointPositionX=diameter*float(pointPositionString.split()[0])/(0.004)
				pointPositionY=length*float(pointPositionString.split()[1])/(0.008)
				pointPositionZ=diameter*float(pointPositionString.split()[2])/(0.004)
				
				line="v {} {} {}".format(pointPositionX,pointPositionY,pointPositionZ)
						
				changeMade=True
				
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("constant/geometry/propeller-innerCylinder.obj","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New inner cylinder size set")
	else :
		print("ERROR: Could not set new inner cylinder size")
		
def setBlockMesh(blockSize,maxElementSize): #function to configure blockMesh (initial Mesh size and density)
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	changeMade=False
	print("Configuring blockMesh...")
	textFile=open("system/blockMeshDictRef","r")
	newTextFile=""
	for line in textFile:
		line=line.strip()
		if 'vertice1' in line:
			line="(-{} -{} -{})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if 'vertice2' in line:
			line="({} -{} -{})".format(blockSize,blockSize,blockSize)
			changeMade=True

		if 'vertice3' in line:
			line="({} {} -{})".format(blockSize,blockSize,blockSize)
			changeMade=True

		if 'vertice4' in line:
			line="(-{} {} -{})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if 'vertice5' in line:
			line="(-{} -{}  {})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if 'vertice6' in line:
			line="({} -{} {})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if 'vertice7' in line:
			line="({} {} {})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if 'vertice8' in line:
			line="(-{} {} {})".format(blockSize,blockSize,blockSize)
			changeMade=True
			
		if '//blocks' in line:
			nbElements=math.ceil(2*blockSize/maxElementSize)
			line="    hex (0 1 2 3 4 5 6 7) ({} {} {}) simpleGrading (1 1 1)".format(int(nbElements),int(nbElements),int(nbElements))
			changeMade=True
				
		newTextFile=newTextFile + line + "\n"
	textFile.close()	
	textOut=open("system/blockMeshDict","w")
	textOut.write(newTextFile)
	textOut.close()
	if changeMade:
		print("New outer cylinder size set")
	else :
		print("ERROR: Could not set new outer cylinder size")
	
def runCase(): #funtion to start computing the case (Mesh+compute)
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	cmd = "./Allrun"
	os.system(cmd)
