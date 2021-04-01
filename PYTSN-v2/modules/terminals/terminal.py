import simpy

from modules.traffic import traffic_generator
from modules.traffic import traffic_sink

                
class terminal(object):
    """ A generic network terminal which can send and receive packets
    """
    def __init__(self, env, id=1, dest_id=2, flow_id=1, priority=0,\
     adist=None, sdist=None, start_time=0, stop_time=float('inf'), rate=10000,\
     debug=False,type="None",data="None"):

        # simpy environment
        self.env = env

        # parameters
        self.rate = rate

        # store resources
        self.S_in = simpy.Store(env)
        self.S_out = simpy.Store(env)

        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.tg = traffic_generator(env, id=id, dest_id=dest_id, flow_id=flow_id, priority=priority,\
            adist=adist, sdist=sdist, start_time=start_time, stop_time=stop_time, type=type, data=data)
        self.tg.output = self.S_out
        
        self.ts = traffic_sink(env, id=id, debug=debug)

        # running concurrent processes
        self.action = env.process(self.r_out())
        self.action = env.process(self.r_in())


    def r_out(self): 
        """ Transmit the packet received from the traffic generator module
        """
        while True:
            pkt = (yield self.S_out.get())
            if(self.output != None):
                yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                self.output.put(pkt)

    def r_in(self): 
        """ Transfer the packet received to the traffic sink module
        """
        while True:
            pkt = (yield self.S_in.get())
            self.ts.input.put(pkt)