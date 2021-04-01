### Network Description File ### Conf-1

## Components
import pandas as pd
import numpy as np
class gcl_packet(object):
    """ A very simple class that represents a gcl packet.
    """
    def __init__(self):
            
        self.ctrl_list = pd.DataFrame()
        self.ctrl_list["q4"]=(np.zeros(10))
        self.ctrl_list["q3"]=(np.zeros(10))
        self.ctrl_list["q2"]=(np.zeros(10))
        self.ctrl_list["q1"]=(np.zeros(10))
        self.ctrl_list["q_nm"]=(np.array((0,0,0,1,1,5,6,7,8,9)))
        self.ctrl_list["q_be"]=(np.zeros(10))

        self.slt_time =  1e-3
        self.gard_band = 1e-6
        self.trml_type = "ST"
        self.trml_slot = 1

# TCPS terminal
#tcps = tcps(pytsn,id=1,dest_id=2,priority=0,start_time=0,stop_time=float("inf"),\
#        rate=1000,debug=True,pkt_size=100,burst_count=5)

# ST terminals
dist_st = const(inter_arr_time=10e-3, size_in_bytes=100)

# 2 <-> 5
st = terminal(pytsn,id=2,dest_id=1,flow_id=0,priority=1, adist=dist_st.adist,\
	sdist=dist_st.sdist, start_time=0e-3, stop_time=float('inf'), rate=1000, \
	debug=True,type="data")

ts = traffic_sink(pytsn,id=1,debug=True)

obj_rx = rx(pytsn)
obj_tx =  tx(pytsn)
obj_pcl = pcl(pytsn) 

#obj_rx.out_fid_log = obj_pcl.in_fid_log

st.output = obj_tx.input
obj_tx.output = ts.input



obj_pcl.out_gc = obj_tx.in_gc

#var_gc = [-1, 0]
#obj_tx.in_gc.put(var_gc)

gcl_pkt = gcl_packet()
obj_pcl.in_gcl.put(gcl_pkt)

#st.output = rcv.input
#tcps.output = st.input