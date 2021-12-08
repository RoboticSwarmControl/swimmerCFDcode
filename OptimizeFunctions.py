import os
import math
import sys
import statistics
import time
import numpy as np
import CFDFunctions as cfd
sys.path.append('SwimmerGeometryGeneration')
import GeometryFunctions as GF

try:
	import matplotlib.pyplot as plt
except:
	print("MatplotLib not installed, plots not avialable")
	
def ObjectiveFunction(ptch1,ptch2,startFreq,searchIntervalLength):
	
	Diam=2.5
	Length=6
	Thread=0.5
	Curve=0.5
	Thickness=0.4
	Cut=2
	
	Moment=0.000001
	Voltage=100
	Resistance=7
	Inductance=0.01
	FieldConstant=0.0005
	NbEM=2
	
	#create swimmer geometry
	cfd.cleanCase()
	GF.createGeometry(Diam,ptch1,ptch2,Length,Thread,Curve, Thickness, Cut)
	
	cfd.setForwardVelcoity(0)
	[rotationalFrequency,propulsiveForce]=cfd.searchStepOutFrequencyV2(Moment,Voltage,Resistance,Inductance,FieldConstant,NbEM,0.1,startFreq,5)
	return([rotationalFrequency,propulsiveForce])

def gradientDescent(ptch1Start,ptch2Start):

	learnRate=30000

	deltaPitch=0.5 #[mm]
	
	minPitch=1
	maxPitch=15
	
	ptch1=ptch1Start
	ptch2=ptch2Start
	
	startFrequency=50
	
	#create monitor file
	cfd.cleanCase()
	line1="monitorType gradientDescent"
	line2="Ptch1[mm],Ptch2[mm],Force[N],StepOutFrequency[Hz],Ptch1Gradient,Ptch2Gradient"
	newTextFile=line1+"\n"+line2+"\n"
	textOut=open("gradientDescent.monitor","w")
	textOut.write(newTextFile)
	textOut.close()
	
	while True:
		
		#compute new point value
		[stepOut,Force]=ObjectiveFunction(ptch1,ptch2,startFrequency,5)
		
		startFrequency=stepOut
		
		#calsulate gradient
		dPtch1=(Force-ObjectiveFunction(ptch1+deltaPitch,ptch2,startFrequency,1)[1])/deltaPitch
		dPtch2=(Force-ObjectiveFunction(ptch1,ptch2+deltaPitch,startFrequency,1)[1])/deltaPitch
		
		#save results
		#read monitor file
		monitorFile=open("gradientDescent.monitor","r")
		textOut=""
		for line in monitorFile:
			textOut=textOut+line
		
		#add data in file
		newLine="{},{},{},{},{},{}".format(ptch1,ptch2,Force,stepOut,dPtch1,dPtch2)
		textOut=textOut+newLine+"\n"
		
		#write monitor file
		oldText=open("gradientDescent.monitor","w")
		oldText.write(textOut)
		oldText.close()
		
		ptch1=ptch1-learnRate*dPtch1
		ptch2=ptch2-learnRate*dPtch2
		
		if ptch1>maxPitch:
			ptch1=maxPitch
			
		if ptch2>maxPitch:
			ptch2=maxPitch
			
		if ptch1<minPitch:
			ptch1=minPitch
			
		if ptch2<minPitch:
			ptch2=minPitch
