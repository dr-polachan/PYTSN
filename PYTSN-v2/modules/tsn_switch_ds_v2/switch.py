""" The switch block. The block is built using the components 
    port, swfbric and SCL
"""

import simpy

from swfbric import swfbric
from scl import scl
from port import port

class switch(object):
    def __init__(self, env, fwd_tbl=None, txq_limit=None, pro_delay=0, \
        list_prt_types=["BE","BE","BE","BE"], list_trmnl_ids=[None, None, None, None],\
        CT=10e-3, list_prt_rates=[1000,1000,1000,1000],sw_id=None):
        
        self.env = env

        # parameters
        self.fwd_tbl = fwd_tbl
        self.txq_limit = txq_limit
        self.pro_delay = pro_delay
        self.list_prt_types = list_prt_types
        self.list_prt_rates = list_prt_rates
        self.list_trmnl_ids = list_trmnl_ids
        self.CT = CT
        self.sw_id = sw_id

        # variables
        self.prtA_type = self.list_prt_types[0]
        self.prtB_type = self.list_prt_types[1]
        self.prtC_type = self.list_prt_types[2]
        self.prtD_type = self.list_prt_types[3]

        self.prtA_rate = self.list_prt_rates[0]
        self.prtB_rate = self.list_prt_rates[1]
        self.prtC_rate = self.list_prt_rates[2]
        self.prtD_rate = self.list_prt_rates[3]

        # store resources
        self.sA1 = simpy.Store(env)
        self.sA2 = simpy.Store(env)
        self.sA3 = simpy.Store(env)
        self.sA4 = simpy.Store(env)
        self.sA5 = simpy.Store(env)
        self.sA6 = simpy.Store(env)


        self.sB1 = simpy.Store(env)
        self.sB2 = simpy.Store(env)
        self.sB3 = simpy.Store(env)
        self.sB4 = simpy.Store(env)
        self.sB5 = simpy.Store(env)
        self.sB6 = simpy.Store(env)


        self.sC1 = simpy.Store(env)
        self.sC2 = simpy.Store(env)
        self.sC3 = simpy.Store(env)
        self.sC4 = simpy.Store(env)
        self.sC5 = simpy.Store(env)
        self.sC6 = simpy.Store(env)


        self.sD1 = simpy.Store(env)
        self.sD2 = simpy.Store(env)
        self.sD3 = simpy.Store(env)
        self.sD4 = simpy.Store(env)
        self.sD5 = simpy.Store(env)
        self.sD6 = simpy.Store(env)


        self.SgA = simpy.Store(env)
        self.SgB = simpy.Store(env)
        self.SgC = simpy.Store(env)
        self.SgD = simpy.Store(env)

        self.SbA = simpy.Store(env)
        self.SbB = simpy.Store(env)
        self.SbC = simpy.Store(env)
        self.SbD = simpy.Store(env)


        # input connection's to store resources
        self.p1_in = self.sA1
        self.p2_in = self.sB1
        self.p3_in = self.sC1
        self.p4_in = self.sD1
        
        # output (should always be set to "None")
        self.p1_out = None
        self.p2_out = None
        self.p3_out = None
        self.p4_out = None

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.obj_prtA = port(env, prt_type=self.prtA_type, pro_delay=self.pro_delay,\
            txq_limit=self.txq_limit, rate=self.prtA_rate, prt_id=1, sw_id=self.sw_id)
        self.obj_prtA.out_rx = self.sA3; self.obj_prtA.out_tx = self.sA2
        self.obj_prtA.out_reg = self.sA5; self.obj_prtA.out_fid=self.sA6
        
        self.obj_prtB = port(env, prt_type=self.prtB_type, pro_delay=self.pro_delay,\
            txq_limit=self.txq_limit, rate=self.prtB_rate, prt_id=2, sw_id=self.sw_id)
        self.obj_prtB.out_rx = self.sB3; self.obj_prtB.out_tx = self.sB2
        self.obj_prtB.out_reg = self.sB5; self.obj_prtB.out_fid=self.sB6

        self.obj_prtC = port(env, prt_type=self.prtC_type, pro_delay=self.pro_delay,\
            txq_limit=self.txq_limit, rate=self.prtC_rate, prt_id=3, sw_id=self.sw_id)
        self.obj_prtC.out_rx = self.sC3; self.obj_prtC.out_tx = self.sC2
        self.obj_prtC.out_reg = self.sC5; self.obj_prtC.out_fid=self.sC6
        
        self.obj_prtD = port(env, prt_type=self.prtD_type, pro_delay=self.pro_delay,\
            txq_limit=self.txq_limit, rate=self.prtD_rate, prt_id=4, sw_id=self.sw_id)
        self.obj_prtD.out_rx = self.sD3; self.obj_prtD.out_tx = self.sD2
        self.obj_prtD.out_reg = self.sD5; self.obj_prtD.out_fid=self.sD6

        self.obj_core = swfbric(env, fwd_tbl=self.fwd_tbl); 
        self.obj_core.out_1 = self.sA4; self.obj_core.out_2 = self.sB4;
        self.obj_core.out_3 = self.sC4;self.obj_core.out_4 = self.sD4;

        self.obj_scl = scl(env, list_prt_types=self.list_prt_types, \
            list_trml_ids=self.list_trmnl_ids, CT=self.CT, fwd_tbl=self.fwd_tbl,\
            list_prt_rates=self.list_prt_rates,sw_id=self.sw_id)
        self.obj_scl.out_gclA = self.SgA
        self.obj_scl.out_gclB = self.SgB
        self.obj_scl.out_gclC = self.SgC
        self.obj_scl.out_gclD = self.SgD

        self.obj_scl.out_regA = self.SbA
        self.obj_scl.out_regB = self.SbB
        self.obj_scl.out_regC = self.SbC
        self.obj_scl.out_regD = self.SbD


        # running concurrent processes
        self.action = env.process(self.p_A1()) 
        self.action = env.process(self.p_A2()) 
        self.action = env.process(self.p_A3()) 
        self.action = env.process(self.p_A4()) 

        self.action = env.process(self.p_B1()) 
        self.action = env.process(self.p_B2()) 
        self.action = env.process(self.p_B3()) 
        self.action = env.process(self.p_B4()) 

        self.action = env.process(self.p_C1()) 
        self.action = env.process(self.p_C2()) 
        self.action = env.process(self.p_C3()) 
        self.action = env.process(self.p_C4()) 

        self.action = env.process(self.p_D1()) 
        self.action = env.process(self.p_D2()) 
        self.action = env.process(self.p_D3()) 
        self.action = env.process(self.p_D4()) 

        self.action = env.process(self.p_gA()) 
        self.action = env.process(self.p_gB()) 
        self.action = env.process(self.p_gC()) 
        self.action = env.process(self.p_gD()) 

        self.action = env.process(self.p_A5()) 
        self.action = env.process(self.p_B5()) 
        self.action = env.process(self.p_C5()) 
        self.action = env.process(self.p_D5()) 

        self.action = env.process(self.p_A6()) 
        self.action = env.process(self.p_B6()) 
        self.action = env.process(self.p_C6()) 
        self.action = env.process(self.p_D6())

        self.action = env.process(self.p_bA()) 
        self.action = env.process(self.p_bB()) 
        self.action = env.process(self.p_bC()) 
        self.action = env.process(self.p_bD()) 


    ## 
    def p_A1(self):
        while True:
            pkt = (yield self.sA1.get())
            self.obj_prtA.in_rx.put(pkt)
    def p_A2(self):
        while True:
            pkt = (yield self.sA2.get())
            if(self.p1_out != None):
                self.p1_out.put(pkt)
    def p_A3(self):
        while True:
            pkt = (yield self.sA3.get())
            self.obj_core.in_1.put(pkt)
    def p_A4(self):
        while True:
            pkt = (yield self.sA4.get())
            self.obj_prtA.in_tx.put(pkt)
    ##        
    def p_B1(self):
        while True:
            pkt = (yield self.sB1.get())
            self.obj_prtB.in_rx.put(pkt)
    def p_B2(self):
        while True:
            pkt = (yield self.sB2.get())
            if(self.p2_out != None):
                self.p2_out.put(pkt)
    def p_B3(self):
        while True:
            pkt = (yield self.sB3.get())
            self.obj_core.in_2.put(pkt)
    def p_B4(self):
        while True:
            pkt = (yield self.sB4.get())
            self.obj_prtB.in_tx.put(pkt)        

    ##        
    def p_C1(self):
        while True:
            pkt = (yield self.sC1.get())
            self.obj_prtC.in_rx.put(pkt)
    def p_C2(self):
        while True:
            pkt = (yield self.sC2.get())
            if(self.p3_out != None):
                self.p3_out.put(pkt)
    def p_C3(self):
        while True:
            pkt = (yield self.sC3.get())
            self.obj_core.in_3.put(pkt)
    def p_C4(self):
        while True:
            pkt = (yield self.sC4.get())
            self.obj_prtC.in_tx.put(pkt)
    
    ##        
    def p_D1(self):
        while True:
            pkt = (yield self.sD1.get())
            self.obj_prtD.in_rx.put(pkt)
    def p_D2(self):
        while True:
            pkt = (yield self.sD2.get())
            if(self.p4_out != None):
                self.p4_out.put(pkt)
    def p_D3(self):
        while True:
            pkt = (yield self.sD3.get())
            self.obj_core.in_4.put(pkt)
    def p_D4(self):
        while True:
            pkt = (yield self.sD4.get())
            self.obj_prtD.in_tx.put(pkt)

    ##   
    def p_gA(self):
        while True:
            pkt = (yield self.SgA.get())
            self.obj_prtA.in_gcl.put(pkt)
    def p_gB(self):
        while True:
            pkt = (yield self.SgB.get())
            self.obj_prtB.in_gcl.put(pkt)
    def p_gC(self):
        while True:
            pkt = (yield self.SgC.get())
            self.obj_prtC.in_gcl.put(pkt)
    def p_gD(self):
        while True:
            pkt = (yield self.SgD.get())
            self.obj_prtD.in_gcl.put(pkt)

    ##
    def p_A5(self):
        while True:
            pkt = (yield self.sA5.get())
            self.obj_scl.in_regA.put(pkt)
    def p_B5(self):
        while True:
            pkt = (yield self.sB5.get())
            self.obj_scl.in_regB.put(pkt)

    def p_C5(self):
        while True:
            pkt = (yield self.sC5.get())
            self.obj_scl.in_regC.put(pkt)

    def p_D5(self):
        while True:
            pkt = (yield self.sD5.get())
            self.obj_scl.in_regD.put(pkt)

    ##
    def p_A6(self):
        while True:
            pkt = (yield self.sA6.get())
            self.obj_scl.in_fid_logA.put(pkt)
    def p_B6(self):
        while True:
            pkt = (yield self.sB6.get())
            self.obj_scl.in_fid_logB.put(pkt)

    def p_C6(self):
        while True:
            pkt = (yield self.sC6.get())
            self.obj_scl.in_fid_logC.put(pkt)

    def p_D6(self):
        while True:
            pkt = (yield self.sD6.get())
            self.obj_scl.in_fid_logD.put(pkt)


    ##
    def p_bA(self):
        while True:
            pkt = (yield self.SbA.get())
            self.obj_prtA.in_reg.put(pkt)

    def p_bB(self):
        while True:
            pkt = (yield self.SbB.get())
            self.obj_prtB.in_reg.put(pkt)

    def p_bC(self):
        while True:
            pkt = (yield self.SbC.get())
            self.obj_prtC.in_reg.put(pkt)

    def p_bD(self):
        while True:
            pkt = (yield self.SbD.get())
            self.obj_prtD.in_reg.put(pkt)