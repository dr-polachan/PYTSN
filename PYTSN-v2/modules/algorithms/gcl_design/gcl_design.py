""" Algorithm for the TCPS terminals to compute the slots to allocate in
    switches from the registration-request data
    ** this module assume that all transmit rates are same
"""

import pandas as pd
import numpy as np

def find_slot_length(reg_req_data, gcl_one_slot_width, be_max_pkt_size,\
        sw_processing, link_propogation):
    '''
    Function returns the array n_slot the required number of gate slots
    to allocate in each switch.

    e.g., reg_req_data format
    data = {"burst_count":1250,\
        "pkt_size": 100,\
        "sw_slt_status":[(1,1,1),(0,1,1)],\
        "sw_rates":[1000,1000],\
        }
    '''

    # parameters
    data = reg_req_data
    d_processing = sw_processing
    d_propogation = link_propogation

    # computing burst-times in different switches
    data["burst_size_req"] = data["burst_count"]*data["pkt_size"]
    burst_times = data["burst_size_req"]*8.0/(1e6*np.array(data["transmit_rates"]))

    ## debug-assumptions: transmit-rates are going to be the same in the network
    hop_count = len(data["transmit_rates"])

    guard_band = be_max_pkt_size*8/(1e6*np.array(min(data["transmit_rates"])))

    one_pkt_de2e = hop_count*data["pkt_size"]*8/(1e6*np.array(min(data["transmit_rates"])))
    one_pkt_de2e += hop_count*(d_processing+d_propogation)
    one_pkt_de2e += guard_band

    '''
    # computing one-pkt end-to-end delay
    hop_count = len(data["transmit_rates"])
    print "hop_count", hop_count
    guard_band = be_max_pkt_size*8/(1e6*np.array(data["transmit_rates"]))
    one_pkt_de2e = hop_count*data["pkt_size"]*8/(1e6*np.array(data["transmit_rates"]))

    one_pkt_de2e += hop_count*(d_processing+d_propogation)
    one_pkt_de2e += guard_band
    '''

    # computing the required gate open time (or gate slot width required)
    gate_slot_width_required = burst_times + one_pkt_de2e


    # determining the number of gate slots required
    n_slot = np.ceil(gate_slot_width_required/gcl_one_slot_width)
    
    return(n_slot)

def find_slots_to_lock(reg_req_data, n_slot):

    #print "n_slot", n_slot

    # convert gate_slt_status to a dataframe
    df = pd.DataFrame(reg_req_data["gate_slt_status"])
    df_gate_slt_status = df.transpose().copy()
    #print df_gate_slt_status

    # convert the n_slot to a dataframe 
    n_slt = [1, 1, 1, 1]
    df = pd.DataFrame(n_slt)
    df_slt_mask = df.transpose().copy()
    #print "slot mask"
    #print df_slt_mask

    # find the slot 
    flag_slot_found = False
    slot_index = None
    for i in range(df_gate_slt_status.shape[0]):
        df = pd.DataFrame(df_gate_slt_status.loc[i,:]).copy()
        df = df.transpose().copy()
        df = df.reset_index(drop=True).copy()
        if(df.equals(df_slt_mask) == True):
            slot_index = i
            flag_slot_found = True
            break

    if(flag_slot_found == True):
        #print "slot-to-allot",slot_index
        drop_req = False
    else:
        drop_req = True

    slots_to_lock = {"lock_slots":[slot_index]}

    return(drop_req, slots_to_lock)

def gate_slot_allocation(reg_req_data):
    """ Function detemrines the slots to allocate in each switch

    Arguments
    ---------

    reg_req_data: dictionary
        data contained in the registration request
        e.g. format,
            data = {"burst_count":1250,\
                    "pkt_size": 100,\
                    "gate_slt_status":[(1,1,1),(0,1,1)],\
                    "transmit_rates":[1000,1000],\
                    }

    Return Parameters
    -----------------
    drop_req: bool
        True if the function is not able to find free slots. The TCPS terminal
        can use this parameter to decide if it has to drop the registration-request
    slot_to_lock: dictionary
        slots to lock in the switches, the parameter is embedded in the
        registration response message.
    
    e.g., reg_req_data format
    
    """
    # parameters
    gcl_one_slot_width = 50e-6
    be_max_pkt_size = 500
    sw_processing = 0.5e-6
    link_propogation = 0.1e-6

    # determines the number of gate slots to allocate in each switch
    n_slot = find_slot_length(reg_req_data, gcl_one_slot_width, be_max_pkt_size,\
        sw_processing, link_propogation)

    drop_req, slots_to_lock  = find_slots_to_lock(reg_req_data, n_slot)
    
    return(drop_req, slots_to_lock)