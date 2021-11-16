import CFDFunctions as cfd
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
import os

#///////////////////////////////////////////////////////////////////////
#BEGIN: create variables with simulations settings
#///////////////////////////////////////////////////////////////////////

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
CL=0.0005 # Default max cell length
t=1 # time

#Variable being tested
velocityVector=[0,0.01,0.02,0.03,0.04,0.05] # Forward velocities

#///////////////////////////////////////////////////////////////////////
#END: create variables to store simulations settings
#///////////////////////////////////////////////////////////////////////

#Set up plots
fig, ax = plt.subplots(1,2)  # Create a figure containing a single axes.
ax[0].set_title('Forward Velocity vs. Force')
ax[0].set_xlabel('Forward Velocity [m/s]')
ax[0].set_ylabel('Propulsive Force [N]')
ax[0].grid()
ax[1].set_title('Forward Velocity vs. Time')
ax[1].set_xlabel('Forward Velocity [m/s]')
ax[1].set_ylabel('Time [s]')
ax[1].grid()

#Check if a results file exist
script_path = os.path.dirname(os.path.realpath(__file__))

try:
	os.chdir(script_path+'/Results')
	ResultsFile=open("scriptResults_forceVsVelocity.txt","r")
	print("Results file found. Continuing computation...")
	time.sleep(2)

except:
	print("No results file found. Starting computation from begining..")
	time.sleep(2)
	#if no result file exist create list to store results and set iteration number to 0
	i=0
	forceResults=[]
	stvResults=[]
	computationTimeResults=[] # Store elapsed time as a vector

while True: #begin the loop that starts each simulation
	
	#///////////////////////////////////////////////////////////////////
	#BEGIN: load data from text file if it exists
	#///////////////////////////////////////////////////////////////////
	try:
		os.chdir(script_path+'/Results')
		ResultsFile=open("scriptResults_forceVsVelocity.txt","r")
		for line in ResultsFile:
			if "iteration" in line:
				iteration=int(line.split()[1])
				i=iteration
			if "forwardVelocity" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				velocityVector=[]
				for k in range(0,listLength):
					velocityVector.append(float(lineList[k+1]))
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
			if "computationTime" in line:
				lineList=line.split()
				listLength=len(lineList)-1
				computationTimeResults=[]
				for k in range(0,listLength):
					computationTimeResults.append(float(lineList[k+1]))

	except:
		pass #do nothing if no data file exists		
	#///////////////////////////////////////////////////////////////////
	#END: load data from text file if it exists
	#//////////////////////////////////////////////////////////////////
						
		
	if i>len(velocityVector)-1:
		ax[0].scatter((velocityVector[0:len(forceResults)]), forceResults)  # Plot some data on the axes.
		ax[1].scatter((velocityVector[0:len(forceResults)]), computationTimeResults)  # Plot some data on the axes.
		fig.set_size_inches(10,5)
		plt.autoscale()
		fig.savefig('ForceVsVelocity.png',dpi=200)
		#fig.savefig(script_path+'/Results/ForceVsVelocity/ForceVsVelocity.png',dpi=200)
		plt.show()
		break #Break loop if computation is completety.

	else: #otherwise continue computation
		
		Vel=velocityVector[i]
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
		cfd.setBlockMesh(max((D*(0.501/1000)),(L*(0.501/1000))),CL) # setBlockMesh(blockSize,maxElementSize)
		cfd.setMaxCourantNumber(C)
		#configure initial mesh
			#blockmesh creates the initial mesh
			#a cube of cell is created and it needs to contain all the geometry
		#cfd.setBlockMesh(max(D*0.501,L*0.501),MinCellLength )#setBlockMesh(cubeSideLEngth,maxElementSize)
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
		computationTimeResults.append(endTime-startTime) #store computation duration in list		

		if solutionConverged:
			results=cfd.getForce()
			averageForceList=results[0]
			sDevForceList=results[1]
			forceResults.append(averageForceList[len(averageForceList)-1]) #store force result in list
			stvResults.append(sDevForceList[len(averageForceList)-1]) #store standard deviation result in list
			print('solution converged-----')
		else:
			forceResults.append(0) #store force result in list
			stvResults.append(0) #store standard deviation result in list

		#computationTimeResults.append(endTime-startTime) #store computation duration in list		
		#print(computationTimeResults)
		#///////////////////////////////////////////////////////////////
		#BEGIN: Save results in text file
		#///////////////////////////////////////////////////////////////
		os.chdir(script_path+'/Results')
		line1="next_iteration {}".format(i+1)
		line2="forwardVelocity {}".format(" ".join(str(e) for e in velocityVector))
		line3="force {}".format(" ".join(str(e) for e in forceResults))
		line4="stDev {}".format(" ".join(str(e) for e in stvResults))
		line5="computationTime {}".format(" ".join(str(e) for e in computationTimeResults))
		
		newTextFile=line1+"\n"+line2+"\n"+line3+"\n"+line4+"\n"+line5
		textOut=open("scriptResults_forceVsVelocity.txt","w")
		textOut.write(newTextFile)
		textOut.close()
		#///////////////////////////////////////////////////////////////
		#END: Save results in text file
		#///////////////////////////////////////////////////////////////

		#///////////////////////////////////////////////////////////////
		# Plot results with each finished iteration
		#///////////////////////////////////////////////////////////////
		ax[0].scatter((velocityVector[0:len(forceResults)]), forceResults)  # Plot some data on the axes.
		ax[1].scatter((velocityVector[0:len(forceResults)]), computationTimeResults)  # Plot some data on the axes.
		fig.set_size_inches(10,5)
		plt.autoscale()
		fig.savefig('ForceVsVelocity'+str(i)+'.png',dpi=200)
		plt.show()
