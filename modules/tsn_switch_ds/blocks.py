import simpy
import pandas as pd
from sub_blocks import dmux as dmux
from sub_blocks import priority_router as priority_router
from sub_blocks import gcl_generator as gcl_generator
from sub_blocks import queue_gate as queue_gate
from sub_blocks import gcl_props_packet as gcl_props_packet

from ..traffic.blocks import Packet as Packet

class tx(object):
    def __init__(self, env, qlimit=1000, rate=1000):
        self.env = env

        # parameters
        self.qlimit = qlimit 
        self.rate = rate

        # variables
        self.var_gce = None

        # store resources
        self.S_in = simpy.Store(env)
        self.S_out = simpy.Store(env)

        self.S_gce = simpy.Store(env)

        self.S_st5q_in = simpy.Store(env)
        self.S_st5q_out =simpy.Store(env)

        self.S_st4q_in = simpy.Store(env)
        self.S_st4q_out =simpy.Store(env)

        self.S_st3q_in = simpy.Store(env)
        self.S_st3q_out =simpy.Store(env)

        self.S_st2q_in = simpy.Store(env)
        self.S_st2q_out =simpy.Store(env)

        self.S_st1q_in = simpy.Store(env)
        self.S_st1q_out = simpy.Store(env)

        self.S_st0q_in = simpy.Store(env)
        self.S_st0q_out = simpy.Store(env)

        self.S_beq_in = simpy.Store(env)
        self.S_beq_out = simpy.Store(env)

        self.S_pas = simpy.Store(env) 

        # input connection
        self.input = self.S_in
        self.in_db = self.S_in
        self.in_nm = self.S_in
        self.in_gc = self.S_gce
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_in())
        
        self.action = env.process(self.r_out())

        self.action = env.process(self.r_gce())

        self.action = env.process(self.r_i5())
        self.action = env.process(self.r_i4())
        self.action = env.process(self.r_i3())
        self.action = env.process(self.r_i2())
        self.action = env.process(self.r_i1())
        self.action = env.process(self.r_i0())
        self.action = env.process(self.r_ibe())

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.dmux = dmux(env);
        self.dmux.out_st_5 = self.S_st5q_in
        self.dmux.out_st_4 = self.S_st4q_in
        self.dmux.out_st_3 = self.S_st3q_in
        self.dmux.out_st_2 = self.S_st2q_in 
        self.dmux.out_st_1 = self.S_st1q_in
        self.dmux.out_st_0 = self.S_st0q_in
        self.dmux.out_be = self.S_beq_in

        #self.gcl_generator = gcl_generator(env, gcl_ts_list=self.gc_ts_list,\
        # gcl_list=self.gc_id_list)
        #self.gcl_generator.output = self.S_gce

        self.qg_st5 = queue_gate(env, gid=5, qlimit=self.qlimit)
        self.qg_st5.output = self.S_st5q_out
        self.qg_st5.pas = self.S_pas

        self.qg_st4 = queue_gate(env, gid=4, qlimit=self.qlimit)
        self.qg_st4.output = self.S_st4q_out
        self.qg_st4.pas = self.S_pas

        self.qg_st3 = queue_gate(env, gid=3, qlimit=self.qlimit)
        self.qg_st3.output = self.S_st3q_out
        self.qg_st3.pas = self.S_pas

        self.qg_st2 = queue_gate(env, gid=2, qlimit=self.qlimit)
        self.qg_st2.output = self.S_st2q_out
        self.qg_st2.pas = self.S_pas

        self.qg_st1 = queue_gate(env, gid=1, qlimit=self.qlimit)
        self.qg_st1.output = self.S_st1q_out
        self.qg_st1.pas = self.S_pas

        self.qg_st0 = queue_gate(env, gid=0, qlimit=self.qlimit)
        self.qg_st0.output = self.S_st0q_out
        self.qg_st0.pas = self.S_pas

        self.qg_be = queue_gate(env, gid=-1, qlimit=self.qlimit)
        self.qg_be.output = self.S_beq_out
        self.qg_be.pas = self.S_pas

    def r_in(self): 
        while True:
            pkt = (yield self.S_in.get())
            self.dmux.input.put(pkt)

    def packets_available(self):
               
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        result = False
        if(self.var_gce != None):
            for i in range(len(gid_list)):
                if gid_list[i] in self.var_gce:
                    if(len(store_list[i].items)>0):
                        result = True  
        
        return(result)

    def gid_of_highest_priority(self):

        queue_list = [self.qg_st5,self.qg_st4,self.qg_st3,self.qg_st2,self.qg_st1,self.qg_st0,self.qg_be]
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        index_list = []
        priority_list = [] 

        for i in range(len(gid_list)):
            if gid_list[i] in self.var_gce:
                if(len(store_list[i].items)>0):
                    index_list.append(i)
                    priority_list.append(queue_list[i].priority)

        # sorting based on priority
        keydict = dict(zip(index_list, priority_list))
        index_list.sort(key=keydict.get, reverse=True)

        return  gid_list[index_list[0]]

    def r_out(self): 

        queue_list = [self.qg_st5,self.qg_st4,self.qg_st3,self.qg_st2,self.qg_st1,self.qg_st0,self.qg_be]
        store_list = [self.S_st5q_out,self.S_st4q_out,self.S_st3q_out,self.S_st2q_out,\
        self.S_st1q_out,self.S_st0q_out,self.S_beq_out]
        gid_list = [5, 4, 3, 2, 1, 0, -1]

        while True:
            if(self.packets_available()==True):
                index = gid_list.index(self.gid_of_highest_priority())
                pkt = (yield store_list[index].get())

                if(self.output != None):
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                    self.output.put(pkt)
                    if(len(queue_list[index].tcs.items) == 0):
                        queue_list[index].tcs.put(1)
            else:
                if(len(self.S_pas.items) != 0):
                    yield self.S_pas.get()
                yield self.S_pas.get()

    def r_out_old(self): 
        while True:


            pkt = (yield self.S_st2q_out.get())

            if(self.output != None):
                gid = 2
                if(gid in self.var_gce):
                    yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                    self.output.put(pkt)
                    if(len(self.qg_st2.pas.items) == 0):
                        self.qg_st2.pas.put(1)
                else:
                    if(len(self.S_pas.items) != 0):
                        yield self.S_pas.get()
                    yield self.S_pas.get()

    def r_gce(self): 
        while True:
            gce = (yield self.S_gce.get())
            self.qg_st5.gce.put(gce)
            self.qg_st4.gce.put(gce)
            self.qg_st3.gce.put(gce)
            self.qg_st2.gce.put(gce)
            self.qg_st1.gce.put(gce)
            self.qg_st0.gce.put(gce)
            self.qg_be.gce.put(gce)
            self.var_gce = gce

            #debug-trigger-gce-rcv-event
            if(len(self.S_pas.items)==0):
                self.S_pas.put(1)

            
    def r_i5(self): 
        while True:
            pkt = (yield self.S_st5q_in.get())
            self.qg_st5.input.put(pkt)  

    def r_i4(self): 
        while True:
            pkt = (yield self.S_st4q_in.get())
            self.qg_st4.input.put(pkt)  

    def r_i3(self): 
        while True:
            pkt = (yield self.S_st3q_in.get())
            self.qg_st3.input.put(pkt)  

    def r_i2(self): 
        while True:
            pkt = (yield self.S_st2q_in.get())
            self.qg_st2.input.put(pkt)  

    def r_i1(self): 
        while True:
            pkt = (yield self.S_st1q_in.get())
            self.qg_st1.input.put(pkt)  

    def r_i0(self): 
        while True:
            pkt = (yield self.S_st0q_in.get())
            self.qg_st0.input.put(pkt)  

    def r_ibe(self): 
        while True:
            pkt = (yield self.S_beq_in.get())
            self.qg_be.input.put(pkt)  

