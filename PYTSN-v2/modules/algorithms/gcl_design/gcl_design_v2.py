""" Algorithm for the TCPS terminals to compute the slots to allocate in
    switches from the registration-request data
    ** this module makes no assumption on transmit rates. Transmit rates 
    can be different for different switches
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
    burst_times = data["burst_size_req"]*8.0/(1e6*np.array(data["sw_rates"]))

    guard_band = be_max_pkt_size*8/(1e6*np.array(min(data["sw_rates"])))

    one_pkt_de2e = data["pkt_size"]*8/(1e6*np.array(min(data["sw_rates"])))
    one_pkt_de2e += (d_processing+d_propogation)
    one_pkt_de2e += guard_band

    # computing the required gate open time (or gate slot width required)
    gate_slot_width_required = burst_times + one_pkt_de2e

    # determining the number of gate slots required
    n_slot = np.ceil(gate_slot_width_required/gcl_one_slot_width)
    
    return(n_slot)

def find_slots_to_lock(reg_req_data, n_slot):
    """ Determine the slot indices to lock in the switches based on the gate_slt_status
        in the switches and n_slot
    """

    # parameters
    n_slt = n_slot.tolist()
    n_slt = [int(i) for i in n_slt] 

    # convert gate_slt_status to a dataframe
    df = pd.DataFrame(reg_req_data["sw_slt_status"])
    
    # replacing 1 with 0 and 0 with 1 (1=> Free Slts)
    df = df.replace({0:1, 1:0})

    df_gate_slt_status = df.transpose().copy()

    # generating the mask dataframe
    row = np.sum(np.array(n_slt))
    col = len(n_slt)
    base_array = np.zeros((row,col))
    df_base = pd.DataFrame(base_array)

    a = np.zeros(0)
    b = np.ones(n_slt[0])
    c = np.zeros(df_base.shape[0]-(len(a)+len(b)))
    df_base.loc[:,0] = np.concatenate((a,b,c))

    for i in range(1, df_base.shape[1]):
        dx = df_base.loc[:,i-1].copy()
        ofst = dx.loc[dx == 1].index.values
        
        if(n_slt[i-1] > n_slt[i]):
            a = np.zeros(ofst[0]+n_slt[i-1]-n_slt[i])
        else:
            a = np.zeros(ofst[0])
            
        b = np.ones(n_slt[i])
        c = np.zeros(df_base.shape[0]-(len(a)+len(b)))
        df_base.loc[:,i] = np.concatenate((a,b,c))
    df_mask = df_base.loc[(df_base!=0).any(1)].copy() # remove rows that are zeros

    # check if mask is found at any portion of the gate slot list
    mask = df_mask.copy()
    df = df_gate_slt_status.copy()

    flag_match_found = False
    for i in range(df.shape[0]):
        if(i+mask.shape[0] > df.shape[0]):
            break
        c = df.loc[i:i+mask.shape[0]-1,:].copy()
        c = c.reset_index(drop=True).copy()
        if(mask.equals(mask*c)==True):
            flag_match_found = True
            index = i
            break

    # identify the slots to lock in each switches
    slots_to_lock = []
    if(flag_match_found == True):
        for i in range(len(n_slt)):
            var = ((mask[i].loc[mask[i]==1].index.values))
            var = var + index
            var = var.tolist()
            var = [int(i) for i in var] 
            slots_to_lock.append(var)

    # drop registration request if match is not found
    drop_req = not(flag_match_found)

    # generate a dictionary to be appended as data in the registration response 
    slots_to_lock = {"slots_to_lock":slots_to_lock}

    return(drop_req, slots_to_lock)

def find_slot_to_transmit(result):
    """ determine the TCPS terminals transmit slot
        the tcps transmit rate should be taken into account to determine
        the terminal transmit slot.
    """


    transmit_slot = result["slots_to_lock"][0]
    result["trml_slot"] = transmit_slot[0]

    return(result)

def gate_slot_allocation(reg_req_data):
    """ Function detemrines the slots to allocate in each switch

    Arguments
    ---------

    reg_req_data: dictionary
        data contained in the registration request
        e.g. format, 

            data = {"burst_count":1250,\
                    "pkt_size": 100,\
                    "sw_slt_status":[(1,1,1),(0,1,1)],\
                    "sw_rates":[1000,1000],\
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
    gcl_one_slot_width = 1e-3 # one slot time width
    be_max_pkt_size = 500 # in bytes
    sw_processing = 0.5e-6 # processing time of switch 
    link_propogation = 0.1e-6 # link propogation delay

    # determines the number of gate slots to allocate in each switch
    n_slot = find_slot_length(reg_req_data, gcl_one_slot_width, be_max_pkt_size,\
        sw_processing, link_propogation)

    drop_req, result  = find_slots_to_lock(reg_req_data, n_slot)


    result = find_slot_to_transmit(result)

    return(drop_req, result)