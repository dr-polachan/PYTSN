import simpy

class Packet(object):
    """ A very simple class that represents a packet.
        This packet will run through a queue at a switch output port.
        We use a float to represent the size of the packet in bytes so that
        we can compare to ideal M/M/1 queues.

        Parameters
        ----------
        time : float
            the time the packet arrives at the output queue.
        size : float
            the size of the packet in bytes
        id : int
            an identifier for the packet
        src, dst : int
            identifiers for source and destination
        flow_id : int
            small integer that can be used to identify a flow
    """
    def __init__(self, time=None, size=None, id=None, src=None, dst=None, flow_id=-1,\
    priority=None, lan_id=None, type=None, conf=None):
        #self.time = time # seconds
        #self.size = size # bytes
        #self.id = id 
        #self.src = src
        #self.dst = dst
        #self.flow_id = flow_id

        self.time = time # seconds
        self.id = id # message-id
        self.flow_id = flow_id
        self.priority = priority
        self.lan_id = lan_id
        self.src = src
        self.dst = dst
        self.size = size # bytes
        self.type = type
        self.conf = conf



    def __repr__(self):
        return "flow: {}, msg: {}, prio: {}, snd-time: {},  size(B): {}, src: {}, dst: {}, type: {}".\
            format(self.flow_id, self.id, self.priority, self.time, self.size, self.src, self.dst, self.type)


class traffic_generator(object):
    
    def __init__(self, env, id=1, lan_id=1, dest_id=2, flow_id=1, priority=0, \
        adist=None, sdist=None, initial_delay=0, type=None, conf=None, rate=1000):

        self.env = env
        
        self.id = id
        self.lan_id = lan_id
        self.dest_id = dest_id
        self.flow_id = flow_id
        self.priority = priority
        self.type = type
        self.conf = conf
        self.rate = rate

        self.adist = adist
        self.sdist = sdist

        self.initial_delay = initial_delay
        self.finish = float("inf")
        
        self.packets_sent = 0

        self.S_1 = simpy.Store(env)
        
        self.action = env.process(self.run())  # starts the run() method as a SimPy process
        self.action = env.process(self.r_out())  # starts the run() method as a SimPy process

        self.output = None #holds the input of next block



    def run(self):
        """The generator function used in simulations.
        """
        yield self.env.timeout(self.initial_delay)
        while self.env.now < self.finish:

            self.packets_sent += 1
            
            pkt = Packet(time=self.env.now, size=self.sdist(), id=self.packets_sent, src=self.id,\
            flow_id=self.flow_id, dst=self.dest_id, lan_id=self.lan_id, priority=self.priority,\
            type=self.type, conf=self.conf)


            self.S_1.put(pkt)

            # wait for next transmission
            yield self.env.timeout(self.adist())

    def r_out(self):

        while(True):

            pkt = (yield self.S_1.get())

            if(self.output != None):
                yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                self.output.put(pkt)


class sink(object):

    def __init__(self, env, id=1, lan_id=1, debug=False):

        self.input = simpy.Store(env)
        self.env = env

        self.action = env.process(self.run())  

    def run(self):

        while True:

            msg = (yield self.input.get())
            print self.env.now, msg


class traffic_sink(object):
    
    def __init__(self, env, id=1, lan_id=1, debug=False):

        self.input = simpy.Store(env)
        self.env = env

        self.id = id
        self.lan_id = lan_id
        self.debug = debug

        # logging to file
        if(self.debug):
            with open("./results/traffic/ts"+str(self.id)+".txt", "w") as file:
                        file.write("flow-id,msg-id,snd-time,size(B),src-id,dst-id,rcv-time\n")

        self.action = env.process(self.run())  

    def run(self):

        while True:

            pkt = (yield self.input.get())

            now = self.env.now
            
            if self.debug:
                print(pkt), ",", "rcv-time:", now, "delay:", (round(now-pkt.time,8))
                
                data = str(pkt.flow_id)+","+str(pkt.id)+","+str(pkt.time)+","+str(pkt.size)+","+\
                str(pkt.src)+","+str(pkt.dst)+","+str(now)+"\n"

                with open("./results/traffic/ts"+str(self.id)+".txt", "a") as file:
                    file.write(data)


                

