import pandas as pd
import sys
import matplotlib

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})


## user settings
dst_id = 0 #4
src_id_list = [3,6,9,12,13,14,15,16,19,22,25,28] 
drop_pcnt_list = []

for src_id in src_id_list: 
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
    
    pkt_drop_percent = 100*drop_pkts/(total_pkts)
    
    print "src-id,",src_id,"drop_percent",pkt_drop_percent
    
    drop_pcnt_list.append(pkt_drop_percent)
    
    
# for the purpose of generating graphs
'''
st_id_list = [1,2,4,5,7,8,10,11,26,27,23,24, 17,18,20,21]
for i in st_id_list:
    src_id_list.append(i)
    drop_pcnt_list.append(0)
'''

# drawing graph
dfx = pd.DataFrame()
dfx["src_id"]=src_id_list
dfx["drop_pcnt"]=drop_pcnt_list

ax = dfx.plot(kind='bar',x='src_id', y='drop_pcnt', fontsize='14',figsize=(7,4),style='-*')
ax.get_legend().remove()

#ax.set_xlim([0,2500])
plt.ylabel('packet drop (%)', fontsize = '14')
plt.xlabel('flow-id', fontsize = '14')
#plt.title('Packet Reception Times for Different TCPS Flows')  

plt.tight_layout()


plt.show()