class rx(object):
    def __init__(self, env, pro_delay=0):
        self.env = env

        # inputs
        self.input = simpy.Store(env)

        # outputs
        self.output = None
        self.out_reg_req = None

        # parameters        
        self.pro_delay = pro_delay

        self.action = env.process(self.run())  # starts the run() method as a SimPy process

    def run(self):
        while True:
            pkt = (yield self.input.get())
            yield self.env.timeout(self.pro_delay) # processing delay
            if(pkt.flow_id == 0):
                if(self.out_reg_req != None):
                    self.out_reg_req.put(pkt)
            else:
                if(self.output != None):
                    self.output.put(pkt)

class tx_old(object):
    def __init__(self, env, qlimit = None, rate=1000):
        self.env = env

        # parameters
        self.qlimit = qlimit 
        self.rate = rate

        # variables

        # store resources
        self.S_in = simpy.Store(env)
        self.S_out = simpy.Store(env)
        self.S_gc = simpy.Store(env)
        self.S_db = simpy.Store(env)

        self.S_st5q_in = simpy.Store(env)
        self.S_st5q_out =simpy.Store(env)

        self.S_st4q_in = simpy.Store(env)
        self.S_st4q_out =simpy.Store(env)

        self.S_st3q_in = simpy.Store(env)
        self.S_st3q_out =simpy.Store(env)

        self.S_st2q_in = simpy.Store(env)
        self.S_st2q_out =simpy.Store(env)

        self.S_st1q_in = simpy.Store(env)
        self.S_st1q_out =simpy.Store(env)

        self.S_beq_in = simpy.Store(env)
        self.S_beq_out =simpy.Store(env)

        self.S_nmq_in = simpy.Store(env)
        self.S_nmq_out =simpy.Store(env)

        # input connection
        self.input = self.S_in
        self.in_gc = self.S_gc
        self.in_nm = self.S_nmq_in
        self.in_db = self.S_db
        
        # output (should always be set to "None")
        self.output = None

        # running concurrent processes
        self.action = env.process(self.r_in())
        self.action = env.process(self.r_db())
        
        self.action = env.process(self.r_out())

        self.action = env.process(self.r_gc())

        self.action = env.process(self.r_i5())
        self.action = env.process(self.r_o5())

        self.action = env.process(self.r_i4())
        self.action = env.process(self.r_o4())

        self.action = env.process(self.r_i3())
        self.action = env.process(self.r_o3())

        self.action = env.process(self.r_i2())
        self.action = env.process(self.r_o2())

        self.action = env.process(self.r_i1())
        self.action = env.process(self.r_o1())

        self.action = env.process(self.r_ibe())
        self.action = env.process(self.r_obe())

        self.action = env.process(self.r_inm())
        self.action = env.process(self.r_onm())
        
        # instantiating sub-blocks and connecting its outputs to a store resource
        self.dmux = dmux(env);
        self.dmux.out_st_5 = self.S_st5q_in 
        self.dmux.out_st_4 = self.S_st4q_in 
        self.dmux.out_st_3 = self.S_st3q_in 
        self.dmux.out_st_2 = self.S_st2q_in 
        self.dmux.out_st_1 = self.S_st1q_in
        self.dmux.out_be = self.S_beq_in

        self.priority_router = priority_router(env)
        self.priority_router.output = self.S_out


        self.qg_st_5 = queue_gate(env, gid=5, qlimit=self.qlimit)
        self.qg_st_5.output = self.S_st5q_out

        self.qg_st_4 = queue_gate(env, gid=4, qlimit=self.qlimit)
        self.qg_st_4.output = self.S_st4q_out

        self.qg_st_3 = queue_gate(env, gid=3, qlimit=self.qlimit)
        self.qg_st_3.output = self.S_st3q_out

        self.qg_st_2 = queue_gate(env, gid=2, qlimit=self.qlimit)
        self.qg_st_2.output = self.S_st2q_out

        self.qg_st_1 = queue_gate(env, gid=1, qlimit=self.qlimit)
        self.qg_st_1.output = self.S_st1q_out

        self.qg_be = queue_gate(env, gid = -1, qlimit=self.qlimit)
        self.qg_be.output = self.S_beq_out

        self.qg_nm = queue_gate(env, gid=0, qlimit=self.qlimit)
        self.qg_nm.output = self.S_nmq_out

        # instantiating a packet object      
        self.pkt = None

    def r_in(self): 
        while True:
            pkt = (yield self.S_in.get())
            self.dmux.input.put(pkt)

    def r_db(self): 
        while True:
            pkt = (yield self.S_db.get())
            self.dmux.input.put(pkt)

    def r_out(self): 
        while True:
            pkt = (yield self.S_out.get())
            if(self.output != None):
                yield self.env.timeout(pkt.size*8.0/(self.rate*1e6)) # rate limiting
                self.output.put(pkt)     

    def r_gc(self): 
        while True:
            pkt = (yield self.S_gc.get())
            self.qg_st_5.in_gc.put(pkt)
            self.qg_st_4.in_gc.put(pkt)
            self.qg_st_3.in_gc.put(pkt)
            self.qg_st_2.in_gc.put(pkt)
            self.qg_st_1.in_gc.put(pkt)        
            self.qg_be.in_gc.put(pkt)        
            self.qg_nm.in_gc.put(pkt)

    def r_i5(self): 
        while True:
            pkt = (yield self.S_st5q_in.get())
            self.qg_st_5.input.put(pkt)  

    def r_i4(self): 
        while True:
            pkt = (yield self.S_st4q_in.get())
            self.qg_st_4.input.put(pkt)  

    def r_i3(self): 
        while True:
            pkt = (yield self.S_st3q_in.get())
            self.qg_st_3.input.put(pkt)  

    def r_i2(self): 
        while True:
            pkt = (yield self.S_st2q_in.get())
            self.qg_st_2.input.put(pkt)  

    def r_i1(self): 
        while True:
            pkt = (yield self.S_st1q_in.get())
            self.qg_st_1.input.put(pkt)  

    def r_ibe(self): 
        while True:
            pkt = (yield self.S_beq_in.get())
            self.qg_be.input.put(pkt)  

    def r_inm(self): 
        while True:
            pkt = (yield self.S_nmq_in.get())
            self.qg_nm.input.put(pkt)  

    def r_o5(self): 
        while True:
            pkt = (yield self.S_st5q_out.get())
            self.priority_router.in_st_5q.put(pkt)  

    def r_o4(self): 
        while True:
            pkt = (yield self.S_st4q_out.get())
            self.priority_router.in_st_4q.put(pkt)  

    def r_o3(self): 
        while True:
            pkt = (yield self.S_st3q_out.get())
            self.priority_router.in_st_3q.put(pkt)  

    def r_o2(self): 
        while True:
            pkt = (yield self.S_st2q_out.get())
            self.priority_router.in_st_2q.put(pkt)  

    def r_o1(self): 
        while True:
            pkt = (yield self.S_st1q_out.get())
            self.priority_router.in_st_1q.put(pkt)  

    def r_obe(self): 
        while True:
            pkt = (yield self.S_beq_out.get())
            self.priority_router.in_be_q.put(pkt)  

    def r_onm(self): 
        while True:
            pkt = (yield self.S_nmq_out.get())
            self.priority_router.in_nm_q.put(pkt)  


