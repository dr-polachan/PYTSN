""" Code for the port block of the switch. 
"""

import simpy

from pcl import pcl
from rx import rx
from tx import tx

class port(object):
    """ The port component is made of the following components --- tx, rx and PCL.

        input/output ports
        ------------------

        out_rx: (type: packet)
            data packets received are transferred through this port to the switch-fabric
        out_fid: (type: dataframe)
            dataframe that logs the flow-id and reception time of all packets received in the last CT
        out_reg: (type: packet)
            registration-requests and response packets are forwarded through this port to SCL
        in_reg: (type: packet)
            registration-requests and responses received from SCL for forwarding
        in_gcl: (type: gcl_packet)
            GCL parameters are received from SCL through this port
        in_tx: (type: packet)
            data packet from switch-fabric is received from this port
        in_rx: (type: packet)
            packets are received through this port
        out_tx: (type: packet)
            packets are transmitted out through this port

        parameters
        ----------
        
        rcv_delay: (type: float)
            simulates the processing delay of the switch
        rate: (type: int) in Mbps
            rate at which packets are transmitted out
        txq_limit: (type: int) in Packets
            queue sizes of the queues in the tx block
        prt_type: (type: string)
            defines if the port is of type "ST" or "BE". Only ST ports send bcn signals 
        prt_id: (type: int)
            specifies the port-ID. Port-ID's for Port-A,B,C and D are 1,2,3, and 4

    """

    def __init__(self, env, prt_type="BE", pro_delay=0, txq_limit=None, rate=1000, prt_id=None,\
        sw_id = None):
        
        self.env = env

        # parameters
        self.prt_type = prt_type 
        self.prt_id = prt_id
        self.pro_delay = pro_delay
        self.txq_limit = txq_limit
        self.rate = rate
        self.sw_id = sw_id

        # variables

        # store resources
        self.S_a = simpy.Store(env)
        self.S_b = simpy.Store(env)
        self.S_c = simpy.Store(env)
        self.S_in_gcl = simpy.Store(env)
        self.S_in_rx = simpy.Store(env)
        self.S_out_tx = simpy.Store(env)
        self.S_out_rx = simpy.Store(env)
        self.S_reg = simpy.Store(env)
        self.S_fid = simpy.Store(env)
        self.S_gc = simpy.Store(env)
        self.S_db = simpy.Store(env)
        self.S_nm = simpy.Store(env)
        self.S_in_tx = simpy.Store(env)

        # map input connections to store resources
        self.in_rx = self.S_in_rx
        self.in_reg = self.S_c
        self.in_gcl = self.S_in_gcl
        self.in_tx = self.S_in_tx

        # output (should always be set to "None")
        self.out_tx = None
        self.out_rx = None
        self.out_fid = None
        self.out_reg = None

        # instantiating sub-blocks and mapping its outputs to store resources
        self.obj_pcl = pcl(env, prt_type=self.prt_type, prt_id=self.prt_id, sw_id=self.sw_id) 
        self.obj_pcl.out_gc = self.S_gc
        self.obj_pcl.out_db = self.S_db
        self.obj_pcl.out_nm = self.S_nm
        self.obj_pcl.out_fid_log = self.S_a
        self.obj_pcl.reg_to_scl = self.S_b

        self.obj_rx = rx(env, pro_delay=self.pro_delay, prt_id=self.prt_id)
        self.obj_rx.output = self.S_out_rx
        self.obj_rx.reg_to_pcl = self.S_reg
        self.obj_rx.out_fid_log = self.S_fid

        self.obj_tx = tx(env, qlimit=self.txq_limit, rate=self.rate)
        self.obj_tx.output = self.S_out_tx

        # running simpy concurrent processes
        self.action = env.process(self.r_a())
        self.action = env.process(self.r_b())
        self.action = env.process(self.r_c())
        self.action = env.process(self.r_gcl())
        self.action = env.process(self.r_out_rx())
        self.action = env.process(self.r_reg())
        self.action = env.process(self.r_fid())
        self.action = env.process(self.r_gc())
        self.action = env.process(self.r_db())
        self.action = env.process(self.r_nm())
        self.action = env.process(self.r_in_tx())
        self.action = env.process(self.r_in_rx())
        self.action = env.process(self.r_out_tx())

        
    def r_a(self): 
        """ transfers fid_tbl to SCL
        """
        while True:
            msg = (yield self.S_a.get())
            if(self.out_fid != None):
                self.out_fid.put(msg)

    def r_b(self): 
        """ transfers registration-request/response packets to SCL
        """
        while True:
            msg = (yield self.S_b.get())
            if(self.out_reg != None):
                self.out_reg.put(msg)

    def r_c(self): 
        """ receives registration-request/response from SCL
        """
        while True:
            msg = (yield self.S_c.get())
            if(self.obj_pcl.reg_from_scl != None):
                self.obj_pcl.reg_from_scl.put(msg)

    def r_gcl(self): 
        """ transfer gcl received from SCL to PCL
        """
        while True:
            msg = (yield self.S_in_gcl.get())
            if(self.obj_pcl.in_gcl != None):
                self.obj_pcl.in_gcl.put(msg)

    def r_in_rx(self): 
        """ transfers received packet to rx-block
        """
        while True:
            msg = (yield self.S_in_rx.get())
            if(self.obj_rx.input != None):
                self.obj_rx.input.put(msg)

    def r_out_tx(self): 
        """ transmit packets out
        """
        while True:
            msg = (yield self.S_out_tx.get())
            if(self.out_tx != None):
                self.out_tx.put(msg)

    def r_out_rx(self): 
        """ transfers data packets to switch fabric
        """
        while True:
            msg = (yield self.S_out_rx.get())
            if(self.out_rx != None):
                self.out_rx.put(msg)

    def r_reg(self): 
        """ transfers registration-request/response packets to PCL
        """
        while True:
            msg = (yield self.S_reg.get())
            if(self.obj_pcl.reg_from_rx != None):
                self.obj_pcl.reg_from_rx.put(msg)

    def r_fid(self): 
        """ transfers fid_tbl to PCL
        """
        while True:
            msg = (yield self.S_fid.get())
            if(self.obj_pcl.in_fid_log != None):
                self.obj_pcl.in_fid_log.put(msg)

    def r_gc(self): 
        """ transfers gate control events from PCL to tx
        """
        while True:
            msg = (yield self.S_gc.get())
            if(self.obj_tx.in_gc != None):
                self.obj_tx.in_gc.put(msg)

    def r_db(self): 
        """ transfers data beacon to tx
        """
        while True:
            msg = (yield self.S_db.get())
            if(self.obj_tx.input != None):
                self.obj_tx.input.put(msg)

    def r_nm(self): 
        """ transfers registration-request/response/conf-bcn to tx
        """
        while True:
            msg = (yield self.S_nm.get())
            if(self.obj_tx.input != None):
                self.obj_tx.input.put(msg)

    def r_in_tx(self): 
        """ transfers data packets to tx
        """
        while True:
            msg = (yield self.S_in_tx.get())
            if(self.obj_tx.input != None):
                self.obj_tx.input.put(msg)

