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
        self.ctrl_list["q4"]=(np.zeros(self.n_slt))
        self.ctrl_list["q3"]=(np.zeros(self.n_slt))
        self.ctrl_list["q2"]=(np.zeros(self.n_slt))
        self.ctrl_list["q1"]=(np.zeros(self.n_slt))
        self.ctrl_list["q_nm"]=(np.insert(np.zeros(self.n_slt-1),0,1))
        self.ctrl_list["q_be"]=(np.insert(np.ones(self.n_slt-1),0,0))

gcl_pkt = gcl_packet(10e-3)
gcl_A = gcl_pkt
gcl_B = gcl_pkt
gcl_C = gcl_pkt
gcl_D = gcl_pkt
GCL = {"gclA":gcl_A, "gclB":gcl_B, "gcl_c":gcl_C, "gcl_D":gcl_D}
print GCL["gclA"].ctrl_list
