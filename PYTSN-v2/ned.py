### Network Description File ### 

## ST terminals

# room-4
st_1 = tcps(pytsn,id=1,dest_id=2,priority=0,start_time=0,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=1000)

st_2 = tcps(pytsn,id=2,dest_id=1,priority=0,start_time=100e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=1000)

# room-5
st_26 = tcps(pytsn,id=26,dest_id=27,priority=0,start_time=1400e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=1000)

st_27 = tcps(pytsn,id=27,dest_id=26,priority=0,start_time=1500e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=1000)


# room-3 and 6
st_4 = tcps(pytsn,id=4,dest_id=23,priority=0,start_time=200e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_5 = tcps(pytsn,id=5,dest_id=24,priority=0,start_time=300e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_23 = tcps(pytsn,id=23,dest_id=4,priority=0,start_time=1200e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_24 = tcps(pytsn,id=24,dest_id=5,priority=0,start_time=1300e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

# room-2 and 8
st_7 = tcps(pytsn,id=7,dest_id=17,priority=0,start_time=400e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_8 = tcps(pytsn,id=8,dest_id=18,priority=0,start_time=500e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_17 = tcps(pytsn,id=17,dest_id=7,priority=0,start_time=800e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_18 = tcps(pytsn,id=18,dest_id=8,priority=0,start_time=900e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

# room-1 and 7
st_10 = tcps(pytsn,id=10,dest_id=20,priority=0,start_time=600e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_11 = tcps(pytsn,id=11,dest_id=21,priority=0,start_time=700e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_20 = tcps(pytsn,id=20,dest_id=10,priority=0,start_time=1000e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

st_21 = tcps(pytsn,id=21,dest_id=11,priority=0,start_time=1100e-3,stop_time=300,\
        rate=1000,debug=True,pkt_size=100,burst_count=10)

## BE terminals

dist_be = poisson(rate_parameter=1e4, size_in_bytes=1000)
dbug_be = True

be_0 = terminal(pytsn, id=0, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=250, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_13 = terminal(pytsn, id=13, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_14 = terminal(pytsn, id=14, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_15 = terminal(pytsn, id=15, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_16 = terminal(pytsn, id=16, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_3 = terminal(pytsn, id=3, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_28 = terminal(pytsn, id=28, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_6 = terminal(pytsn, id=6, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_25 = terminal(pytsn, id=25, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

# room-2 and 8
be_9 = terminal(pytsn, id=9, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_19 = terminal(pytsn, id=19, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

# room-1 and 7
be_12 = terminal(pytsn, id=12, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

be_22 = terminal(pytsn, id=22, dest_id=0, flow_id=-1, priority=0,\
     adist=dist_be.adist, sdist=dist_be.sdist, start_time=0, stop_time=300, rate=1000,\
     debug=dbug_be,type="data",data="None")

## Switches
fwd_tbl = { 0: 3, 4: 1, 5: 1, 23: 2, 24: 2, 17: 2, 18: 2, 7: 1, 8: 1, 20: 2, 21: 2, 10: 1, 11: 1 } # dst-id:output-port
s_0 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=0)

fwd_tbl = { 0: 1, 4: 4, 5: 4, 23: 1, 24: 1 } # dst-id:output-port
s_11 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=11)

fwd_tbl = { 0: 1, 4: 2, 5: 2, 23: 1, 24: 1, 17: 1, 18: 1, 7: 3, 8: 3, 20: 1, 21: 1, 10: 3, 11: 3} # dst-id:output-port
s_12 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=12)

fwd_tbl = { 0: 1, 17: 1, 18: 1, 7: 3, 8: 3, 20: 1, 21: 1, 10: 4, 11: 4 } # dst-id:output-port
s_13 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=13)

fwd_tbl = { 0: 1, 17: 3, 18: 3, 7: 1, 8: 1, 20: 4, 21: 4, 10: 1, 11: 1 } # dst-id:output-port
s_21 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=21)

fwd_tbl = { 0: 1, 4:1, 5:1, 23:3, 24:3, 17: 2, 18: 2, 7: 1, 8: 1, 20: 2, 21: 2, 10: 1, 11: 1 } # dst-id:output-port
s_22 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=22)

fwd_tbl = { 0: 1, 4: 1, 5: 1, 23:3, 24:3 } # dst-id:output-port
s_23 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=23)


fwd_tbl = { 0: 3, 2: 1, 1: 2 } # dst-id:output-port
s_111 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[2, 1, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=111)

fwd_tbl = { 0: 3, 27: 1, 26: 2 } # dst-id:output-port
s_232 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[27, 26, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=232)


fwd_tbl = { 0: 3, 23: 3, 24: 3, 5: 1, 4: 2 } # dst-id:output-port
s_112 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[5, 4, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=112)

fwd_tbl = { 0: 3, 4: 3, 5: 3,  23: 2, 24:1 } # dst-id:output-port
s_231 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[24, 23, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=231)

# room-2
fwd_tbl = { 0: 3, 17: 3, 18: 3, 8: 1, 7: 2 } # dst-id:output-port
s_131 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[8, 7, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=131)
# room-8
fwd_tbl = { 0: 3, 7: 3, 8: 3, 18: 1, 17: 2  } # dst-id:output-port
s_211 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[18, 17, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=211)

# room-1
fwd_tbl = { 0: 3, 20: 3, 21: 3, 11: 1, 10: 2 } # dst-id:output-port
s_132 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[11, 10, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=132)
# room-7
fwd_tbl = { 0: 3, 10: 3, 11: 3, 21: 1, 20: 2  } # dst-id:output-port
s_212 = switch(pytsn, fwd_tbl=fwd_tbl, txq_limit=1000, pro_delay=0.5e-6, \
        list_prt_types=["ST","ST","BE","BE"], list_trmnl_ids=[21, 20, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=212)


## link-definition
link_latency=0.5e-6; link_jitter = 0; link_loss = 0; link_qlimit = 200; 
link_list = [link(pytsn, latency=link_latency, jitter=link_jitter, 
    loss=link_loss, qlimit=link_qlimit) for _ in range(90)]


## Switch Connections
# s_12 <-> s_0
s_12.p1_out = link_list[0].input
link_list[0].output = s_0.p1_in
s_0.p1_out = link_list[1].input
link_list[1].output = s_12.p1_in

# s_0 <-> s_22
s_0.p2_out = link_list[2].input
link_list[2].output = s_22.p1_in
s_22.p1_out = link_list[3].input
link_list[3].output = s_0.p2_in

# s_22 <-> s_21
s_22.p2_out = link_list[4].input
link_list[4].output = s_21.p1_in
s_21.p1_out = link_list[5].input
link_list[5].output = s_22.p2_in

# s_22 <-> s_23
s_22.p3_out = link_list[6].input
link_list[6].output = s_23.p1_in
s_23.p1_out = link_list[7].input
link_list[7].output = s_22.p3_in

# s_12 <-> s_11
s_12.p2_out = link_list[8].input
link_list[8].output = s_11.p1_in
s_11.p1_out = link_list[9].input
link_list[9].output = s_12.p2_in

# s_12 <-> s_13
s_12.p3_out = link_list[10].input
link_list[10].output = s_13.p1_in
s_13.p1_out = link_list[11].input
link_list[11].output = s_12.p3_in

# Switch to Terminal Connections
be_0.output = link_list[12].input
link_list[12].output = s_0.p3_in
s_0.p3_out = link_list[13].input
link_list[13].output = be_0.input

be_13.output = link_list[14].input
link_list[14].output = s_11.p2_in
s_11.p2_out = link_list[15].input
link_list[15].output = be_13.input

be_14.output = link_list[16].input
link_list[16].output = s_13.p2_in
s_13.p2_out = link_list[17].input
link_list[17].output = be_14.input

be_15.output = link_list[18].input
link_list[18].output = s_21.p2_in
s_21.p2_out = link_list[19].input
link_list[19].output = be_15.input

be_16.output = link_list[20].input
link_list[20].output = s_23.p2_in
s_23.p2_out = link_list[21].input
link_list[21].output = be_16.input


# Room-4 connections
s_111.p3_out = link_list[22].input
link_list[22].output = s_11.p3_in
s_11.p3_out = link_list[23].input
link_list[23].output = s_111.p3_in


be_3.output = link_list[24].input
link_list[24].output = s_111.p4_in
s_111.p4_out = link_list[25].input
link_list[25].output = be_3.input


st_1.output = link_list[26].input
link_list[26].output = s_111.p2_in
s_111.p2_out = link_list[27].input
link_list[27].output = st_1.input

st_2.output = link_list[28].input
link_list[28].output = s_111.p1_in
s_111.p1_out = link_list[29].input
link_list[29].output = st_2.input

# Room-5 connections
s_232.p3_out = link_list[30].input
link_list[30].output = s_23.p4_in
s_23.p4_out = link_list[31].input
link_list[31].output = s_232.p3_in


be_28.output = link_list[32].input
link_list[32].output = s_232.p4_in
s_232.p4_out = link_list[33].input
link_list[33].output = be_28.input


st_26.output = link_list[34].input
link_list[34].output = s_232.p2_in
s_232.p2_out = link_list[35].input
link_list[35].output = st_26.input

st_27.output = link_list[36].input
link_list[36].output = s_232.p1_in
s_232.p1_out = link_list[37].input
link_list[37].output = st_27.input


# Room-3 connections
s_112.p3_out = link_list[38].input
link_list[38].output = s_11.p4_in
s_11.p4_out = link_list[39].input
link_list[39].output = s_112.p3_in

be_6.output = link_list[40].input
link_list[40].output = s_112.p4_in
s_112.p4_out = link_list[41].input
link_list[41].output = be_6.input

st_4.output = link_list[42].input
link_list[42].output = s_112.p2_in
s_112.p2_out = link_list[43].input
link_list[43].output = st_4.input

st_5.output = link_list[44].input
link_list[44].output = s_112.p1_in
s_112.p1_out = link_list[45].input
link_list[45].output = st_5.input

# Room-6 connections
s_231.p3_out = link_list[46].input
link_list[46].output = s_23.p3_in
s_23.p3_out = link_list[47].input
link_list[47].output = s_231.p3_in

be_25.output = link_list[48].input
link_list[48].output = s_231.p4_in
s_231.p4_out = link_list[49].input
link_list[49].output = be_25.input

st_23.output = link_list[50].input
link_list[50].output = s_231.p2_in
s_231.p2_out = link_list[51].input
link_list[51].output = st_23.input

st_24.output = link_list[52].input
link_list[52].output = s_231.p1_in
s_231.p1_out = link_list[53].input
link_list[53].output = st_24.input


# Room-2 connections
s_131.p3_out = link_list[54].input
link_list[54].output = s_13.p3_in
s_13.p3_out = link_list[55].input
link_list[55].output = s_131.p3_in

be_9.output = link_list[56].input
link_list[56].output = s_131.p4_in
s_131.p4_out = link_list[57].input
link_list[57].output = be_9.input

st_7.output = link_list[58].input
link_list[58].output = s_131.p2_in
s_131.p2_out = link_list[59].input
link_list[59].output = st_7.input

st_8.output = link_list[60].input
link_list[60].output = s_131.p1_in
s_131.p1_out = link_list[61].input
link_list[61].output = st_8.input

# Room-8 connections
s_211.p3_out = link_list[62].input
link_list[62].output = s_21.p3_in
s_21.p3_out = link_list[63].input
link_list[63].output = s_211.p3_in

be_19.output = link_list[64].input
link_list[64].output = s_211.p4_in
s_211.p4_out = link_list[65].input
link_list[65].output = be_19.input

st_17.output = link_list[66].input
link_list[66].output = s_211.p2_in
s_211.p2_out = link_list[67].input
link_list[67].output = st_17.input

st_18.output = link_list[68].input
link_list[68].output = s_211.p1_in
s_211.p1_out = link_list[69].input
link_list[69].output = st_18.input


# Room-1 connections
s_132.p3_out = link_list[70].input
link_list[70].output = s_13.p4_in
s_13.p4_out = link_list[71].input
link_list[71].output = s_132.p3_in

be_12.output = link_list[72].input
link_list[72].output = s_132.p4_in
s_132.p4_out = link_list[73].input
link_list[73].output = be_12.input

st_10.output = link_list[74].input
link_list[74].output = s_132.p2_in
s_132.p2_out = link_list[75].input
link_list[75].output = st_10.input

st_11.output = link_list[76].input
link_list[76].output = s_132.p1_in
s_132.p1_out = link_list[77].input
link_list[77].output = st_11.input

# Room-7 connections
s_212.p3_out = link_list[78].input
link_list[78].output = s_21.p4_in
s_21.p4_out = link_list[79].input
link_list[79].output = s_212.p3_in

be_22.output = link_list[80].input
link_list[80].output = s_212.p4_in
s_212.p4_out = link_list[81].input
link_list[81].output = be_22.input

st_20.output = link_list[82].input
link_list[82].output = s_212.p2_in
s_212.p2_out = link_list[83].input
link_list[83].output = st_20.input

st_21.output = link_list[84].input
link_list[84].output = s_212.p1_in
s_212.p1_out = link_list[85].input
link_list[85].output = st_21.input