class pcl(object):
    """ The port control logic (PCL).
        PCL is responsible for 
        (i)   generating gate control events from the commands it receive from SCL
        (ii)  transferring registration requests from rx to switch control logic (SCL)
        (iii) transferring broadcast packets from SCL to the network management queue of tx 

        Parameters
        ----------
        prt_type : str
            defines whether the port is used to connect to a 
            best-effort (BE) or scheduled-traffic (ST) terminal
        
    """
    def __init__(self, env, prt_type = "BE"):
        self.env = env

        # parameters
        self.prt_type = prt_type 

        # variables
        self.terminal_id = None
        self.gcl_pkt = None

        # store resources
        self.S_reg_req = simpy.Store(env)
        self.S_uni = simpy.Store(env)
        self.S_brd = simpy.Store(env)
        self.S_brd_out = simpy.Store(env)

        self.S_brd_in = simpy.Store(env)
        self.S_nm = simpy.Store(env)

        self.S_in_gcl = simpy.Store(env)
        self.S_1 = simpy.Store(env)
        self.S_2 = simpy.Store(env)
        self.S_3 = simpy.Store(env)
        self.S_4 = simpy.Store(env)
        self.S_nm = simpy.Store(env)

        # input connection
        self.in_reg_brd = self.S_brd_in
        self.in_gcl_pkt = self.S_in_gcl
        self.in_reg_req = self.S_reg_req
        
        # output (should always be set to "None")
        self.out_reg_brd = None
        self.out_nm = None
        self.out_gc = None
        self.out_db = None

        # running concurrent processes
        self.action = env.process(self.reg_to_brd())
        self.action = env.process(self.terminal_id_extraction())
        self.action = env.process(self.route_reg_req())

        self.action = env.process(self.drop_duplicate_reg_brd())
        self.action = env.process(self.to_nm())

        self.action = env.process(self.gcl_pkt_extraction())
        self.action = env.process(self.terminal_id_match())
        self.action = env.process(self.conf_bcn_signal())
        self.action = env.process(self.data_bcn_signal())
        self.action = env.process(self.gcl_generation())

        # instantiating sub-blocks and configuring its outputs

    def route_reg_req(self):
        while True:
            pkt = (yield self.S_reg_req.get())
            if(pkt.type == "reg_uni"):
                self.S_uni.put(pkt)

            if(pkt.type == "reg_brd"):
                self.S_brd_out.put(pkt)
    def terminal_id_extraction(self):
        while True:
            pkt = (yield self.S_uni.get())
            self.terminal_id = pkt.src
            pkt.type = "reg_brd"
            self.S_brd_out.put(pkt)

    def reg_to_brd(self):
        while True:
            pkt = (yield self.S_brd_out.get())
            
            if(self.out_reg_brd != None):
                self.out_reg_brd.put(pkt)

    def drop_duplicate_reg_brd(self):
        while True:
            pkt = (yield self.S_brd_in.get()) 
            if((pkt.src != self.terminal_id) and (pkt.dst != self.terminal_id)):
                self.S_nm.put(pkt)
    def to_nm(self):
        while True:
            pkt = (yield self.S_nm.get()) 

            if(self.out_nm != None):
                self.out_nm.put(pkt)

    def gcl_pkt_extraction(self):
        while True:
            self.gcl_pkt = (yield self.S_in_gcl.get())
            
            self.S_1.put(1) # trigger gcl-generation
            self.S_2.put(1) # trigger terminal-id match

    def gcl_generation(self):


        while True:
            yield self.S_1.get()
            

            for i in range(len(self.gcl_pkt.control_list)):
                gc = self.gcl_pkt.control_list[i]
                if(self.out_gc != None):
                    self.out_gc.put(gc)
                yield self.env.timeout(self.gcl_pkt.time_list[i])
                


    def terminal_id_match(self):

        while True:

            yield self.S_2.get()

            if (self.prt_type == "ST"):
                if self.terminal_id in self.gcl_pkt.map_terminal_to_flow:
                    self.S_4.put(1) # trigger data-bcn signal
                else:
                    self.S_3.put(1) # trigger conf-bcn signal

    def conf_bcn_signal(self):

        while True:

            yield self.S_3.get()

            yield self.env.timeout(self.gcl_pkt.time_offset)
            pkt = Packet(time=self.env.now,flow_id=0,type="conf_bcn",size=64,conf=None)
            
            self.S_nm.put(pkt)

    def data_bcn_offset(self, gcl_pkt=None, flow_id=None):

        control_list = gcl_pkt.control_list # [[1],[-1],[2]]
        time_list = gcl_pkt.time_list #[1.5, 2, 4]
        map_terminal_to_flow = gcl_pkt.map_terminal_to_flow #{1:1, 2:2}

        index = 0
        result = 0
        for i in control_list:
            if flow_id in i:
                result=index
            index += 1

        offset = 0
        for i in range(result):
            offset += time_list[i]
        offset += gcl_pkt.time_offset # adding 1BE offset

        return offset


    def data_bcn_signal(self):

        while True:

            yield self.S_4.get()

            flow_id = self.gcl_pkt.map_terminal_to_flow[self.terminal_id]

            delay = self.data_bcn_offset(gcl_pkt=self.gcl_pkt,flow_id=flow_id)

            yield self.env.timeout(delay)

            pkt = Packet(time=self.env.now,flow_id=flow_id,type="data_bcn",size=64,conf={"flow_id":flow_id})

            if(self.out_db != None):
                self.out_db.put(pkt)


