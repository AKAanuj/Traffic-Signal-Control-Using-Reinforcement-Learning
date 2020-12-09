import numpy as np
import matplotlib.pyplot as plt
import traci
import sys
from statesfile import get_state,edge_list,edge_cap,edge_count,discrete_states_size
sys.path.insert(0,"C:\tools")
sumobinary = "sumo"
sumocfg=r"C:\Users\hp-PC\Desktop\Sumofiles\final\xml\sumofile.sumocfg"

episodes=25000

learning_rate=0.1
discount=0.95
epsilon=0.5
start_epsilon_decaying=1
end_epsilon_decaying=episodes//2
epsilon_decay_rate=epsilon/(end_epsilon_decaying-start_epsilon_decaying)

tl_states=(("GGgrrrGGgrrr","yyyrrryyyrrr"),("rrrGGgrrrGGg","rrryyyrrryyy"))
actions_list=[(10,tl_states[0]),(20,tl_states[0]),(30,tl_states[0]),(40,tl_states[0]),
             (10,tl_states[1]),(20,tl_states[1]),(30,tl_states[1]),(40,tl_states[1])]

yellow_state_time=3


qtable=np.random.uniform(low=-1,high=0,size=(discrete_states_size+[len(actions_list)])).astype(np.float16)
graph={"Episodic Reward":[],"Mean Speed":[],"Edge Length":[]}
def start_sumo(input):
    sumocmd = [sumobinary, "-c", sumocfg, "--start","--quit-on-end"]    
    traci.start(sumocmd,label="{}".format(input))

def get_action(state):#returns index from action list
    #exploration exploitation
    global epsilon
    global episodes
    if end_epsilon_decaying>=episodes>=start_epsilon_decaying:
        epsilon+=epsilon_decay_value
    if np.random.random() > epsilon:       
        return np.argmax(qtable[state])
    else:
        return np.random.randint(0,len(actions_list))

def get_reward(state,next_state):
    rew=0
    if next_state[0]==next_state[2]==0:
        rew=-8+next_state[1]+next_state[3]
    elif next_state[1]==next_state[3]==0:
        rew=-8+next_state[0]+next_state[2]
    else:
        rew=-np.var([next_state[0]+next_state[2],next_state[1]+next_state[3]])
    return rew

def get_edge_length():
    len=[]
    for i in edge_list:
        len.append(traci.edge.getLastStepVehicleNumber(i))
    return len

def get_mean_speed():
    speed=[]
    for i in edge_list:
        speed.append(traci.edge.getLastStepMeanSpeed(i))
    return speed
i=0
start_sumo(0)
tlid=traci.trafficlight.getIDList()
state=get_state()
action=get_action(state)
traci.trafficlight.setRedYellowGreenState(tlid[0],actions_list[action][1][0])
traci.trafficlight.setPhaseDuration(tlid[0],actions_list[action][0])
print(state,action)
for i in range(episodes):
    mean_edge_length=0
    mean_speed=0
    ep_reward=0
    start_sumo(i+1)    
    np.random.seed(i)
    simval=1
    time=1
    print("episode :",i)
    while simval<700:
        edge_len=np.mean(get_edge_length())
        mean_edge_length=mean_edge_length+((edge_len-mean_edge_length)/(simval+1))
        speed=np.mean(get_mean_speed())
        mean_speed=mean_speed+((speed-mean_speed)/(simval+1))
        if time==actions_list[action][0]:
            traci.trafficlight.setRedYellowGreenState(tlid[0],actions_list[action][1][1])
            traci.trafficlight.setPhaseDuration(tlid[0],yellow_state_time)
             
            
            for i in range(yellow_state_time):            
                traci.simulationStep()
            next_state=get_state()
            reward=get_reward(state,next_state)
            ep_reward+=reward
           
            traci.trafficlight.setRedYellowGreenState(tlid[0],actions_list[action][1][0])
            traci.trafficlight.setPhaseDuration(tlid[0],actions_list[action][0])
            
            max_future_q=np.max(qtable[next_state])
            
            current_q=qtable[state+(action,)]
            print("state",state)
            print("action",action)
            print("next state",next_state)
            print("cq:",current_q,qtable[state])
            new_q=(1-learning_rate)*current_q+learning_rate*(reward+(discount*max_future_q-current_q))
            
            qtable[state+(action,)]=new_q
            print("new_q:",new_q,qtable[state])
            time=1
            action=get_action(next_state)   
            print("new_action",action)
            print("-------------------------")
            state=next_state
        else:
            time+=1
        traci.simulationStep()
        simval+=1
      
    graph["Edge Length"].append(mean_edge_length)
    graph["Mean Speed"].append(mean_speed)
    traci.close()
    graph["Episodic Reward"].append(ep_reward)
np.save("qtable",qtable)

plt.figure()
plt.plot([x for x in range(episodes)],graph["Episodic Reward"])
plt.xlabel("Episodes")
plt.ylabel("Reward")
plt.legend()
plt.show()

plt.figure()
plt.plot([x for x in range(episodes)],graph["Edge Length"])
plt.xlabel("Episodes")
plt.ylabel("Edge Length")
plt.legend()
plt.show()

plt.figure()
plt.plot([x for x in range(episodes)],graph["Mean Speed"])
plt.xlabel("Episodes")
plt.ylabel("Mean Speed")
plt.legend()
plt.show()
EL=np.array(graph["Edge Length"])
MS=np.array(graph["Mean Speed"])
np.save("Edge_Length",EL)
np.save("Mean_Speed",MS)