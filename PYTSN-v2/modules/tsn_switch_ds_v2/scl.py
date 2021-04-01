""" Code for the rx block of the switch. 
"""

import simpy
import pandas as pd
import numpy as np
import sys

class gcl_packet():
    """ A very simple class that represents a gcl packet.
    """
    def __init__(self, CT=10e-3, prt_type = "BE"):

        self.slt_time =  1e-3
        self.gard_band = 1e-6
        #self.trml_type = "ST"
        self.trml_slot = None
        
        self.n_slt = int(1.0*CT/self.slt_time)

        self.ctrl_list = pd.DataFrame()
        self.ctrl_list["q4"]=(np.zeros(self.n_slt))
        self.ctrl_list["q3"]=(np.zeros(self.n_slt))
        self.ctrl_list["q2"]=(np.zeros(self.n_slt))
        self.ctrl_list["q1"]=(np.zeros(self.n_slt))
        self.ctrl_list["q_nm"]=(np.insert(np.zeros(self.n_slt-1),0,1))
        self.ctrl_list["q_be"]=(np.insert(np.ones(self.n_slt-1),0,0))
        
        '''
        if(prt_type == "BE"):
            self.ctrl_list["q_nm"]=(np.insert(np.zeros(self.n_slt-1),0,1))
            self.ctrl_list["q_be"]=(np.insert(np.ones(self.n_slt-1),0,0))
        elif(prt_type == "ST"):
            self.ctrl_list["q_nm"]=(np.ones(self.n_slt))
            self.ctrl_list["q_be"]=(np.zeros(self.n_slt))
        '''


