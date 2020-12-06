### Network Description File ### ned-ds

### Components

## TCPS

# 3 <-> 7
tcps_3 = tcps(pytsn,id=3,lan_id=1,dest_id=7,initial_delay=0-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True) #burst_count=10=>10Mbps

tcps_7 = tcps(pytsn,id=7,lan_id=1,dest_id=3,initial_delay=0-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True)

# 8 <-> 5
tcps_8 = tcps(pytsn,id=8,lan_id=1,dest_id=5,initial_delay=0-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True)

tcps_5 = tcps(pytsn,id=5,lan_id=1,dest_id=8,initial_delay=0-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True)

# 1 <-> 4
tcps_1 = tcps(pytsn,id=1,lan_id=1,dest_id=4,initial_delay=0e-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True)

tcps_4 = tcps(pytsn,id=4,lan_id=1,dest_id=1,initial_delay=0e-3,priority=0,rate=1000,\
	pkt_size=100,burst_count=1250,finish=10,debug=True)

## BE terminals
dist_be = poisson(rate_parameter=1e2, size_in_bytes=100)

# 2,6,9 -> 10
be_2 = terminal(pytsn,id=2,lan_id=1,dest_id=10,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=110,rate=1000,debug=False)

be_6 = terminal(pytsn,id=6,lan_id=1,dest_id=10,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=110,rate=1000,debug=False)

be_9 = terminal(pytsn,id=9,lan_id=1,dest_id=10,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=110,rate=1000,debug=False)

be_10 = terminal(pytsn,id=10,lan_id=1,dest_id=10,flow_id= -1,priority=0,\
	adist=dist_be.adist,sdist=dist_be.sdist,initial_delay=110,rate=1000,debug=True)

## Switches 

# Switches
scl_gp = 10e-3 # CT of TAS (gp: gate period)
scl_gl_netm = 25e-6  # slot-width for network management traffic
scl_gl_tcps = 1000e-6+25e-6  # slot-width for a TCPS pair
scl_gbnd = 5e-6 # guard band, offset used for sending data in a slot
scl_ns = 5 # no of TCPS pairs to support

