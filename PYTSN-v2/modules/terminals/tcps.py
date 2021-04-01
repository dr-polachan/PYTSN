import simpy

from modules.traffic import traffic_sink
from modules.traffic import packet
from modules.algorithms.gcl_design import gate_slot_allocation

class tcps(object):
    """ A tcps terminal
        Generates registration-requesets in response to configuration beacon
        Generates registration-response in response to registration-request received
        Generates packets in response to data beacons
        Receives data packets and registration requests

        Parameters
        ----------
        env : simpy.Environment
            the simulation environment
        id : number
            the TCPS terminal-ID
        lan_id : number
            the lan-ID
        dest_id: number
            the destination terminal to send the packets
        flow_id: number
            the packet flow-ID
        priority: number
            the packet priority
        start_time: number
            Starts packet generation after an initial delay. Default = 0
        stop_time : number
            Stops the packet generation at the stop time. Default is infinite
        pkt_size: number
            Size of data packets to transmit
        burst_count: number
            No of packets to send in response to a data beacon. Default = 10
        rate: number
            the packet transmit rate
        debug: const
            Prints received data packet. Default = False.
    """
    def __init__(self,env,id=1,dest_id=2,priority=0,start_time=0,stop_time=float("inf"),\
        rate=1000,debug=False,pkt_size=100,burst_count=10):
        
        # simpy environment
        self.env = env

        # parameters
        self.id = id
        self.dest_id = dest_id
        self.priority = priority
        self.start_time = start_time
        self.stop_time = stop_time
        self.rate = rate
        self.pkt_size = pkt_size
        self.burst_count = burst_count

        # variables
        self.packet_id = 0

        # store resources
        self.S_in = simpy.Store(env)
        self.S_ts = simpy.Store(env)
        self.S_conf = simpy.Store(env)
        self.S_conf_bcn = simpy.Store(env)
        self.S_reg_req = simpy.Store(env)
        self.S_tg = simpy.Store(env)
        self.S_out = simpy.Store(env)

        # input connection
        self.input = self.S_in
        
        # output (should always be set to "None")
        self.output = None

        # instantiating sub-blocks and connecting its outputs to a store resource       
        self.ts = traffic_sink(env, id=id, debug=debug)

        # running concurrent processes
        self.action = env.process(self.r_in())
        self.action = env.process(self.r_data())
        self.action = env.process(self.r_bcn())
        self.action = env.process(self.r_tg())
        self.action = env.process(self.r_out())
        self.action = env.process(self.r_reg_req())
        self.action = env.process(self.r_reg_rsp())



    def r_in(self):
        """ Receives packets in the interval between the start and stop time 
            Seperates data and non-data packets using the packet's type field. 
        """
        while True:
            pkt = (yield self.S_in.get())
            
            if ((self.env.now < self.start_time) or (self.env.now > self.stop_time)):
            # simulation time is before start_time or after stop_time
                if(pkt.type == "data"):
                    self.S_ts.put(pkt)
                elif(pkt.type == "reg_req"):

                    self.S_conf.put(pkt)

            if ((self.env.now > self.start_time) and (self.env.now < self.stop_time)):
            # simulation time is within start_time and stop_time
                if(pkt.type == "data"):
                    self.S_ts.put(pkt)
                elif(pkt.type != "data"):
                    self.S_conf.put(pkt)


    def r_data(self): 
        """ Transfers the received data-packets to the traffic-sink module
        """
        while True:
            pkt = (yield self.S_ts.get())
            self.ts.input.put(pkt)

    def r_bcn(self): 
        """ Seperates configuration-beacon, data-beacon and registration-response 
            using the packet's type field.
        """
        while True:
            pkt = (yield self.S_conf.get())
            if(pkt.type == "conf_bcn"):
                    self.S_conf_bcn.put(pkt)
            if(pkt.type == "data_bcn"):
                    self.S_tg.put(pkt)
            if(pkt.type == "reg_req"):
                    self.S_reg_req.put(pkt)

    def r_tg(self): 
        """ Generates data packets in response to data-beacon
            Packets are generated with src-id as the flow-id
        """
        while True:
            # receives data-beacon packet
            data_bcn = (yield self.S_tg.get())

            # generates and send data packets
            for i in range(self.burst_count):
                if(self.env.now < self.stop_time):

                    self.packet_id += 1

                    # extract flow-id of data-beacon packet
                    flow_id = data_bcn.flow_id

                    # craft a data packet
                    pkt = packet(time=self.env.now, id=self.packet_id, src=self.id, dst=self.dest_id,\
                     flow_id=self.id, size=self.pkt_size, priority=self.priority, type="data")

                    # transfer's the packet to the "Pkt Transmit" block for trasnmission
                    self.S_out.put(pkt)     

                    # wait for the packet transmit time
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6))  
    
    def r_out(self):
        """ Transmit packet at specified rate.
        """
        while True:
            pkt = yield self.S_out.get()
            if(self.output != None):
                yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                self.output.put(pkt)

    def r_reg_req(self):
        """ Create and send registration request. Registration-request is send 
            in response to configuration-beacon signal. Registration-request has a 
            packet-type of "reg_req", size of 100B, priority of zero, flow_id of zero and 
            data field that contain the required tcps data burst_size in bytes.
        """
        while True:
            # receive packet (configuration-beacon)
            conf_bcn_pkt = yield self.S_conf_bcn.get()

            # create registration-request
            reg_req_pkt = packet(time=self.env.now, id=None, src=self.id, dst=self.dest_id,\
                flow_id=0, size=100, priority=0, type="reg_req")

            #b_req = self.pkt_size*self.burst_count # bandwidth requirement in bytes
            
            reg_req_pkt.data = {"burst_count":self.burst_count, "pkt_size":self.pkt_size,\
                "tcps_rate": self.rate, "sw_slt_status":[], "sw_rates":[]}

            # transfer's the packet to the "Pkt Transmit" block for trasnmission
            self.S_out.put(reg_req_pkt) 


    def r_reg_rsp(self):
        """ Create and send responses to registration request. Registration-response has a 
            packet-type of "reg_rsp", size of 1000B ?, priority of zero, flow_id of zero and 
            data field that contain the required slot indices the switches in the path has to 
            lock for the given flow and slot for the TCPS terminal to transmit its data

            data format (for two hops): {'slot_to_transmit': 1, 'slots_to_lock': [[1, 2], [1, 2]]}
        """
        while True:
            # receive registration request packet
            reg_req_pkt = yield self.S_reg_req.get()

            # create response packet to registration-request
            reg_rsp_pkt = packet(time=self.env.now, id=None, src=self.id, dst=self.dest_id,\
                flow_id=0, size=100, priority=0, type="reg_rsp")
            
            # generate data for the response packet 
            drop_req, reg_rsp_pkt.data = gate_slot_allocation(reg_req_pkt.data) 

            print "debug-tcps: flow-id", reg_rsp_pkt.dst
            print "debug-tcps: time", self.env.now
            print "debug-tcps: data", reg_rsp_pkt.data

            # transfer's the packet to the "Pkt Transmit" block for trasnmission
            if(drop_req == False):
                self.S_out.put(reg_rsp_pkt)              