class port(object):
    """ The port 
        port combines, 
        (i)   Rx
        (ii)  Tx
        (iii) PCL

        Parameters
        ----------
        prt_type : str
            defines whether the port is used to connect to a 
            best-effort (BE) or scheduled-traffic (ST) terminal
        rcv_delay : float
            processing delay in reading packets at rx
        txq_limit : int
            queue limit of tx queue_gate's
        
    """
    def __init__(self,env,prt_type = "BE",pro_delay=0,txq_limit=None,rate=1000):
        
        # parameters
        self.env = env
        self.prt_type = prt_type 
        self.pro_delay = pro_delay
        self.txq_limit = txq_limit
        self.rate = rate


        # variables

        # store resources
        self.S_in_rx = simpy.Store(env)
        self.S_out_rx = simpy.Store(env)
        self.S_req = simpy.Store(env)

        self.S_nm = simpy.Store(env)
        self.S_db = simpy.Store(env)
        self.S_gc = simpy.Store(env)
        self.S_in_tx = simpy.Store(env)
        self.S_out_tx = simpy.Store(env)

        self.S_out_brd = simpy.Store(env)
        self.S_in_brd = simpy.Store(env)
        self.S_in_gcl = simpy.Store(env)

        # input connection
        self.in_reg_brd = self.S_in_brd
        self.in_gcl_pkt = self.S_in_gcl
        self.in_tx = self.S_in_tx
        self.in_rx = self.S_in_rx

        # output (should always be set to "None")
        self.out_tx = None
        self.out_rx = None
        self.out_reg_brd = None

        # instantiating sub-blocks and its outputs
        self.obj_pcl = pcl(env,prt_type=self.prt_type) 
        self.obj_pcl.out_reg_brd = self.S_out_brd
        self.obj_pcl.out_nm = self.S_nm
        self.obj_pcl.out_db = self.S_db
        self.obj_pcl.out_gc = self.S_gc


        self.obj_rx = rx(env,pro_delay=self.pro_delay)
        self.obj_rx.output = self.S_out_rx
        self.obj_rx.out_reg_req = self.S_req

        self.obj_tx = tx(env,qlimit=self.txq_limit,rate=self.rate)
        self.obj_tx.output = self.S_out_tx

        # running concurrent processes
        self.action = env.process(self.r_out_brd())
        self.action = env.process(self.r_in_brd())
        self.action = env.process(self.r_gcl())

        self.action = env.process(self.r_out_rx())
        self.action = env.process(self.r_req())

        self.action = env.process(self.r_nm())
        self.action = env.process(self.r_db())
        self.action = env.process(self.r_gc())
        self.action = env.process(self.r_in_tx())

        self.action = env.process(self.r_in_rx())
        self.action = env.process(self.r_out_tx())

    def r_out_rx(self): 
        while True:
            pkt = (yield self.S_out_rx.get())
            if(self.out_rx != None):
                self.out_rx.put(pkt) 

    def r_out_brd(self): 
        while True:
            pkt = (yield self.S_out_brd.get())
            
            if(self.out_reg_brd != None):
                self.out_reg_brd.put(pkt)  

    def r_in_brd(self): 
        while True:
            pkt = (yield self.S_in_brd.get())
            self.obj_pcl.in_reg_brd.put(pkt)              

    def r_gcl(self): 
        while True:
            pkt = (yield self.S_in_gcl.get())
            self.obj_pcl.in_gcl_pkt.put(pkt)  

    def r_req(self): 
        while True:
            pkt = (yield self.S_req.get())
            self.obj_pcl.in_reg_req.put(pkt)  

    def r_nm(self): 
        while True:
            pkt = (yield self.S_nm.get())
            self.obj_tx.in_nm.put(pkt)

    def r_db(self): 
        while True:
            pkt = (yield self.S_db.get())
            self.obj_tx.in_db.put(pkt)

    def r_gc(self): 
        while True:
            pkt = (yield self.S_gc.get())
            self.obj_tx.in_gc.put(pkt)

    def r_in_tx(self): 
        while True:
            pkt = (yield self.S_in_tx.get())
            self.obj_tx.input.put(pkt)

    def r_in_rx(self): 
        while True:
            pkt = (yield self.S_in_rx.get())
            self.obj_rx.input.put(pkt)

    def r_out_tx(self): 
        while True:
            pkt = (yield self.S_out_tx.get())
            if(self.out_tx != None):
                self.out_tx.put(pkt)

