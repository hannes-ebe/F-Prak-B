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
        self.fit=False

    def get_fit(self,start,stop,p0):
        f_exp = lambda t,offset,a,b: b*np.exp(a*t)+offset 
        self.time_mod = self.time[start:stop]
        self.ch1_mod = self.ch1[start:stop]
        self.ch2_mod = self.ch2[start:stop]
        self.popt, self.pcov = curve_fit(f_exp,self.time_mod,self.ch2_mod,maxfev=10000,p0=p0)
        self.tau=-1/self.popt[1]
        self.tau_err=np.abs(np.sqrt(self.pcov[1][1])/self.popt[1]**2)
        print(f"tau ist {self.tau} pm {self.tau_err}")
        self.fit=True

    def exp_fit(self,t):
        f_exp = lambda t,offset,a,b: b*np.exp(a*t)+offset 
        return f_exp(t,self.popt[0],self.popt[1],self.popt[2])
        

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
            if self.fit:
                ax2.plot(self.time_mod,self.exp_fit(self.time_mod)+offset2,label='Channel 2 fit',color='C1',ls="--")
        else:
            ax1.plot(self.time,self.ch1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2,label='Channel 2',color='C1')
            if self.fit:
                ax2.plot(self.time_mod,self.exp_fit(self.time_mod),label='Channel 2 fit',color='C1',ls="---")
        ax1.tick_params(axis='y', labelcolor='C0')
        ax2.tick_params(axis='y', labelcolor='C1')
        ax1.legend(loc=2)
        ax2.legend(loc=3)
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel1,c="C0")
        ax2.set_ylabel(ylabel2,c='C1')
        plt.title(title)
        plt.tight_layout()
        plt.savefig("figures/dt/tau_bsp.pdf")
        return fig, ax1, ax2

def main():
    a=Oszi("data/ohne_B/orientierungszeit/30Hz_5Vpp")
    start_stop_30=[420,1901]
    start_stop_60=[200,2000]
    start_stop_100=[700,1700]
    a.get_fit(start_stop_30[0],start_stop_30[1],[1.6,-1/0.00295,-0.1])
    a.plot(ScopeSettings=True,ylabel1="U in V Channel 1",ylabel2="U in V Channel 2",title="Orientierungsezit")
    plt.show()


if __name__=="__main__":
    main()