### Network Description File ### Conf-1

## Components

# ST terminals
dist_st = const(inter_arr_time=1e-3, size_in_bytes=100)

# 2 <-> 5

st_2 = terminal(pytsn,id=2,lan_id=1,dest_id=5,flow_id= 1,priority=1,\
	adist=dist_st.adist,sdist=dist_st.sdist,initial_delay=0,rate=1000,debug=True)

st_5 = terminal(pytsn,id=5,lan_id=1,dest_id=2,flow_id= 1,priority=1,\
	adist=dist_st.adist,sdist=dist_st.sdist,initial_delay=0,rate=1000,debug=True)

# BE terminals
dist_be = poisson(rate_parameter=10e5, size_in_bytes=100)

# 1 <-> 4
be_1 = terminal(pytsn,id=1,lan_id=1,dest_id=4,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=10,rate=1000,debug=True)

be_4 = terminal(pytsn,id=4,lan_id=1,dest_id=1,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=10,rate=1000,debug=True)

# 3 <-> 6

be_3 = terminal(pytsn,id=3,lan_id=1,dest_id=6,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=10,rate=1000,debug=False)

be_6 = terminal(pytsn,id=6,lan_id=1,dest_id=3,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=10,rate=1000,debug=False)

# switches 

cmn_gcl_ts_list = [[1e-3]] # for CT = 10e-3
cmn_gcl_list = [[1,-1]]

#cmn_gcl_ts_list = [[20e-6],[980e-6]] # for CT = 10e-3
##cmn_gcl_ts_list = [[2.9e-6],[2.4e-6],[994.7e-6]] # for CT = 1e-3
##cmn_gcl_ts_list = [[2.9e-6],[2.4e-6],[44.7e-6]] # for CT=50us
#cmn_gcl_list = [[1],[-1]]

# first-switch
sw_0_fwd_tbl = {1:1, 2:2, 3:3, 4:4, 5:4, 6:4} # dst-id:output-port
sw_0 = switch_ss(pytsn,sw_0_fwd_tbl,qlimit=100, \
	gcl_ts_list=cmn_gcl_ts_list, gcl_list=cmn_gcl_list, rate=1000, pro_delay=0.5e-6)

# last-switch
sw_1_fwd_tbl = {4:4, 5:2, 6:3, 1:1, 2:1, 3:1} # dst-id:output-port
sw_1 = switch_ss(pytsn,sw_1_fwd_tbl,qlimit=100, \
	gcl_ts_list=cmn_gcl_ts_list, gcl_list=cmn_gcl_list, rate=1000, pro_delay=0.5e-6)


# Links
link_latency=100e-9; link_jitter = 0; link_loss = 0; link_qlimit = 200; 
link_list = [link(pytsn, latency=link_latency, jitter=link_jitter, 
	loss=link_loss, qlimit=link_qlimit) for _ in range(20)]


## component wiring (experiment-A)

# terminal connections

st_2.output = link_list[3].input
link_list[3].output = sw_0.p2_in
sw_0.p2_out = link_list[4].input
link_list[4].output = st_2.input

st_5.output = link_list[9].input
link_list[9].output = sw_1.p2_in
sw_1.p2_out = link_list[10].input
link_list[10].output = st_5.input

be_1.output = link_list[1].input
link_list[1].output = sw_0.p1_in
sw_0.p1_out = link_list[2].input
link_list[2].output = be_1.input

be_3.output = link_list[5].input
link_list[5].output = sw_0.p3_in
sw_0.p3_out = link_list[6].input
link_list[6].output = be_3.input

be_4.output = link_list[7].input
link_list[7].output = sw_1.p4_in
sw_1.p4_out = link_list[8].input
link_list[8].output = be_4.input

be_6.output = link_list[11].input
link_list[11].output = sw_1.p3_in
sw_1.p3_out = link_list[12].input
link_list[12].output = be_6.input

# switch-terminals

sw_0.p4_out = link_list[14].input
link_list[14].output = sw_1.p1_in
sw_1.p1_out = link_list[17].input
link_list[17].output = sw_0.p4_in