class core(object):
    def __init__(self, env, fwd_tbl = None):
        self.env = env

        # class parameters
        self.fwd_tbl = fwd_tbl
        r'''
        self.fwd_tbl = { # dst-id:output-port
          1: 1,
          2: 2,
          3: 3,
          4: 4
        }
        '''

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
        
        # instantiating a packet object      
        self.pkt = None

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

class scl(object):
    def __init__(self,env,rate=1000,scl_gp=10e-3,scl_gl_netm=100e-6,scl_gl_tcps=1e-3,\
        scl_gbnd=1e-6, scl_ns=5):

        # parameters
        self.env = env
        self.rate = rate
        self.scl_gp = scl_gp # GCL-period
        self.scl_gl_netm = scl_gl_netm #gate-width of network-management queue
        self.scl_gl_tcps = scl_gl_tcps  # GCL-gate width
        self.scl_ns = scl_ns # Number of TCPS pairs supported
        self.scl_gbnd = scl_gbnd

        # variables
        self.reg_tbl = pd.DataFrame(columns = ["t1-id","t2-id","add/del"])

        # store resources
        self.SA1 = simpy.Store(env)
        self.SB1 = simpy.Store(env)
        self.SC1 = simpy.Store(env)
        self.SD1 = simpy.Store(env)
        
        self.SA2 = simpy.Store(env)
        self.SB2 = simpy.Store(env)
        self.SC2 = simpy.Store(env)
        self.SD2 = simpy.Store(env)

        # input connection
        self.in_brdA = self.SA1
        self.in_brdB = self.SB1
        self.in_brdC = self.SC1
        self.in_brdD = self.SD1
        
        # output (should always be set to "None")
        self.out_gclA = None
        self.out_gclB = None
        self.out_gclC = None
        self.out_gclD = None

        self.out_brdA = None
        self.out_brdB = None
        self.out_brdC = None
        self.out_brdD = None


        # running concurrent processes
        self.action = env.process(self.gcl_compute_function())
        self.action = env.process(self.p_ext_fwd_A())
        self.action = env.process(self.p_ext_fwd_B())
        self.action = env.process(self.p_ext_fwd_C())
        self.action = env.process(self.p_ext_fwd_D())

        self.action = env.process(self.p_brdA())
        self.action = env.process(self.p_brdB())
        self.action = env.process(self.p_brdC())
        self.action = env.process(self.p_brdD())

    def p_ext_fwd_A(self):

        while True:

            pkt = yield self.SA1.get()
            if(pkt.src < pkt.dst):
                var_list = [pkt.src, pkt.dst, "add"]
            else:
                var_list = [pkt.dst, pkt.src, "add"]

            self.reg_tbl = self.reg_tbl.append(pd.Series(var_list,\
                index=self.reg_tbl.columns), ignore_index=True)

            self.SB2.put(pkt)
            self.SC2.put(pkt)
            self.SD2.put(pkt)

    def p_ext_fwd_B(self):

        while True:

            pkt = yield self.SB1.get()

            if(pkt.src < pkt.dst):
                var_list = [pkt.src, pkt.dst, "add"]
            else:
                var_list = [pkt.dst, pkt.src, "add"]

            self.reg_tbl = self.reg_tbl.append(pd.Series(var_list,\
                index=self.reg_tbl.columns), ignore_index=True)

            self.SA2.put(pkt)
            self.SC2.put(pkt)
            self.SD2.put(pkt)

    def p_ext_fwd_C(self):

        while True:

            pkt = yield self.SC1.get()
            if(pkt.src < pkt.dst):
                var_list = [pkt.src, pkt.dst, "add"]
            else:
                var_list = [pkt.dst, pkt.src, "add"]

            self.reg_tbl = self.reg_tbl.append(pd.Series(var_list,\
                index=self.reg_tbl.columns), ignore_index=True)

            self.SA2.put(pkt)
            self.SB2.put(pkt)
            self.SD2.put(pkt)

    def p_ext_fwd_D(self):

        while True:

            pkt = yield self.SD1.get()
            if(pkt.src < pkt.dst):
                var_list = [pkt.src, pkt.dst, "add"]
            else:
                var_list = [pkt.dst, pkt.src, "add"]

            self.reg_tbl = self.reg_tbl.append(pd.Series(var_list,\
                index=self.reg_tbl.columns), ignore_index=True)

            self.SA2.put(pkt)
            self.SB2.put(pkt)
            self.SC2.put(pkt)

    def gcl_compute_function(self): 

        gcl_pkt = gcl_props_packet()

        # first-cycle
        #gcl_pkt.time_offset = 1500*8.0/(self.rate*1e6) # guard-band (for 1 BE packet transmit interval)
        gcl_pkt.time_offset = self.scl_gbnd
        gcl_pkt.control_list = [[0],[-1]] #flow-id's
        gcl_pkt.time_list = [self.scl_gl_netm,self.scl_gp-self.scl_gl_netm] 
        gcl_pkt.map_terminal_to_flow = {}

        self.out_gclA.put(gcl_pkt)
        self.out_gclB.put(gcl_pkt)
        self.out_gclC.put(gcl_pkt)
        self.out_gclD.put(gcl_pkt)

        yield self.env.timeout(self.scl_gp)

        while True:

            self.reg_tbl = self.reg_tbl.drop_duplicates().copy()

            df_add = self.reg_tbl[self.reg_tbl["add/del"]=="add"].copy()

            df_add = df_add.sort_values(by=["t1-id"]).copy()

            df_add = df_add.reset_index()

            control_list = [[0]] #flow-id's
            time_list = [self.scl_gl_netm]
            map_terminal_to_flow = {}

            
            for i in range(len(df_add)):
                t1_id = df_add.loc[i]["t1-id"]
                t2_id = df_add.loc[i]["t2-id"]
                control_list.append([i+1])
                time_list.append(self.scl_gl_tcps)
                map_terminal_to_flow[t1_id] = i+1
                map_terminal_to_flow[t2_id] = i+1
            
           
            control_list.append([-1])
            time_list.append(self.scl_gp - (len(df_add))*self.scl_gl_tcps-self.scl_gl_netm)
            
            gcl_pkt.control_list = control_list
            gcl_pkt.time_list = time_list
            gcl_pkt.map_terminal_to_flow = map_terminal_to_flow
           
            self.out_gclA.put(gcl_pkt)
            self.out_gclB.put(gcl_pkt)
            self.out_gclC.put(gcl_pkt)
            self.out_gclD.put(gcl_pkt)
            
            yield self.env.timeout(self.scl_gp)
        
        
    def gcl_compute_function_old(self): 

        gcl_pkt = gcl_props_packet()
        gcl_pkt.time_offset = 0.5e-3

        gcl_pkt.control_list = [[0],[-1],[1]] #flow-id's
        gcl_pkt.time_list = [1e-3,1e-3,1e-3]
        gcl_pkt.map_terminal_to_flow = {3:1, 4:1} #terminal-id to flow-id (only for st-flows)

        yield self.env.timeout(0e-3)

        self.out_gclA.put(gcl_pkt)
        self.out_gclB.put(gcl_pkt)
        self.out_gclC.put(gcl_pkt)
        self.out_gclD.put(gcl_pkt)


        yield self.env.timeout(5e-3)

        self.out_gclA.put(gcl_pkt)
        self.out_gclB.put(gcl_pkt)
        self.out_gclC.put(gcl_pkt)
        self.out_gclD.put(gcl_pkt)


        yield self.env.timeout(5e-3)

        self.out_gclA.put(gcl_pkt)
        self.out_gclB.put(gcl_pkt)
        self.out_gclC.put(gcl_pkt)
        self.out_gclD.put(gcl_pkt)


    def p_brdA(self):

        while(True):
            pkt = (yield self.SA2.get())
            if(self.out_brdA != None):
                self.out_brdA.put(pkt)

    def p_brdB(self):

        while(True):
            pkt = (yield self.SB2.get())
            if(self.out_brdB != None):
                self.out_brdB.put(pkt)

    def p_brdC(self):

        while(True):
            pkt = (yield self.SC2.get())
            if(self.out_brdC != None):
                self.out_brdC.put(pkt)

    def p_brdD(self):

        while(True):
            pkt = (yield self.SD2.get())
            if(self.out_brdD != None):
                self.out_brdD.put(pkt)


