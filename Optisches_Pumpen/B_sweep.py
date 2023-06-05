import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import linecache
from scipy.optimize import curve_fit
from scipy.stats import linregress
from scipy.signal import find_peaks
from scipy.constants import mu_0
import scipy.constants as const

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
            ax1.plot(self.time,self.ch1+offset1,label='Magnetfeld Spannung',color='C0')
            ax2.plot(self.time,self.ch2+offset2,label='Photodiodenspannung',color="C1")
            ax2.scatter(self.time[self.peaks],self.ch2[self.peaks]+offset2,label='Peaks in der Photodiodenspannung',color='C2')
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
        plt.savefig("figures/B_sweep_bsp.pdf")
        return fig, ax1, ax2
def I_to_B(I):
    N=80
    r=0.09
    return (4/5)**(3/2)*N/r*I*const.mu_0
def U_to_I(U):
    R=1.7223
    return U/R

def U_to_B(U):
    return I_to_B(U_to_I(U))

def main():
    a=Oszi("data/g_faktor/B_rampe/1000kHz")
    a.plot(ScopeSettings=True,ylabel1="Ch1 U in V",ylabel2="Ch2 U in V",title="Magnetfeldrampe bei 1MHz")
    plt.show()
    f_list=np.append(750,np.arange(1000,10001,500))
    peak1=[]
    peak2=[]
    peak3=[]
    peak4=[]
    for f in f_list:
        a=Oszi(f"data/g_faktor/B_rampe/{f}kHz")
        # print(len(a.peaks))
        peak1.append(a.ch1[a.peaks[1]])
        peak2.append(a.ch1[a.peaks[2]])
        peak3.append(a.ch1[a.peaks[4]])
        peak4.append(a.ch1[a.peaks[5]])
    reg1=linregress(np.append(-f_list,f_list),np.append(U_to_B(np.array(peak1)),U_to_B(np.array(peak4))))
    f_reg1= lambda f: f*reg1.slope+reg1.intercept
    reg2=linregress(np.append(-f_list,f_list),np.append(U_to_B(np.array(peak2)),U_to_B(np.array(peak3))))
    f_reg2= lambda f: f*reg2.slope+reg2.intercept
    g1=const.Planck/(const.physical_constants["Bohr magneton"][0]*reg2.slope*1e-3)
    g1_err=const.Planck/(const.physical_constants["Bohr magneton"][0]*reg2.slope**2*1e-3)*reg2.stderr
    print(f"G1 ist {g1} pm {g1_err}")

    g2=const.Planck/(const.physical_constants["Bohr magneton"][0]*reg1.slope*1e-3)
    g2_err=const.Planck/(const.physical_constants["Bohr magneton"][0]*reg1.slope**2*1e-3)*reg2.stderr
    print(f"G2 ist {g2} pm {g2_err}")

    fig = plt.figure(figsize=(11, 6))
    gs = GridSpec(8, 5)
    fig1 = fig.add_subplot(gs[:, :])
    fig1.set_title("g-Faktor Bestimmung mittels Magnetfeldrampe")
    fig1.set_ylabel("B in T")
    fig1.set_xlabel("Frequenz in kHz")
    fig1.scatter(np.append(-f_list,f_list),np.append(U_to_B(np.array(peak1)),U_to_B(np.array(peak4))),c="C0",label="RB$^{85}$")
    fig1.scatter(np.append(-f_list,f_list),np.append(U_to_B(np.array(peak2)),U_to_B(np.array(peak3))),c="C1",label="Rb$^{87}$")
    fig1.plot(np.append(-f_list,f_list),f_reg1(np.append(-f_list,f_list)),c="C0")
    fig1.plot(np.append(-f_list,f_list),f_reg2(np.append(-f_list,f_list)),c="C1")
    # fig1.plot(f_list,f_reg3(f_list),c="C2")
    # fig1.plot(f_list,f_reg4(f_list),c="C3")
    plt.tight_layout()
    plt.legend()
    plt.savefig("figures/B_sweep_ref.pdf")
    plt.show()





if __name__=="__main__":
    main()