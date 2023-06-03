import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import linecache

# class fourier:
#     def __init__(self,f: float,max_n: int,t: np.ndarray) -> None:
#         self.f=f
#         self.omega=2*np.pi*self.f
#         self.max_n=max_n
#         self.t=t
#         self.U=self.get_U()
#         self.settings=pd.read_csv("data/ohne_B/dt_messung/30Hz_5Vpp_ScopeSettings.txt",sep=" ")
#         self.messung=pd.read_csv("data/ohne_B/dt_messung/30Hz_5Vpp",sep="\t",names=["t","U1","U2"])
#         # print(self.settings)
#         self.plot()
#         pass

#     def get_U(self):
#         U_arr=np.zeros(len(self.t))
#         for ti,t in enumerate(self.t):
#             for n in range(1,self.max_n):
#                 U_arr[ti]+=np.sin((2*n-1)*self.omega*t)/(2*n-1)
#         return U_arr




#     def plot(self):
#         # plt.plot(self.t,self.U)
#         print(self.settings.loc[0,"1"])
#         U_trans=np.array(self.messung["U1"])+float(self.settings.loc[1,"1"])
#         plt.plot(self.messung["t"],U_trans)
#         plt.plot(self.messung["t"],np.array(self.messung["U2"]))
#         plt.show()

class Oszi:
    def __init__(self,path):
        '''Path ohne Endung angeben.'''
        data = np.genfromtxt(path).T
        self.path = path
        self.scope = path + '_ScopeSettings.txt'
        self.time = data[0]
        self.ch1 = data[1]
        self.ch2 = data[2]

    def plot(self,xlabel=None,ylabel1=None,ylabel2=None,title=None,figsize=(8,5),ScopeSettings=False):
        '''ScopeSettings gibt an, ob Oszi-Fenster wie im Praktikum dargestellt werden soll.'''
        fig, ax1 = plt.subplots(figsize=figsize)
        ax2 = ax1.twinx()
        if ScopeSettings == True:
            '''Bin mir nicht ganz sicher, ob das so passt. Wahrscheinliche automatische Anpassung besser'''
            offset1 = float(linecache.getline(self.scope,3).split()[1])
            # scale1 = float(linecache.getline(self.scope,2).split()[1])
            offset2 = float(linecache.getline(self.scope,11).split()[1])
            # scale2 = float(linecache.getline(self.scope,10).split()[1])
            print(offset1)
            print(offset2)
            ax1.plot(self.time,self.ch1+offset1,label='Channel 1',color='blue')
            ax2.plot(self.time,self.ch2+offset2,label='Channel 2',color='red')
            ax1.legend(loc=2)
            ax2.legend(loc=3)
            ax1.tick_params(axis='y', labelcolor='blue')
            ax2.tick_params(axis='y', labelcolor='red')
        else:
            ax1.plot(self.time,self.ch1,label='Channel 1',color='blue')
            ax2.plot(self.time,self.ch2,label='Channel 2',color='red')
            ax1.legend(loc=2)
            ax2.legend(loc=3)
            ax1.tick_params(axis='y', labelcolor='blue')
            ax2.tick_params(axis='y', labelcolor='red')
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel1,c='blue')
        ax2.set_ylabel(ylabel2,c='red')
        plt.title(title)
        return fig, ax1, ax2

def main():
    a=Oszi("data/ohne_B/l_messung/30Hz_5Vpp")
    a.plot(ScopeSettings=False)
    plt.show()
    # b=fourier(0.25,1000,np.arange(0,10,0.01))


if __name__=="__main__":
    main()