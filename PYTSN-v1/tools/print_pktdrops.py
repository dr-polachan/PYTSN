import pandas as pd
import matplotlib.pyplot as plt

### Needs revision. (the method is not correct)

## user settings
terminal_id = 10 #4
src_id = 2 

## read data
df = pd.read_csv('../results/traffic/ts'+str(terminal_id)+'.txt')

## filtering
dfx = df[df["src-id"]==src_id].copy()

def find_missing(lst): 
    return [x for x in range(lst[0], lst[-1]+1)  
                               if x not in lst] 

drop_count = len(find_missing(dfx["msg-id"].tolist()))

pkt_drop_percent = drop_count/(drop_count + len(dfx))

## 
print "packet count", len(dfx)
print "drop packet count", drop_count
print "packet drop (%):", round(pkt_drop_percent,3)


