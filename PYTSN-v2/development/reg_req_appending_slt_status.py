import sys
import numpy as np
import pandas as pd

class gcl_packet():
    """ A very simple class that represents a gcl packet.
    """
    def __init__(self, CT=10e-3):

        self.slt_time =  1e-3
        self.gard_band = 5e-6
        self.trml_type = "ST"
        self.trml_slot = None
        
        self.n_slt = int(1.0*CT/self.slt_time)

        self.ctrl_list = pd.DataFrame()
        #self.ctrl_list["q4"]=(np.zeros(self.n_slt))
        self.ctrl_list["q4"]=(np.zeros(self.n_slt))
        self.ctrl_list["q3"]=(np.zeros(self.n_slt))
        self.ctrl_list["q2"]=(np.zeros(self.n_slt))
        self.ctrl_list["q1"]=(np.zeros(self.n_slt))
        self.ctrl_list["q_nm"]=(np.insert(np.zeros(self.n_slt-1),0,1))
        self.ctrl_list["q_be"]=(np.insert(np.ones(self.n_slt-1),0,0))

gcl_pkt = gcl_packet(10e-3)
df = gcl_pkt.ctrl_list.copy()
print df
df = df.drop(["q_be"],axis=1).copy()
df = df.sum(axis=1).copy()
df = df.clip(upper=1).copy()
#df = df.replace({0:1, 1:0})
slt_status = df.tolist()
result = []
print slt_status

print df
