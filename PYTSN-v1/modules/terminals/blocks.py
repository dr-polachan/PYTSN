import simpy

from ..traffic.blocks import traffic_generator as traffic_generator
from ..traffic.blocks import traffic_sink as traffic_sink
from ..traffic.blocks import Packet as Packet


class tcps(object):
    '''
    Size of 100Bytes are generated for burst_count number of times 
    in response to data-bcn signal until stop_time.
    '''
    def __init__(self,env,id=1,lan_id=1,dest_id=2,flow_id=1,priority=0,\
        initial_delay=0,finish=float("inf"),rate=1000,debug=False,pkt_size=100,\
        burst_count=10,):
        
        self.env = env

        # parameters
        self.id = id
        self.lan_id = lan_id
        self.dest_id = dest_id
        self.finish = finish
        self.priority = priority
        self.size = pkt_size
        self.initial_delay = initial_delay
        self.rate = rate
        self.burst_count = burst_count

        # variables
        self.packets_sent = 0

        # store resources
        self.S_in = simpy.Store(env)
        self.S_data = simpy.Store(env)
        self.S_bcn = simpy.Store(env)
        self.S_rb = simpy.Store(env)
        self.S_db = simpy.Store(env)
        self.S_out = simpy.Store(env)

        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # instantiating sub-blocks and connecting its outputs to a store resource       
        self.ts = traffic_sink(env, id=id, lan_id=lan_id, debug=debug)


        # running concurrent processes
        self.action = env.process(self.r_in())
        self.action = env.process(self.r_data())
        self.action = env.process(self.r_bcn())
        self.action = env.process(self.r_rb())
        self.action = env.process(self.r_db())
        self.action = env.process(self.r_out())

    def r_in(self): 
        while True:

            pkt = (yield self.S_in.get())

            if(self.env.now > self.initial_delay):
                if(pkt.type != None):
                    self.S_bcn.put(pkt)
                else:
                    self.S_data.put(pkt)

    def r_data(self): 
        while True:
            pkt = (yield self.S_data.get())
            self.ts.input.put(pkt)

    def r_bcn(self): 
        while True:
            pkt = (yield self.S_bcn.get())

            if(pkt.type == "data_bcn"):
                self.S_db.put(pkt)
            if(pkt.type == "conf_bcn"):
                self.S_rb.put(pkt)

    def r_rb(self): # send reg-uni
        while True:
            pkt = yield self.S_rb.get()

            reg_pkt = Packet(time=self.env.now, src=self.id, dst=self.dest_id, flow_id=0,\
                lan_id=self.lan_id, type="reg_uni", size=64, conf=None)

            self.S_out.put(reg_pkt)         

    def r_db(self): # send data
        while True:
            rcv_pkt = yield self.S_db.get()

            for i in range(self.burst_count):
                if(self.env.now < self.finish):

                    self.packets_sent += 1
                    flow_id = rcv_pkt.conf["flow_id"]
                    pkt = Packet(time=self.env.now, id=self.packets_sent, src=self.id, dst=self.dest_id, flow_id=flow_id,\
                        lan_id=self.lan_id, size=self.size, priority=self.priority)

                    self.S_out.put(pkt)     

                    # wait for the packet to be transmitted out.
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) 
   

    def r_out(self): 
        while True:
            pkt = yield self.S_out.get()
            
            if(self.output != None):
                yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                self.output.put(pkt)
                

class terminal(object):
    def __init__(self,env,id=1,lan_id=1,dest_id=2,flow_id=1,priority=0,\
        adist=None,sdist=None, initial_delay=0,rate=10000,debug=False):
        self.env = env

        # parameters
        #self.gid = gid # component-id
        #self.qlimit = qlimit # on packet

        # variables
        #self.gate_en = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_out = simpy.Store(env)

        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.tg = traffic_generator(env,id,lan_id=lan_id,dest_id=dest_id,flow_id=flow_id,priority=priority,\
            adist=adist,sdist=sdist,initial_delay=initial_delay,rate=rate)
        self.tg.output = self.S_out
        
        self.ts = traffic_sink(env, id=id, lan_id=lan_id, debug=debug)



        # instantiating a packet object      
        self.pkt = None

        # running concurrent processes
        self.action = env.process(self.r_out())
        self.action = env.process(self.r_in())


    def r_out(self): 
        while True:
            pkt = (yield self.S_out.get())
            if(self.output != None):
                self.output.put(pkt)

    def r_in(self): 
        while True:
            pkt = (yield self.S_in.get())
            if(pkt.type == None):
                self.ts.input.put(pkt)


