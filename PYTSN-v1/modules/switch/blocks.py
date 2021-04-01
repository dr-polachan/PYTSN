import simpy


class rx(object):
    def __init__(self, env):
        self.env = env

        self.input = simpy.Store(env)
        self.output = None
        
        #self.input_delay = 0
        self.pkt = None

        self.action = env.process(self.p_1())  # starts the run() method as a SimPy process

    def p_1(self):
        while True:
            pkt = (yield self.input.get())
            #yield self.env.timeout(self.input_delay) # processing delay
            self.output.put(pkt)

class tx(object):
    def __init__(self, env, qlimit=None):
        self.env = env

        # parameters
        self.qlimit = qlimit # on packet

        # store resources
        self.s1 = simpy.Store(env)

        # input connection
        self.input = self.s1
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.p_1())

    def p_1(self):
        while True:
            pkt = (yield self.s1.get())

            if(self.qlimit != None):
                if(len(self.output.items) <= (self.qlimit-1)):
                    self.output.put(pkt)
                # else, drop the packet
            else:
                self.output.put(pkt)

class port(object):
    def __init__(self, env, qlimit = None):
        self.env = env

        # parameters
        self.qlimit = qlimit

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
        self.obj_rx = rx(env); self.obj_rx.output = self.s2
        
        self.obj_tx = tx(env, self.qlimit); self.obj_tx.output = self.s3

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
    def __init__(self, env, fwd_tbl, qlimit=None):
        self.env = env

        # parameters
        self.fwd_tbl = fwd_tbl
        self.qlimit = qlimit

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
        self.obj_prtA = port(env,self.qlimit); self.obj_prtA.out_rx = self.sA3; self.obj_prtA.out_tx = self.sA2
        self.obj_prtB = port(env,self.qlimit); self.obj_prtB.out_rx = self.sB3; self.obj_prtB.out_tx = self.sB2
        self.obj_prtC = port(env,self.qlimit); self.obj_prtC.out_rx = self.sC3; self.obj_prtC.out_tx = self.sC2
        self.obj_prtD = port(env,self.qlimit); self.obj_prtD.out_rx = self.sD3; self.obj_prtD.out_tx = self.sD2
        
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





 
