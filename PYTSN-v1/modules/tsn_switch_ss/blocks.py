import simpy

from sub_blocks import dmux as dmux
from sub_blocks import priority_router as priority_router
from sub_blocks import gcl_generator as gcl_generator
from sub_blocks import queue_gate as queue_gate

class tx(object):
    def __init__(self, env, qlimit=1000, gcl_ts_list=[[10e-6],[40e-6]],\
     gcl_list=[[1],[-1]], rate=1000):
        self.env = env

        # parameters
        self.qlimit = qlimit 
        self.gc_ts_list = gcl_ts_list 
        self.gc_id_list = gcl_list
        self.rate = rate

        # variables
        self.var_gce = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_out = simpy.Store(env)

        self.S_gce = simpy.Store(env)

        self.S_st5q_in = simpy.Store(env)
        self.S_st5q_out =simpy.Store(env)

        self.S_st4q_in = simpy.Store(env)
        self.S_st4q_out =simpy.Store(env)

        self.S_st3q_in = simpy.Store(env)
        self.S_st3q_out =simpy.Store(env)

        self.S_st2q_in = simpy.Store(env)
        self.S_st2q_out =simpy.Store(env)

        self.S_st1q_in = simpy.Store(env)
        self.S_st1q_out = simpy.Store(env)

        self.S_st0q_in = simpy.Store(env)
        self.S_st0q_out = simpy.Store(env)

        self.S_beq_in = simpy.Store(env)
        self.S_beq_out = simpy.Store(env)

        self.S_pas = simpy.Store(env) 

        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_in())
        
        self.action = env.process(self.r_out())

        self.action = env.process(self.r_gce())

        self.action = env.process(self.r_i5())
        self.action = env.process(self.r_i4())
        self.action = env.process(self.r_i3())
        self.action = env.process(self.r_i2())
        self.action = env.process(self.r_i1())
        self.action = env.process(self.r_i0())
        self.action = env.process(self.r_ibe())

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.dmux = dmux(env);
        self.dmux.out_st_5 = self.S_st5q_in
        self.dmux.out_st_4 = self.S_st4q_in
        self.dmux.out_st_3 = self.S_st3q_in
        self.dmux.out_st_2 = self.S_st2q_in 
        self.dmux.out_st_1 = self.S_st1q_in
        self.dmux.out_st_0 = self.S_st0q_in
        self.dmux.out_be = self.S_beq_in

        self.gcl_generator = gcl_generator(env, gcl_ts_list=self.gc_ts_list,\
         gcl_list=self.gc_id_list)
        self.gcl_generator.output = self.S_gce

        self.qg_st5 = queue_gate(env, gid=5, qlimit=self.qlimit)
        self.qg_st5.output = self.S_st5q_out
        self.qg_st5.pas = self.S_pas

        self.qg_st4 = queue_gate(env, gid=4, qlimit=self.qlimit)
        self.qg_st4.output = self.S_st4q_out
        self.qg_st4.pas = self.S_pas

        self.qg_st3 = queue_gate(env, gid=3, qlimit=self.qlimit)
        self.qg_st3.output = self.S_st3q_out
        self.qg_st3.pas = self.S_pas

        self.qg_st2 = queue_gate(env, gid=2, qlimit=self.qlimit)
        self.qg_st2.output = self.S_st2q_out
        self.qg_st2.pas = self.S_pas

        self.qg_st1 = queue_gate(env, gid=1, qlimit=self.qlimit)
        self.qg_st1.output = self.S_st1q_out
        self.qg_st1.pas = self.S_pas

        self.qg_st0 = queue_gate(env, gid=0, qlimit=self.qlimit)
        self.qg_st0.output = self.S_st0q_out
        self.qg_st0.pas = self.S_pas

        self.qg_be = queue_gate(env, gid=-1, qlimit=self.qlimit)
        self.qg_be.output = self.S_beq_out
        self.qg_be.pas = self.S_pas

    def r_in(self): 
        while True:
            pkt = (yield self.S_in.get())
            self.dmux.input.put(pkt)

    def packets_available(self):
               
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        result = False
        if(self.var_gce != None):
            for i in range(len(gid_list)):
                if gid_list[i] in self.var_gce:
                    if(len(store_list[i].items)>0):
                        result = True  
        
        return(result)

    def gid_of_highest_priority(self):

        queue_list = [self.qg_st5,self.qg_st4,self.qg_st3,self.qg_st2,self.qg_st1,self.qg_st0,self.qg_be]
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        index_list = []
        priority_list = [] 

        for i in range(len(gid_list)):
            if gid_list[i] in self.var_gce:
                if(len(store_list[i].items)>0):
                    index_list.append(i)
                    priority_list.append(queue_list[i].priority)

        # sorting based on priority
        keydict = dict(zip(index_list, priority_list))
        index_list.sort(key=keydict.get, reverse=True)

        return  gid_list[index_list[0]]

    def r_out(self): 

        queue_list = [self.qg_st5,self.qg_st4,self.qg_st3,self.qg_st2,self.qg_st1,self.qg_st0,self.qg_be]
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        while True:
            if(self.packets_available()==True):
                index = gid_list.index(self.gid_of_highest_priority())
                pkt = (yield store_list[index].get())

                if(self.output != None):
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                    self.output.put(pkt)
                    if(len(queue_list[index].tcs.items) == 0):
                        queue_list[index].tcs.put(1)
            else:
                if(len(self.S_pas.items) != 0):
                    yield self.S_pas.get()
                yield self.S_pas.get()

    def r_out_old(self): 
        while True:


            pkt = (yield self.S_st2q_out.get())

            if(self.output != None):
                gid = 2
                if(gid in self.var_gce):
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                    self.output.put(pkt)
                    if(len(self.qg_st2.pas.items) == 0):
                        self.qg_st2.pas.put(1)
                else:
                    if(len(self.S_pas.items) != 0):
                        yield self.S_pas.get()
                    yield self.S_pas.get()

    def r_gce(self): 
        while True:
            gce = (yield self.S_gce.get())
            self.qg_st5.gce.put(gce)
            self.qg_st4.gce.put(gce)
            self.qg_st3.gce.put(gce)
            self.qg_st2.gce.put(gce)
            self.qg_st1.gce.put(gce)
            self.qg_st0.gce.put(gce)
            self.qg_be.gce.put(gce)
            self.var_gce = gce
            
    def r_i5(self): 
        while True:
            pkt = (yield self.S_st5q_in.get())
            self.qg_st5.input.put(pkt)  

    def r_i4(self): 
        while True:
            pkt = (yield self.S_st4q_in.get())
            self.qg_st4.input.put(pkt)  

    def r_i3(self): 
        while True:
            pkt = (yield self.S_st3q_in.get())
            self.qg_st3.input.put(pkt)  

    def r_i2(self): 
        while True:
            pkt = (yield self.S_st2q_in.get())
            self.qg_st2.input.put(pkt)  

    def r_i1(self): 
        while True:
            pkt = (yield self.S_st1q_in.get())
            self.qg_st1.input.put(pkt)  

    def r_i0(self): 
        while True:
            pkt = (yield self.S_st0q_in.get())
            self.qg_st0.input.put(pkt)  

    def r_ibe(self): 
        while True:
            pkt = (yield self.S_beq_in.get())
            self.qg_be.input.put(pkt)  


