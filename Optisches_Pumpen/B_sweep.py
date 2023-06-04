import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import linecache
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

class Oszi:
    def __init__(self,path):
        '''Path ohne Endung angeben.'''
        data = np.genfromtxt(path).T
        self.path = path
        self.scope = path + '_ScopeSettings.txt'
        self.time = data[0]
        self.ch1 = data[1]
        self.ch2 = data[2]
        # print(np.arange(0.001,0.01,0.0001))
        for prom in np.arange(0.001,0.01,0.0001):
            # print(prom)
            self.peaks,_=find_peaks(-self.ch2,prominence=prom,distance=10)
            if len(self.peaks)==7:
                # print(prom,"Erfolg")
                # print("yes")
                break
        # print(prom)
        # print(self.peaks)
        

    def plot(self,xlabel=None,ylabel1=None,ylabel2=None,title=None,figsize=(8,5),ScopeSettings=False):
        '''ScopeSettings gibt an, ob Oszi-Fenster wie im Praktikum dargestellt werden soll.'''
        fig, ax1 = plt.subplots(figsize=figsize)
        ax2 = ax1.twinx()
        if ScopeSettings == True:
            '''Bin mir nicht ganz sicher, ob das so passt. Wahrscheinliche automatische Anpassung besser'''
            offset1 = float(linecache.getline(self.scope,3).split()[1])
            offset2 = float(linecache.getline(self.scope,11).split()[1])
            # print(offset1)
            # print(offset2)
            ax1.plot(self.time,self.ch1+offset1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2+offset2,label='Channel 2',color="C1")
            ax2.scatter(self.time[self.peaks],self.ch2[self.peaks]+offset2,label='Channel 2',color='C2')
        else:
            ax1.plot(self.time,self.ch1,label='Channel 1',color='C0')
            ax2.plot(self.time,self.ch2,label='Channel 2',color='C1')
            ax2.scatter(self.time[self.peaks],self.ch2[self.peaks],label='Channel 2',color='C1')
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
def I_to_B(I):
    return 

def main():
    # a=Oszi("data/g_faktor/B_rampe/500kHz")
    # a.plot(ScopeSettings=True,ylabel1="U in V Channel 1",ylabel2="U in V Channel 2",title="Orientierungsezit")
    # plt.show()
    f_list=np.append(750,np.arange(1000,10001,500))
    peak1=[]
    peak2=[]
    peak3=[]
    peak4=[]
    for f in f_list:
        a=Oszi(f"data/g_faktor/B_rampe/{f}kHz")
        print(len(a.peaks))
        peak1.append(a.ch1[a.peaks[1]])
        peak2.append(a.ch1[a.peaks[2]])
        peak3.append(a.ch1[a.peaks[4]])
        peak4.append(a.ch1[a.peaks[5]])
    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(8, 5)
    fig1 = fig.add_subplot(gs[:, :])
    fig1.set_title("g-Faktor Bestimmung mittels Magnetfeldrampe")
    fig1.set_ylabel("I in A")
    fig1.set_xlabel("Frequenz in Hz")
    fig1.scatter(f_list,peak1,c="C0",label="1. Peak")
    fig1.scatter(f_list,peak2,c="C1",label="2. Peak")
    fig1.scatter(f_list,peak3,c="C2",label="3. Peak")
    fig1.scatter(f_list,peak4,c="C3",label="4. Peak")
    plt.tight_layout()
    plt.legend()
    # plt.savefig("plots/leckrate/leckrate.pdf")
    plt.show()





if __name__=="__main__":
    main()