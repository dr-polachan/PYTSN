### Network Description File ### Conf-1

## Components

# TCPS terminal
#tcps = tcps(pytsn,id=1,dest_id=2,priority=0,start_time=0,stop_time=float("inf"),\
#        rate=1000,debug=True,pkt_size=100,burst_count=5)

# ST terminals
dist_st = const(inter_arr_time=10e-3, size_in_bytes=100)

# 2 <-> 5
st = terminal(pytsn,id=2,dest_id=1,flow_id= 1,priority=1, adist=dist_st.adist,\
	sdist=dist_st.sdist, start_time=0e-3, stop_time=float('inf'), rate=1000, \
	debug=True,type="data")

# rx block
rcv = rx(pytsn)

st.output = rcv.input
#tcps.output = st.input