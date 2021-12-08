import os
import math
import statistics
import time

try:
	import matplotlib.pyplot as plt
except:
	print("MatplotLib not installed, plots not avialable")

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
	forceFolders=os.walk('postProcessing/forces')

	timeList=[]
	forceList=[]
	AvergedForceList=[]
	StVList=[]

	for folder in forceFolders:
		#open file
		try:
			forceFile=open("{}/forces.dat".format(folder[0]))
		except:
			continue
			
		#remove parenthesis from file
		textOut=[] #List that will contain all lines of the file
		for line in forceFile:
			lineOut=""
			for ch in line:
				if not(ch=="(" or ch==")"):
					lineOut=lineOut+ch
			textOut.append(lineOut)
			
		forceTorqueData=[] 
		for line in textOut:
			forceTorqueData.append(line.split()) #split data to get individual numbers. 2D data is stored in a list of lists
		
		#Calculate propulsive force: sum of viscous and pressure forces along Y axis
		index=0
		forceListLocal=[]
		
		for line in forceTorqueData:
			if index>2:
				pressureForceY=float(forceTorqueData[index][2])
				viscousForceY=float(forceTorqueData[index][5])
				forceY=pressureForceY+viscousForceY
				forceList.append(forceY)
				forceListLocal.append(forceY)
				timeList.append(forceTorqueData[index][0])
			index=index+1
			
		AvergedForceList.append(statistics.mean(forceListLocal))
		StVList.append(statistics.pstdev(forceListLocal))	

	return([AvergedForceList,StVList])
	
def getLastSimulationTime(): #funtion to get the last simulation time
	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	forceFile=open('postProcessing/forces/0/forces.dat')
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
	simTime=[] #list to store the force computed in the last time steps
	for line in forceTorqueData:
		if i>2 and float(forceTorqueData[i][0])>float(forceTorqueData[len(forceTorqueData)-1][0])-0.1: #get last 0.1s of the computation
			simTime.append(float(forceTorqueData[i][0]))
			
		i=i+1
	lastSimTime=simTime[len(simTime)-1]
	print("Last simulation time = {}".format(lastSimTime))
	return(lastSimTime)
	
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
	
def runCaseUntilStable(nAverageSamples,averagedTimeWindow,maxVariationPercent,maxSimulationTime): #funtion to start computing the case (Mesh+compute)
	plt.ion()
	fig,axis=plt.subplots(2)
	currentSimulationFinalTime=0;
	
	#compute the first nAverageSamples time slots
	for iteration in range(nAverageSamples):
		currentSimulationFinalTime=currentSimulationFinalTime+averagedTimeWindow
		setTimeMax(currentSimulationFinalTime)
	
		#compute
		if iteration==0:
			cmd = "./Allrun"
		else:
			cmd = "pimpleFoam"
		os.system(cmd)

		axis[0].clear()
		plotForce(axis[0],'All')
		axis[1].clear()
		plotForce(axis[1],'Last')
		plt.show()
		plt.pause(0.001)
	
	#check if solution is stable
	Results=getForce()[0]
	print(Results)
	forceValuesToCheck=Results[len(Results)-nAverageSamples:len(Results)-1]
	print(forceValuesToCheck)
	solutionConverged=100*(max(forceValuesToCheck)-min(forceValuesToCheck))/(sum(forceValuesToCheck)/len(forceValuesToCheck))<maxVariationPercent


	while not(solutionConverged):  #continue until convergence
		
			print("Solution not stable, continuing computation...")
			iteration=iteration+1
			currentSimulationFinalTime=currentSimulationFinalTime+averagedTimeWindow
			setTimeMax(currentSimulationFinalTime)
			cmd = "pimpleFoam"
			os.system(cmd)
			
			#check if solution is stable
			Results=getForce()[0]
			forceValuesToCheck=Results[len(Results)-1-nAverageSamples:len(Results)-1]
			solutionConverged=100*(max(forceValuesToCheck)-min(forceValuesToCheck))/(sum(forceValuesToCheck)/len(forceValuesToCheck))<maxVariationPercent

			#plot force vs time
			axis[0].clear()
			plotForce(axis[0],'All')
			axis[1].clear()
			plotForce(axis[1],'Last')
			plt.show()
			plt.pause(0.001)
			
			if currentSimulationFinalTime>maxSimulationTime:
				break

	print("Stable, solution found")			
	plt.close()
	return(solutionConverged)

def plotForce(axis,length): #funtion to plot the force vs time

	file_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(file_path)
	os.chdir("OpenFoamFiles")
	forceFolders=os.walk('postProcessing/forces')

	timeList=[]
	forceList=[]
	AvergedForceList=[]
	StVList=[]

	for folder in forceFolders:
		#open file
		try:
			forceFile=open("{}/forces.dat".format(folder[0]))
		except:
			continue
			
		#remove parenthesis from file
		textOut=[] #List that will contain all lines of the file
		for line in forceFile:
			lineOut=""
			for ch in line:
				if not(ch=="(" or ch==")"):
					lineOut=lineOut+ch
			textOut.append(lineOut)
			
		forceTorqueData=[] 
		for line in textOut:
			forceTorqueData.append(line.split()) #split data to get individual numbers. 2D data is stored in a list of lists
		
		#Calculate propulsive force: sum of viscous and pressure forces along Y axis
		index=0
		forceListLocal=[]
		timeListLocal=[]
		
		for line in forceTorqueData:
			if index>2:
				pressureForceY=float(forceTorqueData[index][2])
				viscousForceY=float(forceTorqueData[index][5])
				forceY=pressureForceY+viscousForceY
				forceList.append(forceY)
				forceListLocal.append(forceY)
				timeList.append(forceTorqueData[index][0])
				timeListLocal.append(forceTorqueData[index][0])
			index=index+1
			
		AvergedForceList.append(statistics.mean(forceListLocal))
		StVList.append(statistics.pstdev(forceListLocal))
	if length=='All':
		axis.plot(timeList,forceList)
	if length=='Last':
		axis.plot(timeListLocal,forceListLocal)		
