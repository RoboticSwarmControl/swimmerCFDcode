import CFDFunctions as cfd
import os
import statistics
import time

#///////////////////////////////////////////////////////////////////////
#Swimmer properties
#/////////////////////////////////////////////////////////////////////
#1) Swimmer shell geometry: .obj file placed in geometry folder
#2) Magnet properties
magnetDiameter=0.75E-3 #[m]
magnetLength=1E-3 #[m]
magnetMagnetization=900E3 #[A/m]
magnetDensity=7.5
swimmerShellDensity=1.1 


#///////////////////////////////////////////////////////////////////////
#Magnetic manipulator properties
#/////////////////////////////////////////////////////////////////////
k=0.8E-3 #[T/A] coil constant, flux density produced at the center of the worspace by a current of 1A
L=0.195 #[H] inductance of the coils
R=27.3 #[ohms] resistance of the coils
V=100 #[V] max voltage


#///////////////////////////////////////////////////////////////////////
#Liquid properties
#/////////////////////////////////////////////////////////////////////
liquidDensity=1


#///////////////////////////////////////////////////////////////////////
#other
#///////////////////////////////////////////////////////////////////////
swimmerDisplacementVolume=9.611E-9 #[m^3] will be calculated with freecad in the future, displacement of the swimmer including magnet and pocket of air
swimmerAirPocketVolume=1E-9 #m^3
gravityAccel=9.81 #[m/s^2]


#///////////////////////////////////////////////////////////////////////
#calculate vertical static force
#///////////////////////////////////////////////////////////////////////
magnetVolume=3.14159*magnetDiameter*magnetDiameter*magnetLength/4 #[m^3]
magnetWeight=gravityAccel*1000*magnetDensity*magnetVolume #[N]
swimmerBuoyancy=1000*swimmerDisplacementVolume*liquidDensity*gravityAccel #[N]
shellWeight=gravityAccel*(swimmerDisplacementVolume-swimmerAirPocketVolume-magnetVolume)*swimmerShellDensity*1000 #[N]
VSF=swimmerBuoyancy-magnetWeight-shellWeight
print("Vertical static force = {} N".format(VSF))
time.sleep(2)

#///////////////////////////////////////////////////////////////////////
#calculate step out frequency and corresponding propulsive force
#///////////////////////////////////////////////////////////////////////
moment=magnetMagnetization*3.14*magnetDiameter*magnetDiameter*magnetLength/4
results=cfd.searchStepOutFrequency(moment,V,R,L,k,10)


print("Step out frequency = {} Hz".format(results[0]))
print("Force at step out frequency = {} N".format(results[1]))
print("Vertical static force = {} N".format(VSF))
print("Forces ration = {}".format(results[1]/VSF))
