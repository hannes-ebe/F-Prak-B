import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class fourier:
    def __init__(self,f: float,max_n: int,t: np.ndarray) -> None:
        self.f=f
        self.max_n=max_n
        self.U=self.get_U()
        
        pass

    def get_U(self):
        U_arr=np.zeros(len(self.t))
        for ti,t in enumerate(self.t):
            for n in range(self.max_n):
                U_arr[it]+=4/(np.pi*)




    def plot(self):
        plt.plot(t,)



def main():
    pass


if __name__=="__main__":
    main()