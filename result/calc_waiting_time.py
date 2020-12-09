import numpy as np
import traci
import sys

sys.path.insert(0,"C:\tools")
sumobinary = "sumo-gui"
sumocfg=r"C:\Users\hp-PC\Desktop\Sumofiles\final\xml\sumofile.sumocfg"
edge_list=["n4junc","n3junc","n2junc","n1junc"]

def start_sumo(input):
    sumocmd = [sumobinary, "-c", sumocfg, "--start","--quit-on-end"]    
    traci.start(sumocmd,label="{}".format(input))
    
def waiting_time():
    wt=[]
    for i in edge_list:
        wt.append(traci.edge.getWaitingTime(i))
    return wt

simval=0
waiting_time_list=[]
start_sumo(simval)
while simval<700:  
    waiting_time_list.append(waiting_time())
    simval+=1
    traci.simulationStep()
traci.close()
temp=[]
mean=[]
for j in range(4):
    for i in range(len(waiting_time_list)):
        temp.append(waiting_time_list[i][j])
    mean.append(np.mean(temp))

no_optim_time=np.mean(mean)
optim_time=np.mean(np.load("optim_time.npy"))
print("Average waiting time without optimization : %.2f s" %no_optim_time)
print("Average waiting time with optimization : %.2f s" %optim_time)
print("Percentage decrease in waiting time : %.2f " % ((no_optim_time-optim_time)/(no_optim_time)*100))
