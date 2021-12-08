# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.collections import PolyCollection
# FREECADPATH = '/usr/lib/freecad/lib'
# import sys
# sys.path.append(FREECADPATH)
# import FreeCAD
# import FreeCADGui
# App=FreeCAD
# import time

#Example:
Diam=2.5
Ptch1=3.0
Ptch2=2.5
Length=6.0
Thread=0.5
Curve=0.5
Thickness=0.2
Cut=2.0


ExportObjPath=u"SwimmerGeometryGeneration/propeller.obj";
# Space=input("Enter spacing between tip pitch and base pitch: ");
# Spacing between pitches isn't a defined parameter atm
# Tip cut angle could also be a variable with width if needed

A=Diam; # convert from string
Rad=(A/2) # total radius

B=Thread;
Rad2=Rad-B; #cylinder radius (model radius - thread depth) = (1.25 - thread depth)

FreeCAD.open(u"SwimmerGeometryGeneration/SwimmerModel7.FCStd")
App.setActiveDocument("SwimmerModel7")
App.ActiveDocument=App.getDocument("SwimmerModel7")
#FreeCADGui.ActiveDocument=FreeCADGui.getDocument("SwimmerModel7")

# Edit thread depth (cylinder radius)
FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Radius = Rad2

# Changing angle of bottom pitch to align with top pitch (if we change vertical placement of threads, adjust this)
R=360*(1-4/Ptch1)
FreeCAD.getDocument("SwimmerModel7").getObject("Sweep").Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),R))
App.activeDocument().recompute()

# Editing pitch

FreeCAD.getDocument("SwimmerModel7").getObject("Helix").Pitch = Ptch1
App.activeDocument().recompute()
FreeCAD.getDocument("SwimmerModel7").getObject("Helix001").Pitch = Ptch2
App.activeDocument().recompute()
FreeCAD.getDocument("SwimmerModel7").getObject("Helix002").Pitch = Ptch2
App.activeDocument().recompute()
#
#FreeCAD.getDocument("SwimmerModel7").getObject("Helix001").Pitch = 2

# Thread thickness
#----------

T=(Thickness-0.2)
App.ActiveDocument.Sketch001.setDatum(11,App.Units.Quantity(4.100000+(T/2)))
App.ActiveDocument.Sketch001.setDatum(9,App.Units.Quantity(3.900000-(T/2)))
App.ActiveDocument.Sketch.setDatum(11,App.Units.Quantity(0.100000+(T/2)))
App.ActiveDocument.Sketch.setDatum(9,App.Units.Quantity(-1*(0.100000+(T/2))))
App.ActiveDocument.Sketch002.setDatum(9,App.Units.Quantity(4.100000+(T/2)))
App.ActiveDocument.Sketch002.setDatum(11,App.Units.Quantity(3.900000-(T/2)))
#-------
# Change total radius

App.ActiveDocument.Sketch002.setDatum(8,App.Units.Quantity(-Rad))
App.ActiveDocument.Sketch001.setDatum(10,App.Units.Quantity(Rad))
App.ActiveDocument.Sketch.setDatum(10,App.Units.Quantity(Rad))

# Changing tip curvature (fillet radius)

__fillets__ = []
__fillets__.append((1,Curve,Curve))
FreeCAD.ActiveDocument.Fillet.Edges = __fillets__
del __fillets__
#FreeCADGui.ActiveDocument.Cylinder.Visibility = False

# Changing length adds to the end length (should we also add space between tip and base pitches?)

L=6-Length
FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Height = Length
#FreeCAD.getDocument("SwimmerModel7").getObject("Sketch003").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(1,0,0),90))
FreeCAD.getDocument("SwimmerModel7").getObject("Box").Placement = App.Placement(App.Vector(-2,-2,(-6+L)),App.Rotation(App.Vector(0,0,1),0))

# Last trims (tip cut angle can also be made variable)

