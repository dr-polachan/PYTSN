""" Code for the port block of the switch. 
"""

import simpy

from pcl import pcl
from rx import rx
from tx import tx

class swfbric(object):
    """ The switch-fabric component. It routes packets from one port to another based
        on entries in the fwd_tbl.

        input/output ports
        ------------------

        in_1: (type: packet)
            packets from port-A are received through this interface
        out_1: (type: packet)
            packets to port-A are transmitted through this interface

        in_2: (type: packet)
            packets from port-B are received through this interface
        out_2: (type: packet)
            packets to port-B are transmitted through this interface

        in_3: (type: packet)
            packets from port-C are received through this interface
        out_3: (type: packet)
            packets to port-C are transmitted through this interface

        in_4: (type: packet)
            packets from port-D are received through this interface
        out_4: (type: packet)
            packets to port-D are transmitted through this interface            

        parameters
        ----------
        
        fwd_tbl: (type: dict)
            tbl that consists of the packet routing information
            output-port of a packet is determined from the dst-id
            e.g.,
            self.fwd_tbl = { # dst-id:output-port
              1: 1,
              2: 2,
              3: 3,
              4: 4
            }

    """
    def __init__(self, env, fwd_tbl = None):
        self.env = env

        # class parameters
        self.fwd_tbl = fwd_tbl

        # store resources
        self.s1 = simpy.Store(env)
        self.s2 = simpy.Store(env)
        self.s3 = simpy.Store(env)
        self.s4 = simpy.Store(env)
        self.s5 = simpy.Store(env)

        # input connection's to store resources
        self.in_1 = self.s1
        self.in_2 = self.s2
        self.in_3 = self.s3
        self.in_4 = self.s4
        
        # output (should always be set to "None")
        self.out_1 = None
        self.out_2 = None
        self.out_3 = None
        self.out_4 = None
        
        # instantiating sub-blocks and its outputs
        
        # running concurrent processes
        self.action = env.process(self.p_1()) 
        self.action = env.process(self.p_2()) 
        self.action = env.process(self.p_3()) 
        self.action = env.process(self.p_4()) 
        self.action = env.process(self.p_5()) 


    # retreiving data from store resources and pushing forward
    def p_1(self):
        while True:
            pkt = (yield self.s1.get())
            self.s5.put(pkt)
    def p_2(self):
        while True:
            pkt = (yield self.s2.get())
            self.s5.put(pkt)
   
    def p_3(self):
        while True:
            pkt = (yield self.s3.get())
            self.s5.put(pkt)

    def p_4(self):
        while True:
            pkt = (yield self.s4.get())
            self.s5.put(pkt)

    def p_5(self):
        while True:
            pkt = (yield self.s5.get())

            out_id = self.fwd_tbl[pkt.dst]

            if(out_id == 1):
                if(self.out_1 != None):
                    self.out_1.put(pkt)
            if(out_id == 2):
                if(self.out_2 != None):
                    self.out_2.put(pkt)
            if(out_id == 3):
                if(self.out_3 != None):
                    self.out_3.put(pkt)
            if(out_id == 4):
                if(self.out_4 != None):
                    self.out_4.put(pkt)