class switch(object):
    def __init__(self,env,fwd_tbl,txq_limit=None,pro_delay=0,rate=1000,\
        list_prt_types=["BE","BE","BE","BE"],scl_gp=10e-3,scl_gl_netm=100e-6,scl_gl_tcps=1e-3,\
        scl_gbnd=1e-6,scl_ns=5,sw_id=None):

        self.env = env

        # parameters
        self.fwd_tbl = fwd_tbl
        self.txq_limit = txq_limit
        self.pro_delay = pro_delay
        self.list_prt_types = list_prt_types
        self.scl_gp = scl_gp # GCL-period
        self.scl_gl_netm = scl_gl_netm
        self.scl_gl_tcps = scl_gl_tcps  # GCL-gate width
        self.scl_ns = scl_ns # Number of TCPS pairs supported
        self.rate = rate
        self.scl_gbnd = scl_gbnd
        self.sw_id = sw_id

        # variables
        self.prtA_type = self.list_prt_types[0]
        self.prtB_type = self.list_prt_types[1]
        self.prtC_type = self.list_prt_types[2]
        self.prtD_type = self.list_prt_types[3]

        # store resources
        self.sA1 = simpy.Store(env)
        self.sA2 = simpy.Store(env)
        self.sA3 = simpy.Store(env)
        self.sA4 = simpy.Store(env)
        self.sA5 = simpy.Store(env)

        self.sB1 = simpy.Store(env)
        self.sB2 = simpy.Store(env)
        self.sB3 = simpy.Store(env)
        self.sB4 = simpy.Store(env)
        self.sB5 = simpy.Store(env)

        self.sC1 = simpy.Store(env)
        self.sC2 = simpy.Store(env)
        self.sC3 = simpy.Store(env)
        self.sC4 = simpy.Store(env)
        self.sC5 = simpy.Store(env)

        self.sD1 = simpy.Store(env)
        self.sD2 = simpy.Store(env)
        self.sD3 = simpy.Store(env)
        self.sD4 = simpy.Store(env)
        self.sD5 = simpy.Store(env)

        self.SgA = simpy.Store(env)
        self.SgB = simpy.Store(env)
        self.SgC = simpy.Store(env)
        self.SgD = simpy.Store(env)

        self.SbA = simpy.Store(env)
        self.SbB = simpy.Store(env)
        self.SbC = simpy.Store(env)
        self.SbD = simpy.Store(env)


        # input connection's to store resources
        self.p1_in = self.sA1
        self.p2_in = self.sB1
        self.p3_in = self.sC1
        self.p4_in = self.sD1
        
        # output (should always be set to "None")
        self.p1_out = None
        self.p2_out = None
        self.p3_out = None
        self.p4_out = None

        # instantiating sub-blocks and connecting its outputs to a store resource
        self.obj_prtA = port(env,prt_type=self.prtA_type,txq_limit=self.txq_limit,rate=self.rate,\
            pro_delay=self.pro_delay)
        self.obj_prtA.out_rx = self.sA3; self.obj_prtA.out_tx = self.sA2
        self.obj_prtA.out_reg_brd = self.sA5
        
        self.obj_prtB = port(env,prt_type=self.prtB_type,txq_limit=self.txq_limit,rate=self.rate,\
            pro_delay=self.pro_delay)
        self.obj_prtB.out_rx = self.sB3; self.obj_prtB.out_tx = self.sB2
        self.obj_prtB.out_reg_brd = self.sB5

        self.obj_prtC = port(env,prt_type=self.prtC_type,txq_limit=self.txq_limit,rate=self.rate,\
            pro_delay=self.pro_delay)
        self.obj_prtC.out_rx = self.sC3; self.obj_prtC.out_tx = self.sC2
        self.obj_prtC.out_reg_brd = self.sC5
        
        self.obj_prtD = port(env,prt_type=self.prtD_type,txq_limit=self.txq_limit,rate=self.rate,\
            pro_delay=self.pro_delay)
        self.obj_prtD.out_rx = self.sD3; self.obj_prtD.out_tx = self.sD2
        self.obj_prtD.out_reg_brd = self.sD5

        self.obj_core = core(env, fwd_tbl=self.fwd_tbl); 
        self.obj_core.out_1 = self.sA4; self.obj_core.out_2 = self.sB4;
        self.obj_core.out_3 = self.sC4;self.obj_core.out_4 = self.sD4;

        self.obj_scl = scl(env,scl_gp=self.scl_gp,scl_gl_netm=self.scl_gl_netm,\
            scl_gl_tcps=self.scl_gl_tcps,scl_gbnd=self.scl_gbnd,scl_ns=self.scl_ns)
        self.obj_scl.out_gclA = self.SgA
        self.obj_scl.out_gclB = self.SgB
        self.obj_scl.out_gclC = self.SgC
        self.obj_scl.out_gclD = self.SgD

        self.obj_scl.out_brdA = self.SbA
        self.obj_scl.out_brdB = self.SbB
        self.obj_scl.out_brdC = self.SbC
        self.obj_scl.out_brdD = self.SbD


        # running concurrent processes
        self.action = env.process(self.p_A1()) 
        self.action = env.process(self.p_A2()) 
        self.action = env.process(self.p_A3()) 
        self.action = env.process(self.p_A4()) 

        self.action = env.process(self.p_B1()) 
        self.action = env.process(self.p_B2()) 
        self.action = env.process(self.p_B3()) 
        self.action = env.process(self.p_B4()) 

        self.action = env.process(self.p_C1()) 
        self.action = env.process(self.p_C2()) 
        self.action = env.process(self.p_C3()) 
        self.action = env.process(self.p_C4()) 

        self.action = env.process(self.p_D1()) 
        self.action = env.process(self.p_D2()) 
        self.action = env.process(self.p_D3()) 
        self.action = env.process(self.p_D4()) 

        self.action = env.process(self.p_gA()) 
        self.action = env.process(self.p_gB()) 
        self.action = env.process(self.p_gC()) 
        self.action = env.process(self.p_gD()) 

        self.action = env.process(self.p_A5()) 
        self.action = env.process(self.p_B5()) 
        self.action = env.process(self.p_C5()) 
        self.action = env.process(self.p_D5()) 

        self.action = env.process(self.p_bA()) 
        self.action = env.process(self.p_bB()) 
        self.action = env.process(self.p_bC()) 
        self.action = env.process(self.p_bD()) 


    ## 
    def p_A1(self):
        while True:
            pkt = (yield self.sA1.get())
            self.obj_prtA.in_rx.put(pkt)
    def p_A2(self):
        while True:
            pkt = (yield self.sA2.get())
            if(self.p1_out != None):
                self.p1_out.put(pkt)
    def p_A3(self):
        while True:
            pkt = (yield self.sA3.get())
            self.obj_core.in_1.put(pkt)
    def p_A4(self):
        while True:
            pkt = (yield self.sA4.get())
            self.obj_prtA.in_tx.put(pkt)
    ##        
    def p_B1(self):
        while True:
            pkt = (yield self.sB1.get())
            self.obj_prtB.in_rx.put(pkt)
    def p_B2(self):
        while True:
            pkt = (yield self.sB2.get())
            if(self.p2_out != None):
                self.p2_out.put(pkt)
    def p_B3(self):
        while True:
            pkt = (yield self.sB3.get())
            self.obj_core.in_2.put(pkt)
    def p_B4(self):
        while True:
            pkt = (yield self.sB4.get())
            self.obj_prtB.in_tx.put(pkt)        

    ##        
    def p_C1(self):
        while True:
            pkt = (yield self.sC1.get())
            self.obj_prtC.in_rx.put(pkt)
    def p_C2(self):
        while True:
            pkt = (yield self.sC2.get())
            if(self.p3_out != None):
                self.p3_out.put(pkt)
    def p_C3(self):
        while True:
            pkt = (yield self.sC3.get())
            self.obj_core.in_3.put(pkt)
    def p_C4(self):
        while True:
            pkt = (yield self.sC4.get())
            self.obj_prtC.in_tx.put(pkt)
    
    ##        
    def p_D1(self):
        while True:
            pkt = (yield self.sD1.get())
            self.obj_prtD.in_rx.put(pkt)
    def p_D2(self):
        while True:
            pkt = (yield self.sD2.get())
            if(self.p4_out != None):
                self.p4_out.put(pkt)
    def p_D3(self):
        while True:
            pkt = (yield self.sD3.get())
            self.obj_core.in_4.put(pkt)
    def p_D4(self):
        while True:
            pkt = (yield self.sD4.get())
            self.obj_prtD.in_tx.put(pkt)

    ##   
    def p_gA(self):
        while True:
            pkt = (yield self.SgA.get())
            self.obj_prtA.in_gcl_pkt.put(pkt)
    def p_gB(self):
        while True:
            pkt = (yield self.SgB.get())
            self.obj_prtB.in_gcl_pkt.put(pkt)
    def p_gC(self):
        while True:
            pkt = (yield self.SgC.get())
            self.obj_prtC.in_gcl_pkt.put(pkt)
    def p_gD(self):
        while True:
            pkt = (yield self.SgD.get())
            self.obj_prtD.in_gcl_pkt.put(pkt)

    ##
    def p_A5(self):
        while True:
            pkt = (yield self.sA5.get())
            self.obj_scl.in_brdA.put(pkt)
    def p_B5(self):
        while True:
            pkt = (yield self.sB5.get())
            self.obj_scl.in_brdB.put(pkt)

    def p_C5(self):
        while True:
            pkt = (yield self.sC5.get())
            self.obj_scl.in_brdC.put(pkt)

    def p_D5(self):
        while True:
            pkt = (yield self.sD5.get())
            self.obj_scl.in_brdD.put(pkt)

    ##
    def p_bA(self):
        while True:
            pkt = (yield self.SbA.get())
            self.obj_prtA.in_reg_brd.put(pkt)

    def p_bB(self):
        while True:
            pkt = (yield self.SbB.get())
            self.obj_prtB.in_reg_brd.put(pkt)

    def p_bC(self):
        while True:
            pkt = (yield self.SbC.get())
            self.obj_prtC.in_reg_brd.put(pkt)

    def p_bD(self):
        while True:
            pkt = (yield self.SbD.get())
            self.obj_prtD.in_reg_brd.put(pkt)