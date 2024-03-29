import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import pandas as pd
import linecache
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 22})

class Oszi:
    def __init__(self,path,f):
        '''Path ohne Endung angeben.'''
        data = np.genfromtxt(path).T
        self.path = path
        self.scope = path + '_ScopeSettings.txt'
        self.time = data[0]
        self.ch1 = data[1]
        self.ch2 = data[2]
        self.omega=f*2*np.pi
        self.fourier_U,self.fourier_I = self.get_U_fourier()

    def get_U_fourier(self):
        U_arr=np.zeros(len(self.time))
        I_arr=np.zeros(len(self.time))
        self.L=0.0047
        self.R=1.7223
        t_off=0.00011
        for ti,t in enumerate(self.time):
            for n in range(1,1000):
                U_arr[ti]+=4/np.pi*7/8*np.sin((2*n-1)*self.omega*(t-t_off))/(2*n-1)
                I_arr[ti]+=4/np.pi*(np.sin((2*n-1)*self.omega*(t-t_off)-np.arctan((2*n-1)*self.omega*self.L/self.R)))/((2*n-1)**2*self.omega**2*self.L**2*+self.R**2)
        return U_arr,I_arr

    def get_L(self):
        f_exp = lambda t,offset,a,b: b*np.exp(a*t)+offset 
        self.time_mod = self.time[55:]
        self.ch1_mod = self.ch1[55:]
        self.ch2_mod = self.ch2[55:]
        self.popt, self.pcov = curve_fit(f_exp,self.time_mod,self.ch1_mod)
        self.L=1.7223/self.popt[1]*-1
        self.L_err=np.abs(np.sqrt(self.pcov[1][1])*1.7223/self.popt[1]**2)+np.abs(0.0017/self.popt[1]*-1)
        print(f"L ist {self.L} pm {self.L_err}")

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
            # scale1 = float(linecache.getline(self.scope,2).split()[1])
            offset2 = float(linecache.getline(self.scope,11).split()[1])
            # scale2 = float(linecache.getline(self.scope,10).split()[1])
            print(offset1)
            print(offset2)
            ax1.plot(self.time,self.ch1+offset1,label='Channel 1',color='C0')
            # ax1.plot(self.time_mod,self.exp_fit(self.time_mod),label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2+offset2,label='Channel 2',color="C1")
            ax1.plot(self.time,self.fourier_U,label='Fourier Spannung',color='C0',ls="--")
            ax2.plot(self.time,self.fourier_I,label='Fourier Strom',color='C1',ls="--")
            pos_0 = np.argmin(np.abs(self.fourier_I))
            ax2.scatter(self.time[pos_0],self.fourier_I[pos_0],c="C2",label="geschärtzter Start des Pumpens")
            ax2.scatter(self.time[2376],self.ch2[2376]+offset2,c="C2")
            print(self.time[2376]-0.00011,self.time[pos_0]-0.00011,self.time[2376]-self.time[pos_0])
        else:
            ax1.plot(self.time,self.ch1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2,label='Channel 2',color='C1')
            ax1.plot(self.time,self.fourier_U,label='Fourier Spannung',color='C0')
            ax2.plot(self.time,self.fourier_I,label='Fourier Strom',color='C1')
        ax1.tick_params(axis='y', labelcolor='C0')
        ax2.tick_params(axis='y', labelcolor='C1')
        # ax1.legend(bbox_to_anchor=(1.09,1),loc="upper left")
        # ax2.legend(bbox_to_anchor=(1.09,0.85),loc="upper left")
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel1,c="C0")
        ax2.set_ylabel(ylabel2,c='C1')
        plt.title(title)
        plt.tight_layout()
        plt.savefig("figures/dt/dt_1.pdf")
        return fig, ax1, ax2

def dt():
    a=Oszi("data/ohne_B/dt_messung/30Hz_5Vpp",30)
    a.get_L()
    a.plot(ScopeSettings=True,ylabel1="Ch 1 U in V",ylabel2="Ch 2 U in V",title="Messung der Induktivität",figsize=(20,10))
    plt.show()
    # b=fourier(0.25,1000,np.arange(0,10,0.01))


if __name__=="__main__":
    dt()