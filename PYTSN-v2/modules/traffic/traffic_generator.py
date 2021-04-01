import simpy

from packet import packet

class traffic_generator(object):
    
    def __init__(self, env, id=1, dest_id=2, flow_id=1, priority=0, \
        adist=None, sdist=None, start_time=0, stop_time=float('inf'), type=None, data=None):

        # simpy environment
        self.env = env
        
        # parameters
        self.id = id
        self.dest_id = dest_id
        self.flow_id = flow_id
        self.priority = priority
        self.type = type
        self.adist = adist
        self.sdist = sdist
        self.start_time = start_time
        self.stop_time = stop_time
        self.data = data
        
        # variables
        self.packets_sent = 0

        # store resources
        self.S_1 = simpy.Store(env)
        

        self.action = env.process(self.run())  # starts the run() method as a SimPy process
        self.action = env.process(self.r_out())  # starts the run() method as a SimPy process

        self.output = None #holds the input of next block



    def run(self):
        """The generator function used in simulations.
        """
        yield self.env.timeout(self.start_time)
        while self.env.now < self.stop_time:

            self.packets_sent += 1
            
            pkt = packet(time=self.env.now, size=self.sdist(), id=self.packets_sent, src=self.id,\
            flow_id=self.flow_id, dst=self.dest_id, priority=self.priority, type=self.type)

            pkt.data = self.data

            self.S_1.put(pkt)

            # wait for next transmission
            yield self.env.timeout(self.adist())

    def r_out(self):

        while(True):

            pkt = (yield self.S_1.get())
            if(self.output != None):
                self.output.put(pkt)

