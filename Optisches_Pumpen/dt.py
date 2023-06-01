import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class fourier:
    def __init__(self,f: float,max_n: int,t: np.ndarray) -> None:
        self.f=f
        self.omega=2*np.pi*self.f
        self.max_n=max_n
        self.t=t
        self.U=self.get_U()
        self.plot()
        pass

    def get_U(self):
        U_arr=np.zeros(len(self.t))
        for ti,t in enumerate(self.t):
            for n in range(1,self.max_n):
                U_arr[ti]+=np.sin((2*n-1)*self.omega*t)/(2*n-1)
        return U_arr




    def plot(self):
        plt.plot(self.t,self.U)
        plt.show()



def main():
    fourier(0.25,1000,np.arange(0,10,0.01))


if __name__=="__main__":
    main()