""" Code for the rx block of the switch. 
"""

import simpy
import pandas as pd
from random import randrange

from modules.traffic import packet

import random
random.seed(0) 


class pcl(object):
    """ Component Port-Control-Logic (PCL). PCL resides in each port of the switch.

        input/output ports
        ------------------

        reg_to_scl: (type: packet)
            registration-requests and response packets are forwarded through this port
        reg_from_rx: (type: packet)
            registration-requests and response packets are received through this port
        reg_from_scl: (type: packet)
            registration-requests and responses received from SCL for forwarding
        out_nm: (type: packet)
            registration-requests and responses are forwarded to tx-block through this port
        in_gcl: (type: gcl_packet)
            GCL parameters are received from SCL through this port
        out_db: (type: packet)
            data-beacon is forwarded to tx-block through this port
        out_gc: (type: dataframe)
            gate control event to open/close queues in tx-block is transferred this port
        in_fid_log: (type: dataframe)
            dataframe that logs last received packet's flow-id and reception time
        out_fid_log: (type: dataframe)
            dataframe that logs the flow-id and reception time of all packets received in the last CT

        parameters
        ----------

        prt_type: (type: string)
            defines if the port is of type "ST" or "BE". Only ST ports send bcn signals 

        data-structures
        ---------------

        gcl_packet:  
                attributes
                    .ctrl_list (dataframe)
                        coloumns: q4, q3, q2, q1, q_nm, q_be
                        rows: represent a gate control event
                        1: open the queue gate
                        0: close the queue gate                                        
                    .slt_time (float)
                    .gard_band (float)
                    .trml_slot (int)
    """
    def __init__(self, env, prt_type = "BE", prt_id=1, sw_id=None):
        self.env = env

        # parameters
        self.prt_type = prt_type 
        self.prt_id = prt_id
        self.sw_id = sw_id

        # variables
        self.tbl_fid_log = pd.DataFrame()
        self.tbl_fid_log["flow_id"] = []
        self.tbl_fid_log["rcv_time"] = []

        self.gcl_pkt = None

        # store resources
        self.S_reg_req = simpy.Store(env)
        self.S_nm = simpy.Store(env)
        self.S_fid_log = simpy.Store(env)
        self.S_0 = simpy.Store(env)
        self.S_1 = simpy.Store(env)
        self.S_2 = simpy.Store(env)
        self.S_3 = simpy.Store(env)
        self.S_4 = simpy.Store(env)
        self.S_in_gcl = simpy.Store(env)
     
        # map input connections to store resources
        self.reg_from_rx = self.S_reg_req
        self.reg_from_scl = self.S_nm
        self.in_fid_log = self.S_fid_log
        self.in_gcl = self.S_in_gcl
   
        # output (should always be set to "None")
        self.reg_to_scl = None
        self.out_nm = None
        self.out_fid_log = None
        self.out_gc = None
        self.out_db = None
        
        # running concurrent processes
        self.action = env.process(self.r_reg_pkt())
        self.action = env.process(self.r_nm())
        self.action = env.process(self.r_fid())
        self.action = env.process(self.r_fid_txr())
        self.action = env.process(self.r_gcl())
        self.action = env.process(self.r_gce())
        self.action = env.process(self.r_conf_bcn())
        self.action = env.process(self.r_data_bcn())
        self.action = env.process(self.r_trg_bcn())

    def r_reg_pkt(self):
        while True:
            pkt = (yield self.S_reg_req.get())
            if(self.reg_to_scl != None):
                self.reg_to_scl.put(pkt)

    def r_nm(self):
        while True:
            pkt = (yield self.S_nm.get())
            if(self.out_nm != None):
                self.out_nm.put(pkt)

    def r_fid(self):
        while True:
            tbl = (yield self.S_fid_log.get())
            
            # add tbl info to tbl_fid_log and remove duplicates
            self.tbl_fid_log =  pd.concat([self.tbl_fid_log,tbl])
            self.tbl_fid_log = self.tbl_fid_log.reset_index(drop=True)
            self.tbl_fid_log = self.tbl_fid_log.drop_duplicates(subset=['flow_id'],keep='last')

    def r_fid_txr(self):
        while True:
            yield self.S_0.get()

            # transfer tbl_fid_log to SCL
            if(self.out_fid_log != None):
                self.out_fid_log.put(self.tbl_fid_log)

    def r_gcl(self):
        """ Receives gcl_pkt from SCL and generate triggers

            *gcl_pkt 
                attributes
                    .ctrl_list (dataframe)                                        
                    .slt_time (float)
                    .gard_band (float)
                    .trml_slot (int)
        """
        while True:
            self.gcl_pkt = (yield self.S_in_gcl.get())
            
            self.S_0.put(1) # trigger transfer of tbl_fid_log
            self.S_1.put(1) # trigger gce-generation
            self.S_2.put(1) # trigger beacon-generation

    def r_gce(self):
        """ Extract the gate events one by one from gcl and convert it to a list 
            for transferring it to tx-block
        """
        while True:
            yield self.S_1.get()

            for i in range(self.gcl_pkt.ctrl_list.shape[0]):

                gc = self.gcl_pkt.ctrl_list.copy()
                gc = gc.rename(columns={"q4":4,"q3":3,"q2":2,"q1":1,"q_nm":0,"q_be":-1})
                gc = gc.loc[i].copy()
                gc = pd.DataFrame(gc).transpose()
                gc = gc.loc[:, (gc != 0).any(axis=0)].copy() # remove coloumns with zero entries
                gc = gc.columns.tolist()
                gc = map(int, gc)

                if(self.out_gc != None):
                    self.out_gc.put(gc)
                yield self.env.timeout(self.gcl_pkt.slt_time)

    def r_trg_bcn(self):
        """ If prt_type == "ST" and trml_slot == "None", PCL should send conf-beacon signal. 
            Else, PCL should send data_bcn signal.
        """
        while True:

            yield self.S_2.get()

            if(self.prt_type == "ST"):
                if(self.gcl_pkt.trml_slot == None):
                    self.S_3.put(1) # trigger conf-bcn signal
                else:
                    self.S_4.put(1) # trigger data-bcn signal

    def r_conf_bcn(self):
        """ Generates and send conf-bcn 
        """
        while True:
            # wait for trigger
            yield self.S_3.get()

            # wait for guard band
            yield self.env.timeout(self.gcl_pkt.gard_band)

            # generate packet
            pkt = packet(time=self.env.now, src=0, dst=0, priority=0, flow_id=0,\
                type="conf_bcn",size=100)
            
            # transfer packet
            #self.S_nm.put(pkt)

            # randomization
            
            rand = randrange(100)
            if (rand < 50): 
                print "debug-pcl-sending-conf-bcn",self.prt_id,self.sw_id, self.env.now
                self.S_nm.put(pkt)
            
    def r_data_bcn(self):
        """ Generates and send data-bcn in the gcl_pkt.trml_slot 
        """
        while True:

            yield self.S_4.get()

            yield self.env.timeout(self.gcl_pkt.slt_time*self.gcl_pkt.trml_slot)
            yield self.env.timeout(self.gcl_pkt.gard_band)

            pkt = packet(time=self.env.now,flow_id=0,type="data_bcn",size=100)

            if(self.out_db != None):
                self.out_db.put(pkt)
