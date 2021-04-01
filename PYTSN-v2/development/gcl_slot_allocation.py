import sys
import numpy as np
import pandas as pd

# gate slot requirement
n_slt = [2,3,2,2]
data = {"burst_count":80,\
        "pkt_size": 100,
        "gate_slt_status":[(1,1,1,1),(0,1,1,1),(1,1,1,1),(1,1,1,1)],
        "transmit_rates":[1000,500,1000,1000]}


# convert gate_slt_status to a dataframe
df_gate_slt_status = pd.DataFrame(data["gate_slt_status"]).transpose().copy()

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

mask = df_mask.copy()
df = df_gate_slt_status.copy()

flag_match_found = False
for i in range(df.shape[0]):
    if(i+mask.shape[0] > df.shape[0]):
        break
    c = df.loc[i:i+mask.shape[0]-1,:].copy()
    c = c.reset_index(drop=True).copy()
    if(mask.equals(mask*c)==True):
        print "there is a match"
        flag_match_found = True
        index = i
        break

if(flag_match_found == True):
    slots_to_lock = []
    for i in range(len(n_slt)):
        var = ((mask[i].loc[mask[i]==1].index.values))
        var = var + index
        var = var.tolist()
        var = [int(i) for i in var] 
        slots_to_lock.append(var)
    print slots_to_lock

drop_req = not(flag_match_found)
#We need to return, index and n_slt this should be there
#in the registration response. Registration request
#should b edropped if flag_atch_found == False


