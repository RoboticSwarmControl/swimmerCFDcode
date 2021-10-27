import CFDFunctions as cfd
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
# To do: add timer
# plot with python's 'matplotlib': courant number vs force, time vs courant number plots
# change length of time simulation to 1 or 2 seconds
# incorporate plotting into the other functions

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
t=1 # Is this in units of seconds?

Courant=[0.5,0.8,1,5,10,20] # Max courant numbers to compute
forceResults=[]
run_time=[] # Store elapsed time as a vector
for Co in Courant:
	cfd.cleanCase()
	cfd.setTimeMax(t)
	cfd.setRotationalSpeed(Omega)
	cfd.setForwardVelcoity(0.001*Vel)
	cfd.setSwimmerRefinment(sr)
	cfd.setRotatingDomainRefinment(dr)
	cfd.setOuterCylinderSize((0.001*D),(0.001*L))
	cfd.setInnerCylinderSize((0.001*d),(0.001*l))
	cfd.setBlockMesh(max(D*(0.501/1000),L*(0.501/1000)),CL/1000) # setBlockMesh(blockSize,maxElementSize)
	cfd.setMaxCourantNumber(Co)

	start_time = time.time() # Start timer
	cfd.runCase()
	forceResults.append(cfd.getForce())
	end_time = time.time() # End timer after each loop
	run_time.append(end_time-start_time)

p=np.matrix(forceResults)# create a matrix of the force results
propulsive_force=p[:,0]

print("RunTime")
print(run_time)
print("MaxCourantNumber:")
print(Courant)
print("PropulsiveForce")
print(propulsive_force)
print("ForceResults")
print(forceResults)

# Plot force vs courant number
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(Courant, propulsive_force)  # Plot some data on the axes.
ax.set_title('Max Courant Number vs. Force')
ax.set_xlabel('Max Courant number')
ax.set_ylabel('Propulsive Force [N]')
ax.grid()
plt.show()
# Plot courant number vs time
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(Courant, run_time)  # Plot some data on the axes.
ax.set_title('Max Courant Number vs. Time')
ax.set_xlabel('Max Courant Number')
ax.set_ylabel('Time [s]')
ax.grid()
plt.show()
