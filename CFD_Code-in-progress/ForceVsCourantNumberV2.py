import CFDFunctions as cfd
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
import os

#///////////////////////////////////////////////////////////////////////
#example python program that show how to use CFDFunctions
#to programatically control swimmer simulations via OpenFoam



#///////////////////////////////////////////////////////////////////////
#BEGIN: create variables with simulations settings
#///////////////////////////////////////////////////////////////////////
#frequencyVector=[20,40,60,80,20,40,60,80,20,40,60,80] #create a list that contains the rotational frequencies to simulate
#ForwardVelocity=[0.0,0.0,0.0,0.0,0.02,0.02,0.02,0.02,0.04,0.04,0.04,0.04] #[m/s]
#MaxCourantNumber=2 #[m/s]
#SwimmerRefinment=2
#RotatingDomainRefinment=1
#OuterCylinderDiameter=15E-3 #[m]
#OuterCylinderLength=22E-3 #[m]
#InnerCylinderDiameter=5E-3 #[m]
#InnerCylinderLength=12E-3 #[m]
MinCellLength=1E-3 #[m]
MaxSimulationTime=5 #[s]

D=15 # Default outer diameter
L=22 # Default outer Length
d=5 # Default inner diameter
l=12 # default inner length
C=5 # courant number
dr=1 # domain refinement
sr=2 # swimmer refinement
Omega=20 # Hz
Vel=0 # mm/s
CL=0.5 # Default max cell length


Courant=[0.5,0.8,1,5,10,20] # Max courant numbers to compute



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
	forceResults=[]
	run_time=[] # Store elapsed time as a vector


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
			if "courantNumber" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				Courant=[]
				for k in range(0,listLength):
					Courant.append(float(lineList[k+1]))
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
						
		
	if i>len(Courant)-1:
		break #Break loop if computation is complete
	
	else: #otherwise continue computation
		
		Co=Courant[i]
		#///////////////////////////////////////////////////////////////////
		#BEGIN: clean and configure case
		#///////////////////////////////////////////////////////////////////	
		cfd.cleanCase() #remove all previously computed data
		#configure some simulation parameters
			#Note: these parameters are set at each iterations to ensure
			#that the correct parameters are used even is the simulation
			#was stopped, the files modified and then the simulation 
			#restarted
		cfd.setRotationalSpeed(Omega)
		cfd.setForwardVelcoity(0.001*Vel)
		cfd.setSwimmerRefinment(sr)
		cfd.setRotatingDomainRefinment(dr)
		cfd.setOuterCylinderSize((0.001*D),(0.001*L))
		cfd.setInnerCylinderSize((0.001*d),(0.001*l))
		#cfd.setBlockMesh(max(D*(0.501/1000),L*(0.501/1000)),MinCellLength/1000) # setBlockMesh(blockSize,maxElementSize)
		cfd.setMaxCourantNumber(Co)
		#configure initial mesh
			#blockmesh creates the initial mesh
			#a cube of cell is created and it needs to contain all the geometry
		cfd.setBlockMesh(max(D*0.501,L*0.501),MinCellLength )#setBlockMesh(cubeSideLEngth,maxElementSize)
		#///////////////////////////////////////////////////////////////////
		#END: clean and configure case
		#///////////////////////////////////////////////////////////////////	
		
		averagedTimeWindow=1/(4*Omega)
		if averagedTimeWindow<0.001:
			averagedTimeWindow=0.001 #minimum time averge window of 1ms
		
		startTime=time.time()
		#MaxSimulationTime=5
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
		line2="courantNumber {}".format(" ".join(str(e) for e in Courant))
		line3="force {}".format(" ".join(str(e) for e in forceResults))
		line4="stDev {}".format(" ".join(str(e) for e in stvResults))
		line5="computationTime {}".format(" ".join(str(e) for e in computationTimeResults))
		
		newTextFile=line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5
		textOut=open("scriptResults.txt","w")
		textOut.write(newTextFile)
		textOut.close()
		#///////////////////////////////////////////////////////////////
		#END: Save results in text file
		#///////////////////////////////////////////////////////////////
		

# Plot force vs courant number
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(Courant, forceResults)  # Plot some data on the axes.
ax.set_title('Max Courant Number vs. Force')
ax.set_xlabel('Max Courant number')
ax.set_ylabel('Propulsive Force [N]')
ax.grid()
plt.show()
# Plot courant number vs time
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(Courant, computationTimeResults)  # Plot some data on the axes.
ax.set_title('Max Courant Number vs. Time')
ax.set_xlabel('Max Courant Number')
ax.set_ylabel('Time [s]')
ax.grid()
plt.show()
