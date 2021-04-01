import simpy

class debug_sink(object):
    """ A module to log received data packets
    """
    def __init__(self,env):

        # simpy environment
        self.env = env
        
        # store resources
        self.input = simpy.Store(env)

        # running concurrent processes
        self.action = env.process(self.run())  


    def run(self):

        while True:
            pkt = (yield self.input.get())
            
            now = self.env.now         
            
            print "rcv-time:",now,", obj-received:",pkt
            print pkt.data