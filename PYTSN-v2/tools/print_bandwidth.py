import pandas as pd
import sys
import matplotlib

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import matplotlib.pyplot as plt

## user settings
terminal_id = 0 #4
src_id = "all"
CT = 10e-3
GCL_cycle = 12
bw_avg_interval = CT

## close all open plots
plt.close('all')

time_ms = []
avg_bw = []
for GCL_cycle in range (0,250):
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
    
    #print "gcl-cycle:",GCL_cycle
    #print "averaging window (ms):", bw_avg_interval
    #print "average bandwidth (Mbps):", round(avg_bandwidth,2)
    print GCL_cycle*10e-3,round(avg_bandwidth,2)
    time_ms.append(GCL_cycle*10e-3)
    avg_bw.append(round(avg_bandwidth,2))


dfx = pd.DataFrame()
dfx["time"]=time_ms
dfx["avg-bw"]=avg_bw

dfx["time"]=dfx["time"]*1000

ax = dfx.plot(x='time', y='avg-bw', fontsize='14',figsize=(7,4),style='-*')
ax.get_legend().remove()

ax.set_xlim([0,2500])
plt.ylabel('reception rate (Mbps)', fontsize = '14')
plt.xlabel('time (ms)', fontsize = '14')
#plt.title('Packet Reception Times for Different TCPS Flows')  

plt.tight_layout()


plt.show()