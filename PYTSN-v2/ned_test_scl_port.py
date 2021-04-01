### Network Description File ### Conf-1

## Components
import pandas as pd
import numpy as np

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
ds = debug_sink(pytsn)

obj_rx = rx(pytsn)
obj_tx =  tx(pytsn)
obj_pcl = pcl(pytsn) 
obj_port = port(pytsn,prt_type="ST")
obj_scl = scl(pytsn)

#obj_rx.out_fid_log = obj_pcl.in_fid_log

#st.output = obj_port.in_tx
obj_port.out_tx = ds.input



#obj_pcl.out_gc = obj_tx.in_gc

#var_gc = [-1, 0]
#obj_tx.in_gc.put(var_gc)

#gcl_pkt = gcl_packet()
obj_scl.out_gclA = obj_port.in_gcl
#obj_port.in_gcl.put(gcl_pkt)

#st.output = rcv.input
#tcps.output = st.input