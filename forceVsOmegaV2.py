import CFDFunctions as cfd

frequencyVector=[20,40,60]

ForwardVelocity=0 #[m/s]
MaxCourantNumber=5 #[m/s]
SwimmerRefinment=2
RotatingDomainRefinment=1
OuterCylinderDiameter=15E-3
OuterCylinderLength=22E-3
InnerCylinderDiameter=5E-3
InnerCylinderLength=12E-3
MinCellLength=0.5E-3

simulationTime=0.01


forceResults=[]
stvResults=[]

i=0
while True:
	
	if i>len(frequencyVector)-1:
		break
	else:
		cfd.cleanCase()

		cfd.setRotationalSpeed(frequencyVector[i])
		cfd.setForwardVelcoity(ForwardVelocity)
		cfd.setMaxCourantNumber(MaxCourantNumber)
		cfd.setSwimmerRefinment(SwimmerRefinment)
		cfd.setRotatingDomainRefinment(RotatingDomainRefinment)
		cfd.setOuterCylinderSize(OuterCylinderDiameter,OuterCylinderLength)
		cfd.setInnerCylinderSize(InnerCylinderDiameter,InnerCylinderLength)
		
		cfd.setBlockMesh(max(OuterCylinderDiameter*0.501,OuterCylinderLength*0.501),MinCellLength )#blockmesh creates the initial mesh - setBlockMesh(blockSize,maxElementSize)
		
		cfd.setTimeMax(simulationTime)
		
		
		cfd.runCase()
		forceResults.append(cfd.getForce()[0])
		stvResults.append(cfd.getForce()[1])
		i=i+1
		
		#Save results in text file
		line1="next_iteration {}".format(i)
		line2="frequency {}".format(frequencyVector)
		line3="force {}".format(forceResults)
		line4="stDev {}".format(stvResults)
		newTextFile=line1+"\n"+line2+"\n"+line3+"\n"+line4
		textOut=open("scriptResults.txt","w")
		textOut.write(newTextFile)
		textOut.close()

print("PropulsiveForce")
print(forceResults)
print("PropulsiveForce")
print(stvResults)