class rx(object):
    def __init__(self, env, pro_delay=2e-6):
        self.env = env

        self.input = simpy.Store(env)
        self.output = None
        
        self.delay_processing = pro_delay

        self.action = env.process(self.p_1())  # starts the run() method as a SimPy process

    def p_1(self):
        while True:
            pkt = (yield self.input.get())
            yield self.env.timeout(self.delay_processing) # processing delay
            self.output.put(pkt)


class port(object):
    def __init__(self, env, qlimit=None, pro_delay=1e-6, gcl_ts_list=[[1e-3]],\
     gcl_list=[[-1,1,2]], rate=10000):
        self.env = env

        # parameters
        self.qlimit = qlimit
        self.gcl_ts_list = gcl_ts_list
        self.gcl_list = gcl_list
        self.pro_delay = pro_delay
        self.rate = rate

        # store resources
        self.s1 = simpy.Store(env)
        self.s2 = simpy.Store(env)
        self.s3 = simpy.Store(env)
        self.s4 = simpy.Store(env)

        # input connection
        self.in_rx = self.s1
        self.in_tx = self.s4
        
        # output (should always be set to "None")
        self.out_rx = None
        self.out_tx = None
        
        # instantiating sub-blocks and its outputs
        self.obj_rx = rx(env, pro_delay=self.pro_delay) 
        self.obj_rx.output = self.s2
        
        self.obj_tx = tx(env, qlimit=self.qlimit, gcl_ts_list=self.gcl_ts_list,\
         gcl_list=self.gcl_list, rate=self.rate)
        self.obj_tx.output = self.s3

        # instantiating a packet object      
        self.pkt = None

        # running concurrent processes
        self.action = env.process(self.p_1()) 
        self.action = env.process(self.p_2()) 
        self.action = env.process(self.p_3()) 
        self.action = env.process(self.p_4()) 


    # retreiving data from store resources and pushing forward
    def p_1(self):
        while True:
            pkt = (yield self.s1.get())
            self.obj_rx.input.put(pkt)
    def p_2(self):
        while True:
            pkt = (yield self.s2.get())
            self.out_rx.put(pkt)
   
    def p_3(self):
        while True:
            pkt = (yield self.s4.get())
            self.obj_tx.input.put(pkt)

    def p_4(self):
        while True:
            pkt = (yield self.s3.get())
            self.out_tx.put(pkt)