sw_0_fwd_tbl = {1:1, 2:2, 3:3, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4, 10:4} # dst-id:output-port
sw_0 = switch_ds(pytsn,sw_0_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["ST","BE","ST","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=0)

sw_1_fwd_tbl = {1:1, 2:1, 3:1, 4:2, 5:4, 6:4, 7:2, 8:3, 9:4, 10:3} # dst-id:output-port
sw_1 = switch_ds(pytsn,sw_1_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","BE","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=1)

sw_2_fwd_tbl = {1:1, 2:1, 3:1, 4:1, 5:4, 6:4, 7:1, 8:1, 9:2, 10:1} # dst-id:output-port
sw_2 = switch_ds(pytsn,sw_2_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","BE","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=2)

sw_3_fwd_tbl = {1:1, 2:1, 3:1, 4:1, 5:2, 6:3, 7:1, 8:1, 9:1, 10:1} # dst-id:output-port
sw_3 = switch_ds(pytsn,sw_3_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","ST","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=3)

#[updated]

sw_4_fwd_tbl = {1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:1, 9:2, 10:3} # dst-id:output-port
sw_4 = switch_ds(pytsn,sw_4_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["ST","BE","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=4)

sw_5_fwd_tbl = {1:3, 2:3, 3:3, 4:2, 5:3, 6:3, 7:2, 8:3, 9:3, 10:3}# dst-id:output-port
sw_5 = switch_ds(pytsn,sw_5_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","BE","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=5)

sw_6_fwd_tbl = {1:3, 2:3, 3:3, 4:4, 5:3, 6:3, 7:2, 8:3, 9:3, 10:3} # dst-id:output-port
sw_6 = switch_ds(pytsn,sw_6_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","ST","BE","BE"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=6)

sw_7_fwd_tbl = {1:1, 2:1, 3:1, 4:4, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1} # dst-id:output-port
sw_7 = switch_ds(pytsn,sw_7_fwd_tbl,txq_limit=1000,pro_delay=0.5e-6,rate=1000,\
	list_prt_types=["BE","BE","BE","ST"],scl_gp=scl_gp,scl_gl_netm=scl_gl_netm,\
	scl_gl_tcps=scl_gl_tcps,scl_gbnd=scl_gbnd,scl_ns=scl_ns,sw_id=7)

## Links [updated]
link_latency=100e-9; link_jitter = 0; link_loss = 0; link_qlimit = 200; 
link_list = [link(pytsn, latency=link_latency, jitter=link_jitter, 
	loss=link_loss, qlimit=link_qlimit) for _ in range(40)]

### component wiring (experiment-A)

## Terminal Connections

# id:1 to sw-0(p1)
tcps_1.output = link_list[0].input
link_list[0].output = sw_0.p1_in
sw_0.p1_out = link_list[1].input
link_list[1].output = tcps_1.input

# id:2 to sw-0(p2)
be_2.output = link_list[2].input
link_list[2].output = sw_0.p2_in
sw_0.p2_out = link_list[3].input
link_list[3].output = be_2.input

# id:3 to sw-0(p3)
tcps_3.output = link_list[4].input
link_list[4].output = sw_0.p3_in
sw_0.p3_out = link_list[5].input
link_list[5].output = tcps_3.input

# id:7 to sw-1(p2) [updated]
tcps_7.output = link_list[6].input
link_list[6].output = sw_6.p2_in
sw_6.p2_out = link_list[7].input
link_list[7].output = tcps_7.input

# id:8 to sw-1(p3) [updated]
tcps_8.output = link_list[8].input
link_list[8].output = sw_4.p1_in
sw_4.p1_out = link_list[9].input
link_list[9].output = tcps_8.input

# id:9 to sw-2(p2)
be_9.output = link_list[10].input
link_list[10].output = sw_2.p2_in
sw_2.p2_out = link_list[11].input
link_list[11].output = be_9.input

# id:10 to sw-2(p3) [updated]
be_10.output = link_list[12].input
link_list[12].output = sw_4.p3_in
sw_4.p3_out = link_list[13].input
link_list[13].output = be_10.input

# id:5 to sw-3(p2)
tcps_5.output = link_list[14].input
link_list[14].output = sw_3.p2_in
sw_3.p2_out = link_list[15].input
link_list[15].output = tcps_5.input

# id:6 to sw-3(p3)
be_6.output = link_list[16].input
link_list[16].output = sw_3.p3_in
sw_3.p3_out = link_list[17].input
link_list[17].output = be_6.input

# id:4 to sw-3(p4) [updated]
tcps_4.output = link_list[18].input
link_list[18].output = sw_7.p4_in
sw_7.p4_out = link_list[19].input
link_list[19].output = tcps_4.input

## Switch-Wiring

# old
sw_0.p4_out = link_list[25].input
link_list[25].output = sw_1.p1_in
sw_1.p1_out = link_list[26].input
link_list[26].output = sw_0.p4_in

sw_1.p4_out = link_list[27].input
link_list[27].output = sw_2.p1_in
sw_2.p1_out = link_list[28].input
link_list[28].output = sw_1.p4_in

sw_2.p4_out = link_list[29].input
link_list[29].output = sw_3.p1_in
sw_3.p1_out = link_list[30].input
link_list[30].output = sw_2.p4_in

# new-addition
sw_1.p3_out = link_list[31].input
link_list[31].output = sw_4.p2_in
sw_4.p2_out = link_list[32].input
link_list[32].output = sw_1.p3_in

sw_1.p2_out = link_list[33].input
link_list[33].output = sw_5.p3_in
sw_3.p3_out = link_list[34].input
link_list[34].output = sw_1.p2_in

sw_5.p2_out = link_list[35].input
link_list[35].output = sw_6.p3_in
sw_6.p3_out = link_list[36].input
link_list[36].output = sw_5.p2_in

sw_6.p4_out = link_list[37].input
link_list[37].output = sw_7.p1_in
sw_7.p1_out = link_list[38].input
link_list[38].output = sw_6.p4_in