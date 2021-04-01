import simpy

class gcl_props_packet(object):
    """ A very simple class that represents a gcl property packet.
    """
    def __init__(self,time_offset=0,control_list=None,time_list=None,map_terminal_to_flow = None):
            
            self.time_offset = time_offset
            self.control_list = control_list
            self.time_list = time_list
            self.map_terminal_to_flow = map_terminal_to_flow

class gcl_packet_generator(object):
    def __init__(self, env):
        self.env = env

        # parameters

        # store resources

        # input connection
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.run())

    def run(self): 

        gcl_pkt = gcl_props_packet()
        gcl_pkt.time_offset = 0.5e-3

        gcl_pkt.control_list = [[0],[1],[2],[-1]]
        gcl_pkt.time_list = [1e-3,1e-3,1e-3,0]
        gcl_pkt.map_terminal_to_flow = {1:1, 2:2}


        yield self.env.timeout(0e-3)


        if(self.output != None):
            self.output.put(gcl_pkt)

        yield self.env.timeout(5e-3)

        if(self.output != None):
            self.output.put(gcl_pkt)

        yield self.env.timeout(5e-3)

        if(self.output != None):
            self.output.put(gcl_pkt)

class gcl_generator(object):
    def __init__(self, env, gcl_Ts = 1e-3, gcl_list = [2,1,-1]):
        self.env = env

        # parameters
        self.gcl_Ts = gcl_Ts 
        self.gcl_list = gcl_list

        # store resources

        # input connection
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_out())

    def r_out(self): 
        while True:
            for i in range(len(self.gcl_list)):
                gcl = self.gcl_list[i]
                if(self.output != None):
                    self.output.put(gcl)
                yield self.env.timeout(self.gcl_Ts)

class queue_gate(object):
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
                    
class queue_gate_old(object):
    def __init__(self, env, gid=None, qlimit = None):
        self.env = env

        # parameters
        self.gid = gid # component-id
        self.qlimit = qlimit # queue limit in packets

        # variables
        self.gate_signal = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_gc = simpy.Store(env)
        self.S_ge = simpy.Store(env)
        self.S_q = simpy.Store(env)

        # input connection
        self.input = self.S_in
        self.in_gc = self.S_gc
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_in())
        self.action = env.process(self.r_out())
        self.action = env.process(self.r_gc())

    def r_in(self): 
        while True:
            pkt = (yield self.S_in.get())
            if(self.qlimit == None):
                self.S_q.put(pkt)
            elif(len(self.S_q.items) <= self.qlimit-1):
                self.S_q.put(pkt)

    def r_gc(self): 
        while True:
            gc = (yield self.S_gc.get())

            while(len(self.S_ge.items) != 0): # empty the store resource
                self.S_ge.get()
            
            if self.gid in gc:
                self.gate_signal = 1
                self.S_ge.put(1)
            
            else:
                self.gate_signal = 0
                # store resource is empty

    def r_out(self): 
        while True:
            pkt = (yield self.S_q.get())
            if(self.gate_signal != 1): # if gate is not open
                yield self.S_ge.get() # wait for gate to open
            self.output.put(pkt)

class queue_gate_old(object):
    def __init__(self, env, gid=None, qlimit = 'inf'):
        self.env = env

        # parameters
        self.gid = gid # component-id
        self.qlimit = qlimit # on packet

        # variables
        self.gate_en = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_gc = simpy.Store(env)
        self.S_event_gate_enable = simpy.Store(env, capacity=1)

        # input connection
        self.input = self.S_in
        self.in_gc = self.S_gc
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_in_gcl())
        self.action = env.process(self.r_transfer())

    def r_in_gcl(self): 
        while True:
            gc = (yield self.S_gc.get())
            if self.gid in gc:
                self.gate_en = 1
                self.S_event_gate_enable.put(1)
            else:
                self.gate_en = 0

    def r_transfer(self):
        while True:

            pkt = yield self.S_in.get()
            if(len(self.S_in.items) <= self.qlimit-1):
                if(self.gate_en == 1): # if gate is open
                    self.output.put(pkt)
                    if(len(self.S_event_gate_enable.items) > 0):
                        yield self.S_event_gate_enable.get()
                else:
                    yield self.S_event_gate_enable.get() # wait for gate to be open  
                    self.output.put(pkt) 
            

