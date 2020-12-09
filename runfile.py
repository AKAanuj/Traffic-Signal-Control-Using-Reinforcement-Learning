import numpy as np
import matplotlib.pyplot as plt
import traci
import sys
from statesfile import get_state,actions_list,edge_list,tl_states
sys.path.insert(0,"C:\tools")
sumobinary = "sumo-gui"
sumocfg=r"C:\Users\hp-PC\Desktop\Sumofiles\final\xml\sumofile.sumocfg"

yellow_state_length=3
qtable=np.load("qtable.npy")
def start_sumo(input):
    sumocmd = [sumobinary, "-c", sumocfg, "--start","--quit-on-end"]    
    traci.start(sumocmd,label="{}".format(input))     


def get_action(state):#returns index from action list
    return np.argmax(qtable[state])

def waiting_time():
    wt=[]
    for i in edge_list:
        wt.append(traci.edge.getWaitingTime(i))
    return wt

start_sumo(1)
simval=0
tlid=traci.trafficlight.getIDList()
test_sum=0
waiting_time_list=[]
while simval<700:
    print(simval)
    state=get_state()
    action=get_action(state)
    waiting_time_list.append(waiting_time())
    print(state," ",action)
    print(qtable[state])
    traci.trafficlight.setRedYellowGreenState(tlid[0],actions_list[action][1][0])
    traci.trafficlight.setPhaseDuration(tlid[0],actions_list[action][0])
    phasedur=actions_list[action][0]+yellow_state_length
    while phasedur!=0:
        if phasedur==yellow_state_length:
            traci.trafficlight.setRedYellowGreenState(tlid[0],actions_list[action][1][1])
            traci.trafficlight.setPhaseDuration(tlid[0],yellow_state_length)
        traci.simulationStep()
        simval+=1
        phasedur-=1
        
temp=[]
mean=[]
for j in range(4):
    for i in range(len(waiting_time_list)):
        temp.append(waiting_time_list[i][j])
    mean.append(np.mean(temp))

np.save("result/optim_time.npy",mean)