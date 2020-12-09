import numpy as np
import traci
tl_states=(("GGgrrrGGgrrr","yyyrrryyyrrr"),("rrrGGgrrrGGg","rrryyyrrryyy"))

actions_list=[(10,tl_states[0]),(20,tl_states[0]),(30,tl_states[0]),(45,tl_states[0]),
(10,tl_states[1]),(20,tl_states[1]),(30,tl_states[1]),(45,tl_states[1])]
edge_list=["n4junc","n3junc","n2junc","n1junc"]
edge_cap=4
edge_count=len(edge_list)
discrete_states_size=[edge_cap]*edge_count
def get_speed_state():
    state=[]
    for i in edge_list:
        if traci.edge.getLastStepVehicleNumber(i)==0:
            inp=-1
        else:
            inp=traci.edge.getLastStepMeanSpeed(i)
        if inp==-1:
            state.append(0)
        elif inp>=0 and inp<=2 :
            state.append(1)
        elif inp>2 and inp<=7:
            state.append(2)
        elif inp>7 and inp<=12:
            state.append(3)
        elif inp>12:
            state.append(4)
    return tuple(state)

def get_wait_state():
    wt=[]
    state=[]
    for i in edge_list:
        inp=traci.edge.getWaitingTime(i)
        if inp==0:
            state.append(0)
        elif inp>=0 and inp<=7 :
            state.append(1)
        elif inp>7 and inp<=20:
            state.append(2)
        elif inp>20:
            state.append(3)
    return tuple(state)

def get_state():
    state=[]
    for i in edge_list:
        inp=traci.edge.getLastStepVehicleNumber(i)
        if inp==0:
            state.append(0)
        elif inp>=0 and inp<=7 :
            state.append(1)
        elif inp>7 and inp<=15:
            state.append(2)
    return tuple(state)

def get_reward(state,next_state):
    rew=np.mean(np.subtract(state,next_state))
    return rew
def get_reward(state,next_state):
    rew=0
    if next_state[0]==next_state[2]==0:
        rew=-8+next_state[1]+next_state[3]
    elif next_state[1]==next_state[3]==0:
        rew=-8+next_state[0]+next_state[2]
    else:
        rew=-np.var([next_state[0]+next_state[2],next_state[1]+next_state[3]])
    return rew
