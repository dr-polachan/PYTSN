""" Code for the tx block of the switch. Tx block uses two subcomponents, dmux and queue-gate.
"""

import simpy

class dmux(object):
    """ Routes the received packet to different tx queues. 
        (1) if the packet has flow-id of -1, it is routed to queue-be
        (2) if the packet has flow-id of 0, it is routed to queue-nm
        (3) packets with flow-id other than -1 and 0 are routed based on prt_in. 
        prt_in indicate from which port the packet is received by the switch.
        if prt_in corresponds to Port-A, packet is routed to queue-1, if it 
        corresponds to Port-B, C, and D, packet is routed to queue-2,3 and 4 respectively.
    """
    def __init__(self, env, qlimit=None):

        # parameters
        self.env = env

        # store resources
        self.S_in = simpy.Store(env)
       
        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.out_st_5 = None
        self.out_st_4 = None
        self.out_st_3 = None
        self.out_st_2 = None
        self.out_st_1 = None
        self.out_st_0 = None
        self.out_be = None

        # running concurrent processes
        self.action = env.process(self.r_dmux())

    def r_dmux(self):
        """ Simpy process that routes the packets based on its prt_in and flow_id
        """
        while True:
            pkt = (yield self.S_in.get())

            if(pkt.flow_id == 0): # network-management traffic
                if(self.out_st_0 != None):
                    self.out_st_0.put(pkt)
            
            elif(pkt.flow_id == -1): # best-effort traffic
                if(self.out_be != None):
                    self.out_be.put(pkt)
            
            elif(pkt.prt_in == 1): # if packet entered through Port-A
                if(self.out_st_1 != None):
                    self.out_st_1.put(pkt)

            elif(pkt.prt_in == 2): # if packet entered through Port-B
                if(self.out_st_2 != None):
                    self.out_st_2.put(pkt)

            elif(pkt.prt_in == 3): # if packet entered through Port-C
                if(self.out_st_3 != None):
                    self.out_st_3.put(pkt)

            elif(pkt.prt_in == 4): # if packet entered through Port-D
                if(self.out_st_4 != None):
                    self.out_st_4.put(pkt)

class queue_gate(object):
    """ Simulates the gated tx queue
    """
    def __init__(self, env, gid=None, qlimit = None):
        self.env = env

        # parameters
        self.gid = gid # component-id
        self.qlimit = qlimit # queue limit in packets

        # variables
        self.priority = None
        self.var_gce = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_q = simpy.Store(env)
        self.S_gce = simpy.Store(env)
        self.S_tcs = simpy.Store(env)
        self.S_gcs = simpy.Store(env)

        # input connection
        self.input = self.S_in
        self.gce = self.S_gce
        self.tcs = self.S_tcs
        
        # output (should always be set to "None")
        self.output = None
        self.pas = None

        # running concurrent processes
        self.action = env.process(self.r_q())
        self.action = env.process(self.r_tr())
        self.action = env.process(self.r_gce())

    def r_gce(self):
        while True:
            self.var_gce = (yield self.S_gce.get())
            if(len(self.S_gcs.items)==0):
                self.S_gcs.put(1)

    def r_q(self): 
        while True:
            pkt = (yield self.S_in.get())
            if(self.qlimit == None):
                self.S_q.put(pkt)
            elif(len(self.S_q.items) <= self.qlimit-1):
                self.S_q.put(pkt)

    def r_tr(self): 
        while True:
            pkt = (yield self.S_q.get())
            flag_txr = 0
            #print "debug-1", pkt, self.env.now
            while(flag_txr == 0):
                #print "debug-A", self.var_gce
                if(self.gid in self.var_gce):
                    if(len(self.output.items) == 0):
                        self.output.put(pkt)
                        self.priority = pkt.priority
                        if(len(self.pas.items) == 0):
                            self.pas.put(1)
                        flag_txr = 1
                        #print "debug-2", pkt, self.env.now

                    else:
                        if(len(self.S_tcs.items) != 0):
                            yield self.S_tcs.get()
                        yield self.S_tcs.get()
                else:
                    #print "debug-3", pkt, self.env.now
                    if(len(self.S_gcs.items) != 0):
                        yield self.S_gcs.get()
                    yield self.S_gcs.get()
      


class tx(object):
    """ Simulates the tx block. Uses two subcomponents dmux and queue_gate
    """
    def __init__(self, env, qlimit=1000, rate=1000):
        self.env = env

        # parameters
        self.qlimit = qlimit 
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
        self.in_db = self.S_in
        self.in_nm = self.S_in
        self.in_gc = self.S_gce
        
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

        #self.gcl_generator = gcl_generator(env, gcl_ts_list=self.gc_ts_list,\
        # gcl_list=self.gc_id_list)
        #self.gcl_generator.output = self.S_gce

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

            #debug-trigger-gce-rcv-event
            if(len(self.S_pas.items)==0):
                self.S_pas.put(1)
            
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


