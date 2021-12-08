import CFDFunctions as cfd
import os
import time

#///////////////////////////////////////////////////////////////////////
#example python program that show how to use CFDFunctions
#to programatically control swimmer simulations via OpenFoam



#///////////////////////////////////////////////////////////////////////
#BEGIN: create variables with simulations settings
#///////////////////////////////////////////////////////////////////////
frequencyVector=[20,40,60,80,20,40,60,80,20,40,60,80] #create a list that contains the rotational frequencies to simulate
ForwardVelocity=[0.0,0.0,0.0,0.0,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04] #[m/s]
MaxCourantNumber=2 #[m/s]
SwimmerRefinment=2
RotatingDomainRefinment=1
OuterCylinderDiameter=15E-3 #[m]
OuterCylinderLength=22E-3 #[m]
InnerCylinderDiameter=5E-3 #[m]
InnerCylinderLength=12E-3 #[m]
MinCellLength=1E-3 #[m]
MaxSimulationTime=3 #[s]
#///////////////////////////////////////////////////////////////////////
#END: create variables to store simulations settings
#///////////////////////////////////////////////////////////////////////

#Check if a results file exist
script_path = os.path.dirname(os.path.realpath(__file__))
try:
	os.chdir(script_path)
	ResultsFile=open("scriptResults.txt","r")
	print("Results file found. Continuing computation...")
	time.sleep(2)
except:
	print("No results file found. Starting computation from begining..")
	time.sleep(2)
	#if no result file exist create list to store results and set iteration number to 0
	i=0
	forceResults=[] #list to store the force results
	stvResults=[] #list to store the standard devition results
	computationTimeResults=[]


while True: #begin the loop that starts each simulation
	
	#///////////////////////////////////////////////////////////////////
	#BEGIN: load data from text file if it exists
	#///////////////////////////////////////////////////////////////////
	try:
		os.chdir(script_path)
		ResultsFile=open("scriptResults.txt","r")
		for line in ResultsFile:
			if "iteration" in line:
				iteration=int(line.split()[1])
				i=iteration
			if "frequency" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				frequencyVector=[]
				for k in range(0,listLength):
					frequencyVector.append(float(lineList[k+1]))
			if "force" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				forceResults=[]
				for k in range(0,listLength):
					forceResults.append(float(lineList[k+1]))
			if "stDev" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				stvResults=[]
				for k in range(0,listLength):
					stvResults.append(float(lineList[k+1]))
	except:
		pass #do nothing if no data file exists		
	#///////////////////////////////////////////////////////////////////
	#END: load data from text file if it exists
	#//////////////////////////////////////////////////////////////////
						
		
	if i>len(frequencyVector)-1:
		break #Break loop if computation is complete
	
	else: #otherwise continue computation
		
			
		#///////////////////////////////////////////////////////////////////
		#BEGIN: clean and configure case
		#///////////////////////////////////////////////////////////////////	
		cfd.cleanCase() #remove all previously computed data
		#configure some simulation parameters
			#Note: these parameters are set at each iterations to ensure
			#that the correct parameters are used even is the simulation
			#was stopped, the files modified and then the simulation 
			#restarted
		cfd.setRotationalSpeed(frequencyVector[i])  #rotational frequency changes at each simulation
		cfd.setForwardVelcoity(ForwardVelocity[i]) 
		cfd.setMaxCourantNumber(MaxCourantNumber)
		cfd.setSwimmerRefinment(SwimmerRefinment)
		cfd.setRotatingDomainRefinment(RotatingDomainRefinment)
		cfd.setOuterCylinderSize(OuterCylinderDiameter,OuterCylinderLength)
		cfd.setInnerCylinderSize(InnerCylinderDiameter,InnerCylinderLength)
		#configure initial mesh
			#blockmesh creates the initial mesh
			#a cube of cell is created and it needs to contain all the geometry
		cfd.setBlockMesh(max(OuterCylinderDiameter*0.501,OuterCylinderLength*0.501),MinCellLength )#setBlockMesh(cubeSideLEngth,maxElementSize)
		#///////////////////////////////////////////////////////////////////
		#END: clean and configure case
		#///////////////////////////////////////////////////////////////////	
		
		averagedTimeWindow=1/(4*frequencyVector[i])
		if averagedTimeWindow<0.001:
			averagedTimeWindow=0.001 #minimum time averge window of 1ms
		
		startTime=time.time()
		
		solutionConverged=cfd.runCaseUntilStable(4,averagedTimeWindow,1,MaxSimulationTime)
		
		endTime=time.time()
		
		if solutionConverged:
			results=cfd.getForce()
			averageForceList=results[0]
			sDevForceList=results[1]
		
			forceResults.append(averageForceList[len(averageForceList)-1]) #store force result in list
			stvResults.append(sDevForceList[len(averageForceList)-1]) #store standard deviation result in list
			computationTimeResults.append(endTime-startTime) #store computation duration in list
			
		else:
			forceResults.append(0) #store force result in list
			stvResults.append(0) #store standard deviation result in list
			computationTimeResults.append(endTime-startTime) #store computation duration in list

		#///////////////////////////////////////////////////////////////
		#BEGIN: Save results in text file
		#///////////////////////////////////////////////////////////////
		os.chdir(script_path)
		line1="next_iteration {}".format(i+1)
		line2="frequency {}".format(" ".join(str(e) for e in frequencyVector))
		line3="forwardVelocity {}".format(" ".join(str(e) for e in ForwardVelocity))
		line4="force {}".format(" ".join(str(e) for e in forceResults))
		line5="stDev {}".format(" ".join(str(e) for e in stvResults))
		line6="computationTime {}".format(" ".join(str(e) for e in computationTimeResults))
		
		newTextFile=line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5+"\n"+line6
		textOut=open("scriptResults.txt","w")
		textOut.write(newTextFile)
		textOut.close()
		#///////////////////////////////////////////////////////////////
		#END: Save results in text file
		#///////////////////////////////////////////////////////////////
		
#print results after all computations are done
print("PropulsiveForce")
print(forceResults)
print("Standard Deviation")
print(stvResults)
