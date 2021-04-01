import pandas as pd
import matplotlib.pyplot as plt

### Needs revision. (the method is not correct)

## user settings
dst_id = 1 #4
src_id = 2 

## read data
df = pd.read_csv('../results/traffic/ts'+str(dst_id)+'.txt')

## filtering
dfx = df[df["src-id"]==src_id].copy()

dfx["msg-id-diff"] = dfx.diff()["msg-id"]

dfy = pd.DataFrame()
dfy["msg-id-diff"] = dfx["msg-id-diff"][1:].copy()
dfy["msg-id-diff"] = dfy["msg-id-diff"] - 1

total_pkts = dfx["msg-id"].iloc[-1]
drop_pkts =  dfy["msg-id-diff"].sum()

'''
def find_missing(lst): 
    return [x for x in range(lst[0], lst[-1]+1)  
                               if x not in lst] 


drop_count = len(find_missing(dfx["msg-id"].tolist()))

pkt_drop_percent = drop_count/(drop_count + len(dfx))
'''

pkt_drop_percent = 100*drop_pkts/(total_pkts)

## 
print "packet count", total_pkts
print "drop packet count", drop_pkts
print "packet drop (%):", round(pkt_drop_percent,3)


