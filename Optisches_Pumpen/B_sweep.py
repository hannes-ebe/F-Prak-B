import numpy as np
import matplotlib.pyplot as plt
import linecache
from scipy.optimize import curve_fit

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
            offset2 = float(linecache.getline(self.scope,11).split()[1])
            print(offset1)
            print(offset2)
            ax1.plot(self.time,self.ch1+offset1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2+offset2,label='Channel 2',color="C1")
        else:
            ax1.plot(self.time,self.ch1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2,label='Channel 2',color='C1')
        ax1.tick_params(axis='y', labelcolor='C0')
        ax2.tick_params(axis='y', labelcolor='C1')
        ax1.legend(loc=2)
        ax2.legend(loc=3)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel1,c="C0")
        ax2.set_ylabel(ylabel2,c='C1')
        plt.title(title)
        plt.tight_layout()
        plt.savefig("figures/dt/test.pdf")
        return fig, ax1, ax2

def main():
    a=Oszi("data/g_faktor/B_rampe/500kHz")
    a.plot(ScopeSettings=True,ylabel1="U in V Channel 1",ylabel2="U in V Channel 2",title="Orientierungsezit")
    plt.show()


if __name__=="__main__":
    main()