class scl(object):
    """ The Switch Control Logic (SCL).

        input/output ports
        ------------------

        in_regA, in_regB, in_regC, in_regD: (type: packet)
            the port recieves registration-requests and response packets from the switch ports
            Port-A, Port-B, Port-C, and Port-D, respectively.

        in_regA, in_regB, in_regC, in_regD: (type: packet)
            the port transmits out registration-requests and response packets to the switch ports
            Port-A, Port-B, Port-C, and Port-D, respectively.

        out_gclA, out_gclB, out_gclC, out_gclD (type: gcl_packet)
            the prot transmits gcl's to the switch ports Port-A, B, C and D, respectively
        
        in_fid_logA, in_fid_logB, in_fid_logC, in_fid_logD (type: dataframe)
            flow_id log tables from the switch ports Port-A, B, C and D. flow_id log tables
            log's flow_id's of packets and their last reception time in the ports

        parameters
        ----------

        CT:  (type: int)
            Gate cycle time of IEEE 802.1Qbv

        fwd_tbl: (type: dict)
            A python dictionary that consists of the packet routing information
            output-port of a packet is determined from the dst-id
            e.g.,
            self.fwd_tbl = { # dst-id:output-port
              1: 1,
              2: 2,
              3: 3,
              4: 4
            }

        list_prt_types: (type: list)
            this list indicates the type of port's in the switches
            eg: list_prt_types = ["ST", "BE", "BE", "ST"] indicates that 
                port-A and D is of type ST and port-C and D is of type BE

        list_trml_ids: (type: list)
            this list specifies the src_id of the terminals connected to it
            eg: [1, 2, None, None] indicates that two terminals with ID's 1 and 2
                are connected to Port-A and Port-B. No terminals are connected to 
                Port-C and Port-D
 
        global variables
        ----------------

        GCL: (type: list)
            GCL = [gcl_A, gcl_B, gcl_C, gcl_D]
            list of gcl's for the switch ports Port-A,B,C and D respectively 
            gcl_A, gcl_B, gcl_C, gcl_D are of type gcl_packet

        slt_add: (type: dict)
            "prt": (type: int)
                Specifies the switch port whoose gcl needs to be updated. It is decided from 
                the prt_in field of the registration response packet
            "queue": (type: int)
                Decides gates corresponding to which queue in the gcl needs to be updated. 
                It is equivalent to the switch port to where the registration response is destined. 
                This information is created from the dst_id and fwd_tbl.
            "slt_list": (type: list)
                Specifies which slots of the queue corresponding to the gcl neeeds to be updated.
            "fid": (type: int)
                For logging purposes. "fid" set to "dst-id" of the registration-response

        slt_add_log: (type: dataframe)



        data-structures
        ---------------

        gcl_packet:  
                attributes
                    .ctrl_list (dataframe)
                        coloumns: q4, q3, q2, q1, q_nm, q_be
                        rows: represent a gate control event
                        1: open the queue gate
                        0: close the queue gate
                        e.g.,
                                q4   q3   q2   q1  q_nm  q_be
                            0  0.0  0.0  0.0  0.0   1.0   0.0
                            1  0.0  0.0  0.0  0.0   0.0   1.0
                            2  0.0  0.0  0.0  0.0   0.0   1.0
                            3  0.0  0.0  0.0  0.0   0.0   1.0
                            4  0.0  0.0  0.0  0.0   0.0   1.0
                            5  0.0  0.0  0.0  0.0   0.0   1.0
                            6  0.0  0.0  0.0  0.0   0.0   1.0
                            7  0.0  0.0  0.0  0.0   0.0   1.0
                            8  0.0  0.0  0.0  0.0   0.0   1.0
                            9  0.0  0.0  0.0  0.0   0.0   1.0                                        
                    .slt_time (float): length of slots
                    .gard_band (float): offset to transmit data in a slot
                    .trml_slot (int): slot used by the port to send data-bcn signal to connected TCPS


    """
    def __init__(self, env, list_prt_types=["BE","BE","BE","BE"], \
            list_trml_ids=[None, None, None, None], CT=10e-3, fwd_tbl=None,
            list_prt_rates=[1000,1000,1000,1000],sw_id=None):
        
        self.env = env

        # parameters
        self.list_prt_types = list_prt_types
        self.list_prt_rates = list_prt_rates
        self.list_trml_ids = list_trml_ids
        self.CT = CT
        self.fwd_tbl = fwd_tbl
        self.sw_id = sw_id

        # variables
        self.read_flag = None
        self.GCL = None
        self.slt_add = None
        self.tbl_fid_reg_log = pd.DataFrame()
        self.tbl_fid_reg_log["flow-id"] = []
        self.tbl_fid_reg_log["reg_time"] = []
        self.slt_add
        
        self.tbl_fid_rcv_log = pd.DataFrame()
        self.tbl_fid_rcv_log["flow_id"] = []
        self.tbl_fid_rcv_log["rcv_time"] = []

        self.prtA_type = self.list_prt_types[0]
        self.prtB_type = self.list_prt_types[1]
        self.prtC_type = self.list_prt_types[2]
        self.prtD_type = self.list_prt_types[3]

        # store resources
        self.S_reg = simpy.Store(env)
        self.S_req = simpy.Store(env)
        self.S_rsp = simpy.Store(env)
        self.S_a = simpy.Store(env)
        self.S_b = simpy.Store(env)
        self.S_c = simpy.Store(env)
        self.S_d = simpy.Store(env)
        self.S_fid = simpy.Store(env)
        self.S_r = simpy.Store(env)

        # map input connections to store resources
        self.in_regA = self.S_reg
        self.in_regB = self.S_reg
        self.in_regC = self.S_reg
        self.in_regD = self.S_reg

        self.in_fid_logA = self.S_fid
        self.in_fid_logB = self.S_fid
        self.in_fid_logC = self.S_fid
        self.in_fid_logD = self.S_fid
   
        # output (should always be set to "None")
        self.out_gclA = None
        self.out_gclB = None
        self.out_gclC = None
        self.out_gclD = None
        
        self.out_regA = None
        self.out_regB = None
        self.out_regC = None
        self.out_regD = None

        # running concurrent processes
        self.action = self.r_gcl()
        self.action = self.env.process(self.r_dmux_reg())
        self.action = self.env.process(self.r_req())
        self.action = self.env.process(self.r_rt())
        self.action = self.env.process(self.r_rsp())
        self.action = self.env.process(self.r_fid())

    def r_fid(self):
        """ the function accumulates the received fid log tables in self.tbl_fid_log variable
        """
        while True:
            tbl = (yield self.S_fid.get())
            
            # add tbl info to tbl_fid_log and remove duplicates
            self.tbl_fid_rcv_log =  pd.concat([self.tbl_fid_rcv_log,tbl])
            self.tbl_fid_rcv_log = self.tbl_fid_rcv_log.reset_index(drop=True)
            self.tbl_fid_rcv_log = self.tbl_fid_rcv_log.drop_duplicates(subset=['flow_id'],keep='last')

    def r_rt(self):
        """ route the registration packet to the destination port
        """
        while True:

            ## wait to receive the registration packet
            reg_pkt = (yield self.S_r.get())

            ## find the destination port ID
            dst_port_id = self.fwd_tbl[reg_pkt.dst] 
            
            ## route the registration packet to the destination port
            if(dst_port_id == 1):
                self.out_regA.put(reg_pkt)
            elif(dst_port_id == 2):
                self.out_regB.put(reg_pkt)
            elif(dst_port_id == 3):
                self.out_regC.put(reg_pkt)
            elif(dst_port_id == 4):
                self.out_regD.put(reg_pkt)

    def r_rsp(self):
        """ extract the slot's to lock information from the registration response message

                e.g., format of registration response packet's data field
                    reg_rsp.data = {'trml_slot': 1, 'slots_to_lock': [[1, 2], [1, 2]]}

            extrated information will be in slt_add
                e.g., slt_add
                        ["port"] = the port whoose slots to be alloted
                        ["queue"] = the queue of the port that need to be alloted
                        ["flow_id"] = for logging purposes
                        ["slt_list"] = list of slots to lock
                        ["trml_slot"] = the slot tcps terminal should transmit data
                        ["trml_port"]
                        ["reg_time"] = time of reception of reg_rsp packet

            slt_add is appended in slt_add_log list which is of type dataframe
        """ 
        while True:
            """ port whoose slots to be locked is specified by prt_in 
                queue of the port corresponds to the port to which reg_rsp is destined for
                flow-id is the src-id of TCPS terminal = dst-id of the reg_rsp packet
                slt-list will be the last item in slots_to_lock list
                trml_slot is valid only for the last hop switch in the reg_rsp path
                trml_port is the port to which the transmitting tcps terminal is connected
            """

            reg_rsp_pkt = (yield self.S_rsp.get())

            dst_port_id = self.fwd_tbl[reg_rsp_pkt.dst]

            if(len(reg_rsp_pkt.data["slots_to_lock"]) == 1):
                trml_slot = reg_rsp_pkt.data["trml_slot"]
            else:
                trml_slot = None

            slt_list = reg_rsp_pkt.data["slots_to_lock"].pop()

            # crafting slt_add 
            self.slt_add = {"port": reg_rsp_pkt.prt_in, "queue": dst_port_id,\
                "flow-id": reg_rsp_pkt.dst, "slt_list": slt_list, "trml_slot":\
                trml_slot, "trml_port": dst_port_id, "reg_time": self.env.now}

            # logging slt_add's in a list
            self.tbl_fid_reg_log = self.tbl_fid_reg_log.append(self.slt_add, ignore_index=True)
            self.tbl_fid_reg_log = self.tbl_fid_reg_log.drop_duplicates(subset=['flow-id'], keep='last')
            self.tbl_fid_reg_log = self.tbl_fid_reg_log.reset_index(drop=True)

            # transferring registration response
            self.S_r.put(reg_rsp_pkt)

    def r_req(self):
        """ append the switch's destination port's slot status and transmit rate 
            to the data field of the registration request packet

            e.g., format of registration request packet
                reg_req_pkt.data = {"burst_count":self.burst_count, "pkt_size":self.pkt_size,\
                "tcps_rate": self.rate, "sw_slt_status":[], "sw_rates":[]}
        """
        while True:

            reg_req_pkt = (yield self.S_req.get())

            if(self.read_flag == 1):

                ## set read_flag to zero
                self.read_flag = 0

                ## find the destination port ID
                dst_port_id = self.fwd_tbl[reg_req_pkt.dst] 
                
                ## identify gcl of the destination port
                gcl = None
                if(dst_port_id == 1):
                    gcl = self.GCL["A"]
                elif(dst_port_id == 2):
                    gcl = self.GCL["B"]
                elif(dst_port_id == 3):
                    gcl = self.GCL["C"]
                elif(dst_port_id == 4):
                    gcl = self.GCL["D"]
                    
                ## update "slt_status" in reg_req.data 
                df = gcl.ctrl_list.copy()
                df = df.drop(["q_be"],axis=1).copy()
                df = df.sum(axis=1).copy()
                df = df.clip(upper=1).copy()
                #df = df.replace({0:1, 1:0}) # 1=> free-slts
                reg_req_pkt.data["sw_slt_status"].append(df.tolist())

                ## append destination port's rate to reg_req.data["sw_rates"]
                reg_req_pkt.data["sw_rates"].append(self.list_prt_rates[dst_port_id-1])

                ## transfer the updated registration request
                self.S_r.put(reg_req_pkt)


    def r_dmux_reg(self):
        """ function seperates and routes registration response and 
            request packets onto different paths
        """
        while True:

            pkt = (yield self.S_reg.get())
            if(pkt.type == "reg_req"):
                self.S_req.put(pkt)
            elif(pkt.type == "reg_rsp"):
                self.S_rsp.put(pkt)

    def r_gcl(self):

        # initializing GCL for Ports A, B, C and D
        gcl_A = gcl_packet(self.CT, self.prtA_type)
        gcl_B = gcl_packet(self.CT, self.prtB_type)
        gcl_C = gcl_packet(self.CT, self.prtC_type)
        gcl_D = gcl_packet(self.CT, self.prtD_type)
        self.GCL = {"A":gcl_A, "B":gcl_B, "C":gcl_C, "D":gcl_D}

        # initialize read-flag
        self.read_flag = 1

        # trigger concurrent processes
        self.action = self.env.process(self.r_1())
        self.action = self.env.process(self.r_2())
        self.action = self.env.process(self.r_3())

    def r_2(self):
        while True:
            if(self.read_flag == 0):
                yield self.env.timeout(2*self.CT)
                self.read_flag = 1
            else:
                yield self.env.timeout(self.CT)
    def r_1(self):


        while True:

            '''
            if(self.env.now > 80e-3):
                print "sw-id",self.sw_id
                print "GCL-A", self.GCL["A"].ctrl_list
                print "GCL-B", self.GCL["B"].ctrl_list
                sys.exit()
            '''

            if(self.out_gclA != None):
                self.out_gclA.put(self.GCL["A"])
            if(self.out_gclB != None):
                self.out_gclB.put(self.GCL["B"])
            if(self.out_gclC != None):
                self.out_gclC.put(self.GCL["C"])
            if(self.out_gclD != None):
                self.out_gclD.put(self.GCL["D"])  

            yield self.env.timeout(self.CT)

    def r_3_reserve_slots(self):

        if(self.slt_add != None):
                

                # extract gcl of the required port and allocate slots
                port_id = self.slt_add["port"]
                if(port_id == 1):
                    gcl = self.GCL["A"]
                elif(port_id == 2):
                    gcl = self.GCL["B"]
                elif(port_id == 3):
                    gcl = self.GCL["C"]
                elif(port_id == 4):
                    gcl = self.GCL["D"]
            
                queue_id = self.slt_add["queue"]
                if(queue_id == 1):
                    queue_label = "q1"
                elif(queue_id == 2):
                    queue_label = "q2"
                elif(queue_id == 3):
                    queue_label = "q3"
                elif(queue_id == 4):
                    queue_label = "q4"
                
                for i in self.slt_add["slt_list"]:
                    gcl.ctrl_list[queue_label][i] = 1
                    gcl.ctrl_list["q_be"][i] = 0


                ''' set terminal slot in the gcl of the terminal port and 
                allocate nm slot for sending data-bcn
                '''
                port_id = self.slt_add["trml_port"]
                if(port_id == 1):
                    gcl = self.GCL["A"]
                elif(port_id == 2):
                    gcl = self.GCL["B"]
                elif(port_id == 3):
                    gcl = self.GCL["C"]
                elif(port_id == 4):
                    gcl = self.GCL["D"]

                # adding terminal slot information to GCL
                gcl.trml_slot = self.slt_add["trml_slot"]

                # allocating terminal slot 
                if(gcl.trml_slot != None):
                    gcl.ctrl_list["q_nm"][gcl.trml_slot] = 1
                    gcl.ctrl_list["q_be"][gcl.trml_slot] = 0

                # clean slt_add 
                self.slt_add = None

    def r_3_find_fids_inactive(self):
        """ find flow-id's that are inactive 
        """
        # variables
        n_ct = 4*self.CT # CT multiple to check for flow alive 

        # cs-1: filter TCPS flow entries in tbl_fid_rcv_log that are not older than n_ct
        df = self.tbl_fid_rcv_log.copy()
        df = df[df["flow_id"]>0].copy()
        tbl_rcvA =  df[df["rcv_time"] > (self.env.now - n_ct)].copy()

        # cs-2: filter TCPS flow entries in tbl_fid_reg_log that are not older than n_ct
        df = self.tbl_fid_reg_log.copy()
        tbl_regA =  df[df["reg_time"] < (self.env.now - n_ct)].copy()

        # cs-3: find flow-ids in tbl_regA that do not exist in tbl_rcvA
        lst1 = tbl_regA["flow-id"].tolist()
        lst2 = tbl_rcvA["flow_id"].tolist()

        lst_fids_inactive = map(int, list(set(lst1) - set(lst2)))

        return lst_fids_inactive

    def r_3_deallocate_slots(self, list_flows_inactive):
        """ deallocate slots for inactive flows
        """

        ## return the function if no flows are active
        if(len(list_flows_inactive) == 0):
            return

        
        for i in range(len(list_flows_inactive)):
        
            ## flow-id to delete
            fid_to_delete = list_flows_inactive[i]

            ## find the index corresponding to the flow-id to delete in the registered flow list
            #index = list_flows_registered.index(fid_to_delete)

            ## retreive the slot allocation information for the flow to delete
            slt_del = self.tbl_fid_reg_log[self.tbl_fid_reg_log["flow-id"]==fid_to_delete].to_dict('records')[0]
            self.tbl_fid_reg_log = self.tbl_fid_reg_log[self.tbl_fid_reg_log["flow-id"]!=fid_to_delete].copy()

            #print "debug", self.slt_add_log

            ## deallocate slots

            # extract gcl of the required port and de-allocate slots
            port_id = slt_del["port"]
            if(port_id == 1):
                gcl = self.GCL["A"]
            elif(port_id == 2):
                gcl = self.GCL["B"]
            elif(port_id == 3):
                gcl = self.GCL["C"]
            elif(port_id == 4):
                gcl = self.GCL["D"]
        
            queue_id = slt_del["queue"]
            if(queue_id == 1):
                queue_label = "q1"
            elif(queue_id == 2):
                queue_label = "q2"
            elif(queue_id == 3):
                queue_label = "q3"
            elif(queue_id == 4):
                queue_label = "q4"
            
            for i in slt_del["slt_list"]:
                gcl.ctrl_list[queue_label][i] = 0
                gcl.ctrl_list["q_be"][i] = 1


            ''' set terminal slot in the gcl of the terminal port and 
            deallocate nm slot used for sending data-bcn
            '''
            port_id = slt_del["trml_port"]
            if(port_id == 1):
                gcl = self.GCL["A"]
            elif(port_id == 2):
                gcl = self.GCL["B"]
            elif(port_id == 3):
                gcl = self.GCL["C"]
            elif(port_id == 4):
                gcl = self.GCL["D"]

            trml_slot = slt_del["trml_slot"]

            #print "terminal port, slot", port_id, trml_slot

            if(trml_slot != None):
                gcl.ctrl_list["q_nm"][trml_slot] = 0
                gcl.ctrl_list["q_be"][trml_slot] = 1

       

    def r_3(self):
        """ this function does the following,
            (1) first it reserves slots in gcl 
            (2) next it find non-active flows
            (3) next it deallocate slots for non-active flows

            data-structures
            ---------------

            gcl_packet:  
                attributes
                    .ctrl_list (dataframe)
                        coloumns: q4, q3, q2, q1, q_nm, q_be
                        rows: represent a gate control event
                        1: open the queue gate
                        0: close the queue gate
                        e.g.,
                                q4   q3   q2   q1  q_nm  q_be
                            0  0.0  0.0  0.0  0.0   1.0   0.0
                            1  0.0  0.0  0.0  0.0   0.0   1.0
                            2  0.0  0.0  0.0  0.0   0.0   1.0
                            3  0.0  0.0  0.0  0.0   0.0   1.0
                            4  0.0  0.0  0.0  0.0   0.0   1.0
                            5  0.0  0.0  0.0  0.0   0.0   1.0
                            6  0.0  0.0  0.0  0.0   0.0   1.0
                            7  0.0  0.0  0.0  0.0   0.0   1.0
                            8  0.0  0.0  0.0  0.0   0.0   1.0
                            9  0.0  0.0  0.0  0.0   0.0   1.0                                        
                    .slt_time (float)
                    .gard_band (float)
                    .trml_slot (int)
            

            e.g., slt_add
                ["port"] = the port whoose slots to be alloted
                ["queue"] = the queue of the port that need to be alloted
                ["flow_id"] = for logging purposes
                ["slt_list"] = list of slots to lock
                ["trml_slot"] = the slot tcps terminal should transmit data
                ["trml_port"] = the slot to which the transmitting tcps terminal is connected

            e.g., tbl_fid_log - logs the flow-ids of packets received and last reception times
                    flow_id  rcv_time
                0      0.0  0.010003
                1      2.0  0.091010

            e.g., slt_add_log - dataframe format,
                flow-id  port  queue slt_list  trml_port trml_slot
            0      1.0   2.0    1.0      [1]        1.0      None
            1      2.0   1.0    2.0      [2]        2.0         2
        """
        while True:

            # wait for CT/2
            yield self.env.timeout(self.CT/2.0)
           

            # allocating slots for flows
            self.r_3_reserve_slots()      


            # identifying list of registered, inactive flows
            lst_fids_inactive = self.r_3_find_fids_inactive()
            

            # deallocatting slots for the inactive flows
            self.r_3_deallocate_slots(lst_fids_inactive)

     

            # wait for CT/2
            yield self.env.timeout(self.CT/2.0)
