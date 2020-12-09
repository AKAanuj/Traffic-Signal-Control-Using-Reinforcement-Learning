import xml.etree.ElementTree as ET
import numpy as np
import traci

prob=1/12.0
vehicletypes=["car"]
edges=["n1junc juncn2","n1junc juncn3","n1junc juncn4",
       "n2junc juncn1","n2junc juncn3","n2junc juncn4",
       "n3junc juncn1","n3junc juncn2","n3junc juncn4",
       "n4junc juncn1","n4junc juncn2","n4junc juncn3"]
routes=ET.Element("routes")
vType1=ET.SubElement(routes,"vType",attrib={"id":vehicletypes[0],"accel":"4.0","decel":"4.5","sigma":"0.5","length":"4","maxSpeed":"100"})    
#vType2=ET.SubElement(routes,"vType",attrib={"id":vehicletypes[1],"accel":"3.0","decel":"2.5","sigma":"0.1","length":"7","maxSpeed":"100"})

for i in range(1,50):
    vehicle=ET.SubElement(routes,"vehicle",attrib={"id":str(i),"type":str(np.random.choice(vehicletypes)),"depart":str(i*4),"guiShape":"emergency"})
    route=ET.SubElement(vehicle,"route",attrib={"edges":np.random.choice([edges[3],edges[4],edges[5],edges[9],edges[10],edges[11]])})
for i in range(50,100):
    vehicle=ET.SubElement(routes,"vehicle",attrib={"id":str(i),"type":str(np.random.choice(vehicletypes)),"depart":str(i*4),"guiShape":"emergency"})
    route=ET.SubElement(vehicle,"route",attrib={"edges":np.random.choice([edges[0],edges[1],edges[2],edges[6],edges[7],edges[8]])})
for i in range(100,200):
    vehicle=ET.SubElement(routes,"vehicle",attrib={"id":str(i),"type":str(np.random.choice(vehicletypes)),"depart":str(i*3),"guiShape":"emergency"})
    route=ET.SubElement(vehicle,"route",attrib={"edges":np.random.choice(edges,p=[prob,prob,prob,prob,prob,prob,prob,prob,prob,prob,prob,prob])})

stringdata=ET.tostring(routes,encoding="unicode")
file=open("route.rou.xml","w")
file.write(stringdata)