class mux_dmux(object):
    def __init__(self, env):
        self.env = env

        # class parameters
        self.fwd_tbl = { # dst-id:output-port
          1: 1,
          2: 2,
          3: 3,
          4: 4
        }

        # store resources
        self.s1 = simpy.Store(env)
        self.s2 = simpy.Store(env)
        self.s3 = simpy.Store(env)
        self.s4 = simpy.Store(env)
        self.s5 = simpy.Store(env)

        # input connection's to store resources
        self.in_1 = self.s1
        self.in_2 = self.s2
        self.in_3 = self.s3
        self.in_4 = self.s4
        
        # output (should always be set to "None")
        self.out_1 = None
        self.out_2 = None
        self.out_3 = None
        self.out_4 = None
        
        # instantiating sub-blocks and its outputs
        
        # instantiating a packet object      
        self.pkt = None

        # running concurrent processes
        self.action = env.process(self.p_1()) 
        self.action = env.process(self.p_2()) 
        self.action = env.process(self.p_3()) 
        self.action = env.process(self.p_4()) 
        self.action = env.process(self.p_5()) 


    # retreiving data from store resources and pushing forward
    def p_1(self):
        while True:
            pkt = (yield self.s1.get())
            self.s5.put(pkt)
    def p_2(self):
        while True:
            pkt = (yield self.s2.get())
            self.s5.put(pkt)
   
    def p_3(self):
        while True:
            pkt = (yield self.s3.get())
            self.s5.put(pkt)

    def p_4(self):
        while True:
            pkt = (yield self.s4.get())
            self.s5.put(pkt)


    def p_5(self):
        while True:
            pkt = (yield self.s5.get())



            out_id = self.fwd_tbl[pkt.dst]

            if(out_id == 1):
                self.out_1.put(pkt)
            if(out_id == 2):
                self.out_2.put(pkt)
            if(out_id == 3):
                self.out_3.put(pkt)
            if(out_id == 4):
                self.out_4.put(pkt)


class switch(object):
    def __init__(self, env, fwd_tbl, qlimit=None, pro_delay=1e-6,\
     gcl_ts_list=[[1e-3]], gcl_list=[[-1,1,2]], rate=10000):
        self.env = env

        # parameters
        self.fwd_tbl = fwd_tbl
        self.qlimit = qlimit
        self.gcl_ts_list = gcl_ts_list
        self.gcl_list = gcl_list
        self.pro_delay = pro_delay
        self.rate = rate

        # store resources
        self.sA1 = simpy.Store(env)
        self.sA2 = simpy.Store(env)
        self.sA3 = simpy.Store(env)
        self.sA4 = simpy.Store(env)
        self.sA5 = simpy.Store(env)

        self.sB1 = simpy.Store(env)
        self.sB2 = simpy.Store(env)
        self.sB3 = simpy.Store(env)
        self.sB4 = simpy.Store(env)
        self.sB5 = simpy.Store(env)

        self.sC1 = simpy.Store(env)
        self.sC2 = simpy.Store(env)
        self.sC3 = simpy.Store(env)
        self.sC4 = simpy.Store(env)
        self.sC5 = simpy.Store(env)

        self.sD1 = simpy.Store(env)
        self.sD2 = simpy.Store(env)
        self.sD3 = simpy.Store(env)
        self.sD4 = simpy.Store(env)
        self.sD5 = simpy.Store(env)

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
        self.obj_prtA = port(env,qlimit=self.qlimit,gcl_ts_list=self.gcl_ts_list,\
            gcl_list=self.gcl_list,pro_delay=self.pro_delay, rate=self.rate)
        self.obj_prtA.out_rx = self.sA3; self.obj_prtA.out_tx = self.sA2
        
        self.obj_prtB = port(env,qlimit=self.qlimit,gcl_ts_list=self.gcl_ts_list,\
            gcl_list=self.gcl_list,pro_delay=self.pro_delay, rate=self.rate)
        self.obj_prtB.out_rx = self.sB3; self.obj_prtB.out_tx = self.sB2
        
        self.obj_prtC = port(env,qlimit=self.qlimit,gcl_ts_list=self.gcl_ts_list,\
            gcl_list=self.gcl_list,pro_delay=self.pro_delay, rate=self.rate)
        self.obj_prtC.out_rx = self.sC3; self.obj_prtC.out_tx = self.sC2
        
        self.obj_prtD = port(env,qlimit=self.qlimit,gcl_ts_list=self.gcl_ts_list,\
            gcl_list=self.gcl_list,pro_delay=self.pro_delay, rate=self.rate)
        self.obj_prtD.out_rx = self.sD3; self.obj_prtD.out_tx = self.sD2
        
        self.obj_muxdmux = mux_dmux(env); 
        self.obj_muxdmux.fwd_tbl = self.fwd_tbl
        self.obj_muxdmux.out_1 = self.sA4; self.obj_muxdmux.out_2 = self.sB4;
        self.obj_muxdmux.out_3 = self.sC4;self.obj_muxdmux.out_4 = self.sD4;

        # instantiating a packet object      
        self.pkt = None

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

    # updating class parameters
    def update_parameters(self):
        self.obj_muxdmux.fwd_tbl = self.fwd_tbl

    # retreiving data from store resources and pushing forward
    
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
            self.obj_muxdmux.in_1.put(pkt)
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
            self.obj_muxdmux.in_2.put(pkt)
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
            self.obj_muxdmux.in_3.put(pkt)
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
            self.obj_muxdmux.in_4.put(pkt)
    def p_D4(self):
        while True:
            pkt = (yield self.sD4.get())
            self.obj_prtD.in_tx.put(pkt)





 
