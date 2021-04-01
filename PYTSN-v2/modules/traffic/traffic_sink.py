import simpy

class traffic_sink(object):
    """ A module to log received data packets
    """
    def __init__(self,env,id=1,debug=False):

        # simpy environment
        self.env = env

        # parameters
        self.id = id
        self.debug = debug
        
        # store resources
        self.input = simpy.Store(env)

        # running concurrent processes
        self.action = env.process(self.run())  

        # logging to file
        if(self.debug):
            with open("./results/traffic/ts"+str(self.id)+".txt", "w") as file:
                        file.write("flow-id,msg-id,snd-time,size(B),src-id,dst-id,rcv-time\n")

    def run(self):

        while True:
            pkt = (yield self.input.get())
            now = self.env.now         
            if self.debug:
                print(pkt), ",", "rcv-time:", now, "delay:", (round(now-pkt.time,8)),\
                    "data:", pkt.data
                
                data = str(pkt.flow_id)+","+str(pkt.id)+","+str(pkt.time)+","+str(pkt.size)+","+\
                str(pkt.src)+","+str(pkt.dst)+","+str(now)+"\n"

                with open("./results/traffic/ts"+str(self.id)+".txt", "a") as file:
                    file.write(data)