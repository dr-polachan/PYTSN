import sys
import numpy as np
import pandas as pd

class gcl_packet(object):
    """ A very simple class that represents a gcl packet.
    """
    def __init__(self):
            
        self.ctrl_list = pd.DataFrame()
        self.ctrl_list["q4"]=(np.array((1,1,0,1,1,5,6,7,8,9)))
        self.ctrl_list["q3"]=(np.zeros(10))
        self.ctrl_list["q2"]=(np.zeros(10))
        self.ctrl_list["q1"]=(np.array((1,1,0,1,1,5,6,7,8,9)))
        self.ctrl_list["q_nm"]=(np.array((1,1,0,1,1,5,6,7,8,9)))
        self.ctrl_list["q_be"]=(np.array((1,1,0,1,1,5,6,7,8,9)))

        
        self.slt_time =  5e-3
        self.gard_band = 1e-6
        self.trml_type = "ST"
        self.trml_slot = 1
            
gcl_pkt = gcl_packet()

print gcl_pkt.ctrl_list

for i in range(1): #gcl_pkt.ctrl_list.shape[0]):

    gc = gcl_pkt.ctrl_list.copy()
    gc = gc.rename(columns={"q4":4,"q3":3,"q2":2,"q1":1,"q_nm":0,"q_be":-1})
    gc = gc.loc[i].copy()
    gc = pd.DataFrame(gc).transpose()
    gc = gc.loc[:, (gc != 0).any(axis=0)].copy() # remove coloumns with zero entries
    gc = gc.columns.tolist()
    gc = map(int, gc)

    #gc = gc.reindex(columns=[4,3,2,1,0,-1])
    #gc["id"] = [4,3,2,1,0,-1]
    print gc
    #print gcl_pkt.slt_time
    #a = [gc["q4"]*4, gc["q3"]*3, gc["q2"]*2, gc["q1"]*1, gc[q_nm]]
    #print a