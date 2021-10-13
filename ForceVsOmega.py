import CFDFunctions as cfd

frequency=[20,40,60,80] #rotational speeds to compute

forceResults=[]

for f in frequency:
	cfd.cleanCase()
	cfd.setRotationalSpeed(f)
	cfd.runCase()
	forceResults.append(cfd.getForce())

print("Frequency:")
print(frequency)
print("PropulsiveForce")
print(forceResults)