Crve=Curve;
X=Rad2-Crve
Y=Length-Crve-0.01
Z=Crve+0.2

#App.ActiveDocument.Sketch003.setDatum(16,App.Units.Quantity(Rad+0.01))
#App.ActiveDocument.Sketch003.setDatum(15,App.Units.Quantity(Crve))
#App.ActiveDocument.Sketch003.setDatum(11,App.Units.Quantity(Z))
#App.ActiveDocument.Sketch003.setDatum(13,App.Units.Quantity(X))
#App.ActiveDocument.Sketch003.setDatum(17,App.Units.Quantity(X))
#App.ActiveDocument.Sketch003.setDatum(14,App.Units.Quantity(Y))

Web=0.05 # This is the amount of spacing at the tip for dulling the point.
#App.ActiveDocument.Sketch003.setDatum(6,App.Units.Quantity('6.010000 mm')) # height + 0.01

App.ActiveDocument.Sketch003.setDatum(5,App.Units.Quantity(0.01+Web)) # web
App.ActiveDocument.Sketch003.setDatum(7,App.Units.Quantity(6.01-Cut)) # angle via height of triangle base
#----------

# In order to add spacing btwn tip and base pitches... (Not using this atm)

#S=float(Space)
#FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Placement = App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,0,1),0))
#FreeCAD.getDocument("SwimmerModel7").getObject("Cylinder").Height = Length
#App.getDocument("SwimmerModel7").Sweep.Placement=App.Placement(App.Vector(0,0,-S), App.Rotation(App.Vector(0,0,1),0), App.Vector(0,0,0))

#Change bottom cut to have the same angle for any parameters (Radius and diameter of total swimmer being constant)
App.ActiveDocument.Sketch004.setDatum(5,App.Units.Quantity(-Rad2))

App.activeDocument().recompute()

# The original file is named 'SwimmerModel7')
# To save changes to the file itself:
#App.getDocument("test").save()

# Make sure this saves to a new name for each design, to avoid overwriting with
# a backup of any errors.
#App.getDocument("SwimmerModel7").saveAs(u"SwimmerModel79.FCStd")

# Save as an stl

#__objs__=[]
#__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut001"))
#import Mesh
#Mesh.export(__objs__,ExportOBJPath)
#Mesh.export(__objs__,ExportSTLPath)
#del __objs__

#__objs__=[]
#__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut001"))
#import Mesh
#Mesh.export(__objs__,ExportOBJPath)
#Mesh.export(__objs__,ExportSTLPath)
#del __objs__

#del __doc__, __mesh__, __part__, __shape__

#import ObjectsFem
#ObjectsFem.makeMeshNetgen(FreeCAD.ActiveDocument, 'FEMMeshNetgen')
#FreeCAD.ActiveDocument.ActiveObject.Shape = FreeCAD.ActiveDocument.Cut001
#FreeCADGui.ActiveDocument.setEdit(FreeCAD.ActiveDocument.ActiveObject.Name)
#import femmesh.femmesh2mesh
#out_mesh = femmesh.femmesh2mesh.femmesh_2_mesh(FreeCAD.ActiveDocument.FEMMeshNetgen.FemMesh)
#import Mesh
#Mesh.Mesh(out_mesh)
#FreeCAD.ActiveDocument.FEMMeshNetgen.ViewObject.hide()

# __objs__=[]
# __objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut003"))
# import Part
# Part.export(__objs__,ExportBrepPath)
# del __objs__

#del __objs__
#import Gui
#Gui.SendMsgToActiveView("SaveAs")
__objs__=[]
__objs__.append(FreeCAD.getDocument("SwimmerModel7").getObject("Cut003"))
import Mesh
Mesh.export(__objs__,ExportObjPath)
del __objs__
App.closeDocument("SwimmerModel7")
exit()
#//////////////////////////////////////////////////////////////////////
#END PART 3: Python code that uses FreeCAD to generate a custom swimmer
#/////////////////////////////////////////////////////////////////////
