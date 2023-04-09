import random
import numpy as np
import copy
from tInstance import Job,State,Machine,PT,num_mach
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class GA:
    def __init__(self,J_num,State,Machine,PT):
        self.State=State
        self.Machine=Machine
        self.PT=PT
        self.J_num=J_num
        self.Pm=0.2
        self.Pc=0.9
        self.Pop_size=100                           #the population size

    ## Randomly generated chromosomeimport matplotlib
    def RCH(self):                                  #the set of job in a given stage : exp state 2 ===[4,5,6,2,1,3,0]    
        Chromo = [i for i in range(self.J_num)]
        random.shuffle(Chromo)                      #we have to work with real affectation blocs
        return Chromo                           

    ## Generate initial population
    def CHS(self):
        CHS = []                                    
        for i in range(self.Pop_size):              # for i in the population size we have to append each set of jobs for a given stage 
            CHS.append(self.RCH())
        return CHS

    ##choice
    def Select(self, Fit_value):
        
        Fit = []
        for i in range(len(Fit_value)):
            fit = 1 / Fit_value[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(Fit_value)), size=len(Fit_value), replace=True,
                               p=(Fit) / (Fit.sum()))
        return idx
         
    ## overlapping
    def Crossover(self, CHS1, CHS2):
        T_r = [j for j in range(self.J_num)]
        r = random.randint(2, self.J_num)  ## An integer r is generated in the interval [1,T0]
        random.shuffle(T_r)
        R = T_r[0:r]  ## Generate r unequal integers according to the random number r
        ## Copy the chromosomes of the parents into the offspring and maintain their order and position
        H1=[CHS1[_] for _ in R]
        H2=[CHS2[_] for _ in R]
        C1=[_ for _ in CHS1 if _ not in H2]
        C2=[_ for _ in CHS2 if _ not in H1]
        CHS1,CHS2=[],[]
        k,m=0,0
        for i in range(self.J_num):
            if i not in R:
                CHS1.append(C1[k])
                CHS2.append(C2[k])
                k+=1
            else:
                CHS1.append(H2[m])
                CHS2.append(H1[m])
                m+=1
        return CHS1, CHS2

    ## variation
    def Mutation(self, CHS):
        Tr = [i_num for i_num in range(self.J_num)]
        ## Machine selection section
        r = random.randint(1, self.J_num)  ## Select r positions in the mutant chromosome
        random.shuffle(Tr)
        T_r = Tr[0:r]
        K=[]
        for i in T_r:
            K.append(CHS[i])
        random.shuffle(K)
        k=0
        for i in T_r:
            CHS[i]=K[k]
            k+=1
        return CHS

    def main(self):
        BF=[]
        x=[_ for _ in range(self.Pop_size+1)]
        C=self.CHS()
        Fit=[]
        from tScheduling import scheduling as Sch
        for C_i in C:
            s=Sch(self.J_num,self.Machine,self.State,self.PT)
            s.Decode(C_i)
            Fit.append(s.fitness)
        best_C = None
        best_fit=min(Fit)
        BF.append(best_fit)
        for i in range(self.Pop_size):
            C_id=self.Select(Fit)
            C=[C[_] for _ in C_id]
            for Ci in range(len(C)):
                if random.random()<self.Pc:
                    _C=[C[Ci]]
                    CHS1,CHS2=self.Crossover(C[Ci],random.choice(C))
                    _C.extend([CHS1,CHS2])
                    Fi=[]
                    for ic in _C:
                        s = Sch(self.J_num, self.Machine, self.State, self.PT)
                        s.Decode(ic)
                        Fi.append(s.fitness)
                    C[Ci]=_C[Fi.index(min(Fi))]
                    Fit.append(min(Fi))
                elif random.random()<self.Pm:
                    CHS1=self.Mutation(C[Ci])
                    C[Ci]=CHS1
            Fit = []
            Sc=[]
            for C_i in C:   
                s = Sch(self.J_num, self.Machine, self.State, self.PT)
                s.Decode(C_i)
                Sc.append(s)
                Fit.append(s.fitness)
            if min(Fit)<best_fit:
                best_fit=min(Fit)
                best_C=Sc[Fit.index(min(Fit))]
            BF.append(best_fit)
        plt.plot(x,BF)
        plt.show()
        best_C.Gantt()

if __name__=="__main__":
    g=GA(Job,State,Machine,PT)
    g.main()


