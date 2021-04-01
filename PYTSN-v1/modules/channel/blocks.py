import simpy
import random

class link(object):
    def __init__(self, env, latency=0, jitter = 0, loss=0, qlimit=None):
        self.env = env

        # parameter
        self.latency = latency # seconds
        self.jitter = jitter
        self.loss = loss # %
        #self.rate = rate # Mbps 
        self.qlimit = qlimit # queue limit in packets

        # store resources
        self.S_in = simpy.Store(env)
        self.S_1 = simpy.Store(env)
        self.S_2 = simpy.Store(env)


        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_1())
        self.action = env.process(self.r_2())
        self.action = env.process(self.r_3())


    def delay(self, pkt):

        yield self.env.timeout(self.latency*(1 + random.random()*self.jitter/100.0)) # propogation delay,jitter
        self.S_2.put(pkt)

    def r_1(self):
        while True:
            pkt = (yield self.S_in.get())
            
            # implementing q_limit
            if(self.qlimit == None):
                self.S_1.put(pkt)
            elif(len(self.S_1.items) <= self.qlimit-1):
                self.S_1.put(pkt)

    def r_2(self):
        while True:
            pkt = (yield self.S_1.get()) 
            #yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
            self.action = self.env.process(self.delay(pkt)) # latency and jitter

    def r_3(self):
        while True:
            pkt = (yield self.S_2.get())   

            # simulate packet loss        
            if (random.random() > self.loss/100.0):
                if(self.output):
                    self.output.put(pkt)




