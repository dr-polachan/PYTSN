""" Code for the rx block of the switch. 
"""

import simpy
import pandas as pd

class rx(object):
    """ (i) The block routes the received packet based on its flow_id.
        (ii) The block also generates a table fid_log_tbl containing the packets flow-id 
        and its received time. The table is then send to the PCL
        (iii) the block also appends the input port information in the packet (prt_in field)
    """
    def __init__(self, env, pro_delay=0, prt_id=None):
        self.env = env

        # parameters        
        self.pro_delay = pro_delay
        self.prt_id = prt_id

        # inputs
        self.input = simpy.Store(env)

        # outputs
        self.output = None
        self.reg_to_pcl = None
        self.out_fid_log = None

        # running concurrent processes
        self.action = env.process(self.run())  

    def run(self):
        while True:
            # wait to receive packet
            pkt = (yield self.input.get())

            # add port-id to packet's prt_in field
            pkt.prt_in = self.prt_id

            # simulate processing delay
            yield self.env.timeout(self.pro_delay) # processing delay of the switch
        
            # route packet based on flow_id
            if(pkt.flow_id == 0):
                if(self.reg_to_pcl != None):
                    self.reg_to_pcl.put(pkt)
            else:
                if(self.output != None):
                    self.output.put(pkt)

            # creating and transferring fid_log_tbl
            fid_log_tbl =  pd.DataFrame()
            fid_log_tbl["flow_id"] = [pkt.flow_id]
            fid_log_tbl["rcv_time"] = [self.env.now]

            if(self.out_fid_log != None):
                self.out_fid_log.put(fid_log_tbl)