class priority_router(object):

    def __init__(self, env):
        self.env = env

        # parameters

        # store resources
        self.S_st5q_in = simpy.Store(env)
        self.S_st4q_in = simpy.Store(env)
        self.S_st3q_in = simpy.Store(env)
        self.S_st2q_in = simpy.Store(env)
        self.S_st1q_in = simpy.Store(env)
        self.S_beq_in = simpy.Store(env)
        self.S_nmq_in = simpy.Store(env)


        self.S_out = simpy.Store(env)

       
        # input connection
        self.in_st_5q = self.S_st5q_in
        self.in_st_4q = self.S_st4q_in
        self.in_st_3q = self.S_st3q_in
        self.in_st_2q = self.S_st2q_in
        self.in_st_1q = self.S_st1q_in
        self.in_be_q = self.S_beq_in
        self.in_nm_q = self.S_nmq_in

        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_st_5())
        self.action = env.process(self.r_st_4())
        self.action = env.process(self.r_st_3())
        self.action = env.process(self.r_st_2())
        self.action = env.process(self.r_st_1())

        self.action = env.process(self.r_be())
        self.action = env.process(self.r_nm())
        
        self.action = env.process(self.r_priority_router())

    def r_st_5(self):
        while True:          
            pkt = (yield self.S_st5q_in.get())
            self.S_out.put(pkt)

    def r_st_4(self):
        while True:          
            pkt = (yield self.S_st4q_in.get())
            self.S_out.put(pkt)

    def r_st_3(self):
        while True:          
            pkt = (yield self.S_st3q_in.get())
            self.S_out.put(pkt)

    def r_st_2(self):
        while True:          
            pkt = (yield self.S_st2q_in.get())
            self.S_out.put(pkt)

    def r_st_1(self):
        while True:          
            pkt = (yield self.S_st1q_in.get())
            self.S_out.put(pkt)

    def r_be(self):
        while True:          
            pkt = (yield self.S_beq_in.get())
            self.S_out.put(pkt)

    def r_nm(self):
        while True:          
            pkt = (yield self.S_nmq_in.get())
            self.S_out.put(pkt)

    def pkt_priority_sort(self,arrPkt):

        def funKey(element):
            return element.priority
        
        arrPkt.sort(key=funKey, reverse=True)

        return(arrPkt)

    def r_priority_router(self):
        while True:          
            pkt = (yield self.S_out.get())

            pending_pkts = len(self.S_out.items)
            arrPkt = []
            arrPkt.append(pkt)
            for i in range (pending_pkts):
                pkt = (yield self.S_out.get())
                arrPkt.append(pkt)
            arrPkt = self.pkt_priority_sort(arrPkt)
            for i in range(len(arrPkt)):
                pkt = arrPkt[i] 
                self.output.put(pkt)

class dmux(object):
    def __init__(self, env, qlimit=None):
        self.env = env

        # parameters

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

        while True:
            pkt = (yield self.S_in.get())
            if(pkt.flow_id == 5):
                if(self.out_st_5 != None):
                    self.out_st_5.put(pkt)
            if(pkt.flow_id == 4):
                if(self.out_st_4 != None):
                    self.out_st_4.put(pkt)
            if(pkt.flow_id == 3):
                if(self.out_st_3 != None):
                    self.out_st_3.put(pkt)
            if(pkt.flow_id == 2):
                if(self.out_st_2 != None):
                    self.out_st_2.put(pkt)
            if(pkt.flow_id == 1):
                if(self.out_st_1 != None):
                    self.out_st_1.put(pkt)
            if(pkt.flow_id == 0):
                if(self.out_st_0 != None):
                    self.out_st_0.put(pkt)
            if(pkt.flow_id < 0):
                if(self.out_be != None):
                    self.out_be.put(pkt)
            

class dmux_old(object):
    def __init__(self, env):
        self.env = env

        # parameters

        # store resources
        self.S_in = simpy.Store(env)
       
        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.out_st_6 = None
        self.out_st_5 = None
        self.out_st_4 = None
        self.out_st_3 = None
        self.out_st_2 = None
        self.out_st_1 = None
        self.out_be = None

        # running concurrent processes
        self.action = env.process(self.r_dmux())

    def r_dmux(self):

        while True:
            pkt = (yield self.S_in.get())

            if(pkt.flow_id == 6):
                if(self.out_st_6 != None):
                    self.out_st_6.put(pkt)
            if(pkt.flow_id == 5):
                if(self.out_st_5 != None):
                    self.out_st_5.put(pkt)
            if(pkt.flow_id == 4):
                if(self.out_st_4 != None):
                    self.out_st_4.put(pkt)
            if(pkt.flow_id == 3):
                if(self.out_st_3 != None):
                    self.out_st_3.put(pkt)            
            if(pkt.flow_id == 2):
                if(self.out_st_2 != None):
                    self.out_st_2.put(pkt)
            if(pkt.flow_id == 1):
                if(self.out_st_1 != None):
                    self.out_st_1.put(pkt)
            if(pkt.flow_id == -1):
                if(self.out_be != None):
                    self.out_be.put(pkt)
            

