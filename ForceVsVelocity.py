import CFDFunctions as cfd
f=50
Velocity=[0,0.01,0.02,0.03] #rotational speeds to compute

forceResults=[]

for v in Velocity:
	cfd.cleanCase()
	cfd.setRotationalSpeed(f)
	cfd.setForwardVelcoity(v)
	cfd.runCase()
	forceResults.append(cfd.getForce())

print("Velcity:")
print(Velocity)
print("PropulsiveForce")
print(forceResults)
