### Network Description File ### 


# BE terminals

dist_be = poisson(rate_parameter=1e5, size_in_bytes=100)


hBE3 = terminal(pytsn, id=3, dest_id=4, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=True,type="data",data="None")

hBE4 = terminal(pytsn, id=4, dest_id=3, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=True,type="data",data="None")


# TCPS terminals
hTCPS1 = tcps(pytsn,id=1,dest_id=2,priority=0,start_time=0,stop_time=100,\
        rate=1000,debug=True,pkt_size=100,burst_count=100)

hTCPS2 = tcps(pytsn,id=2,dest_id=1,priority=0,start_time=0,stop_time=300e-3,\
        rate=1000,debug=True,pkt_size=100,burst_count=100)

# Switches
fwd_tbl = { 1: 1, 2: 2, 3: 3, 4: 2 } # dst-id:output-port
sw1 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=None, pro_delay=0, \
        list_prt_types=["ST","BE","BE","BE"], list_trmnl_ids=[1, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=1)

fwd_tbl = { 1: 1, 2: 2, 3: 1, 4: 3 } # dst-id:output-port
sw2 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=None, pro_delay=0, \
        list_prt_types=["BE","ST","BE","BE"], list_trmnl_ids=[None, 2, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=2)

# Connections
hTCPS1.output = sw1.p1_in 
sw1.p1_out = hTCPS1.input

sw1.p2_out = sw2.p1_in
sw2.p1_out = sw1.p2_in

sw2.p2_out = hTCPS2.input 
hTCPS2.output = sw2.p2_in

# Connection (BE terminals)
hBE3.output = sw1.p3_in 
sw1.p3_out = hBE3.input

hBE4.output = sw2.p3_in 
sw2.p3_out = hBE4.input