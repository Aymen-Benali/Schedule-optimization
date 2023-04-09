import random
from turtle import color
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
# from tInstance import Job,State,Machine,PT,num_mach,mach_name
from tInstance import Job,State,Machine,PT,num_mach,mach_name
import datetime 

class Item:
    def __init__(self):   #for a given job we declare these variables:
        self.start=[]         #list of the starting time of each job
        self.end=[]           #list of the ending time of each job
        self._on=[]           #time of operation for each job
        self.T=[]             #time in process for each job
        self.last_ot=0        #the time of the end of the last operation
        self.L=0              #the loading machine time 

    def update(self,s,e,on,t):
        self.start.append(s)
        self.end.append(e)
        self._on.append(on)
        self.T.append(t)
        self.last_ot=e
        self.L+=t

class scheduling:
    
    def __init__(self,J_num,Machine,State,PT):
        self.M=Machine          #machine declaration
        self.J_num=J_num        # nb of total job "how many job we operate"
        self.State=State        # l'etage 
        self.PT=PT              #7list of lists PT: from the instance to set teh processing time of each job in each stage with a given machine
        self.Create_Job()       #create a job
        self.Create_Machine()   #create a machine
        self.fitness=0          #fitness start 0

    def Create_Job(self):
        self.Jobs=[]            #create a list of jobs
        for i in range(self.J_num):
            J=Item()            #heritate the criteria of the class item 
            self.Jobs.append(J)

    def Create_Machine(self):
        self.Machines=[]        #create a list of all machines
        for i in range(len(self.M)):    ##Highlight the stages of machines, that is, which machines are in each stage
            State_i=[]          #for a given stage :we append its machines
            for j in range(self.M[i]):
                M=Item()
                State_i.append(M) #append the machine in the stage i list
            self.Machines.append(State_i) #append the machine of a given stage in the list of all the machines

    ##Decoding at each stage
    def Stage_Decode(self,CHS,Stage):       
        for i in CHS:
            last_od=self.Jobs[i].last_ot                                                # the time of the end of the last operation for a given job
            last_Md=[self.Machines[Stage][M_i].last_ot for M_i in range(self.M[Stage])] ##list of Machine completion time   
            last_ML = [self.Machines[Stage][M_i].L for M_i in range(self.M[Stage])]     ##list of Machine load
            M_time=[self.PT[Stage][M_i][i] for M_i in range(self.M[Stage])]             ##list of Processing time of the machine for the current operation
            O_et=[last_Md[_]+M_time[_] for _ in range(self.M[Stage])]                   #list of (the totals of: machine completion time + processing time of the machine for the current operation: for each stage(=state)
        #these lines are described by the step 2 of the decoding's part
            if O_et.count(min(O_et))>1 and last_ML.count(last_ML)>1:                    # if (there is more than one minimum in the liste) and the list of machine load is bigger than 1 
                Machine=random.randint(0,self.M[Stage])                                 #these lines describe step 2 of decoding part
            elif O_et.count(min(O_et))>1 and last_ML.count(last_ML)<1:                  
                Machine=last_ML.index(min(last_ML))
            else:
                Machine=O_et.index(min(O_et))
        # these lines describe the step 1 of the decoding part
            s=max(last_od,last_Md[Machine])                     #s is the maximum between(the end's time of the last operation of the job AND the machine compelation time) 
            e=max(last_od,last_Md[Machine])+M_time[Machine]     #e is the maximum between(the end's time of the last operation of the job AND sum of machine compelation time and the processing time of the machine for the current operation)
            t=M_time[Machine]                                   # for a given machine: t is processing time of the machaine for the current operation 
            self.Jobs[i].update(s, e,Machine, t)             
            self.Machines[Stage][Machine].update(s, e,i, t)               #use the update function to set the start, end and operational time 
            if e>self.fitness:
                self.fitness=e

    ##decode
        #this function describe the step 3 of decoding part 
    def Decode(self,CHS):
        for i in range(self.State):
            self.Stage_Decode(CHS,i)
            Job_end=[self.Jobs[i].last_ot for i in range(self.J_num)]
            CHS = sorted(range(len(Job_end)), key=lambda k: Job_end[k], reverse=False)






    # ##Draw a Gantt chart
    def Gantt(self):
        fig = plt.figure()
        M = ['#808080','#DAA520','#EEC900','#FFFAF0','#FF7D40','#B22222','#00C957','#1E90FF','#696969','#00FFFF','#00B2EE','#BF3EFF','#CDC0B0','#CD1076','#7FFFD4','#483D8B','#9BCD9B','#B23AEE','#8B4500','#458B74','#FF8C00','#BCEE68','#BDB76B','#8B6508','#B8860B','#DC143C','#8B8878','#6495ED','#808A87','#8B4513','#66CD00','#FF6103','#C1CDCD','#7AC5CD','#5F9EA0','#FFE4C4','#CDAA7D','#8B2323','#9C661F','#0000CD','#20B2AA','#8470FF',
             '#EEB422','#8B7500','#FFD700','#228B22','#8B1A1A','#FF3030','#FCE6C9','#1C86EE','#00688B','#68228B','#00BFFF','#EE1289','#2F4F4F','#76EEC6','#EEDFCC','#B4EEB4','#68228B','#EE7600','#6E8B3D','#CAFF70','#006400','#CD950C','#008B8B','#8B8878','#6495ED','#FF7256','#3D9140','#EE7621','#76EE00','#E0EEEE','#FF9912','#8EE5EE','#8A3324','#E3CF57','#EEC591','#CD3333','#8A2BE2','#0000FF','#F08080','#7A8B8B','#B0E2FF','#FF00FF',
             '#FFC125','#CDAD00','#F8F8FF','#DCDCDC','#CD2626','#EE2C2C','#104E8B','#1874CD','#009ACD','#8B0A50','#FF1493','#79CDCD','#97FFFF','#C1FFC1','#E9967A','#FF7F00','#FAEBD7','#A2CD5A','#556B2F','#A9A9A9','#EEAD0E','#00CDCD','#8B8878','#6495ED','#FF7F50','#3D59AB','#D2691E','#7FFF00','#ED9121','#98F5FF','#8A360F','#FFD39B','#FF4040','#F0FFFF','#00008B', '#FFEBCD','#F0F8FF','#8B814C','#CD8C95','#CD8162','#607B8B','#E3A869']
        plt.grid(axis="y",which="major",ls="--", lw=1)
        plt.grid(axis="x",which="major",ls="--", lw=1)
        M_num=0
        for i in range(State):
            for j in range(self.M[i]):
                for k in range(len(self.Machines[i][j].start)):
                    Start_time=self.Machines[i][j].start[k]
                    End_time=self.Machines[i][j].end[k]
                    Job=self.Machines[i][j]._on[k]
                    #title=str(datetime.timedelta(self.Machines[State-1][self.M[State-1]].end[len(self.Machines[State-1][self.M[State-1]].start)]))
                    # Start_time=str(datetime.timedelta(self.Machines[i][j].start[k]))
                    # print(Start_time)
                    # End_time=str(datetime.timedelta(self.Machines[i][j].end[k]))
                    # print(End_time)
                    # Job=str(datetime.timedelta(self.Machines[i][j]._on[k]))
                    # print(Job)
                    if (End_time - Start_time)!=0:
                        plt.barh(M_num, width=End_time - Start_time, height=0.8, left=Start_time, \
                             color=M[Job], edgecolor='black')
                        plt.text(x=Start_time + ((End_time - Start_time) / 2.5 ), y=M_num ,
                             s=Job+3, size=10, fontproperties='Times New Roman')
                    

                    #plt.barh(M_num, width=End_time - Start_time, height=0.8, left=Start_time, \
                     #       color=M[Job], edgecolor='black')
                    #plt.barh(M_num, width=End_time - Start_time, height=0.8, left=Start_time, \
                    #        color=M[Job], edgecolor='black')
                    #plt.text(x=Start_time-0.5 , y=M_num - 0.2,
                    #            s=Job+1, size=10, fontproperties='Times New Roman')
                    #plt.text(x=Start_time + ((End_time - Start_time) / 3 - 0.25), y=M_num - 0.2,
                    #         s=Job+1, size=10, fontproperties='Times New Roman')
                M_num += 1

        for i in range(State):
            for j in range(self.M[i]):
                for k in range(len(self.Machines[i][j].start)):
                    Start_time=self.Machines[i][j].start[k]
                    End_time=self.Machines[i][j].end[k]
                    Job=self.Machines[i][j]._on[k]

        plt.yticks(np.arange(M_num + 1), np.arange(1, M_num + 2), size=5, fontproperties='Times New Roman')
        plt.ylabel("Machine", size=10, fontproperties='SimSun')
        
        plt.xlabel("Time", size=10, fontproperties='SimSun')
        plt.tick_params(labelsize=10)
        plt.tick_params(direction='in')
        plt.title("Objective :" )
        plt.show()
## Sch=Scheduling(J_num,Machine,State,PT)