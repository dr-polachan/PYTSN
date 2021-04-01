import pandas as pd
import matplotlib.pyplot as plt

## user settings
terminal_id = 10 #4
src_id = "all"
CT = 10e-3
GCL_cycle = 3
bw_avg_interval = CT

## close all open plots
plt.close('all')

## read data
df = pd.read_csv('../results/traffic/ts'+str(terminal_id)+'.txt')

## filtering
if(src_id != "all"):
    dfx = df[df["src-id"]==src_id].copy()
if(src_id == "all"):
    dfx = df.copy()

## 
dfy = dfx[dfx["rcv-time"]>GCL_cycle*CT].copy()
dfy = dfy[dfy["rcv-time"]<GCL_cycle*CT+CT].copy()
pkts_received_in_bits = dfy["size(B)"].sum()*8
avg_bandwidth = pkts_received_in_bits/bw_avg_interval #bps
avg_bandwidth = avg_bandwidth/1000.0 #Kbps
avg_bandwidth = avg_bandwidth/1000.0 #Mbps

print "averaging window (us):", bw_avg_interval*1000*1000
print "average bandwidth (Mbps):", round(avg_bandwidth,2)


