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


cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']


plt.close('all')


## user settings
terminal_ids = [1,2,5,4,7,8,17,18,20,21,23,24,26,27] # destination terminal
## <<<<<<<<<<<<<

df_list = []
## read data
for i in terminal_ids:
    df = pd.read_csv('../results/traffic/ts'+str(i)+'.txt')
    df_list.append(df)

ax=None
for i in range(0,len(df_list)): 
    df = df_list[i]
    if(len(df) != 0):
        df1 = pd.DataFrame()
        df1["flow-id"] = df["flow-id"].copy()
        df1["msg-id"] = df["msg-id"].copy()
        df1["rcv-time"] = df["rcv-time"].copy()
        df1["rcv-time"] = df1["rcv-time"]*1000
        dfx =df1
        label = "flow-id:"+str(df["flow-id"][0])
        ax = dfx.plot(x='rcv-time', y='msg-id', fontsize='14',figsize=(7,4),style='+',ax=ax,label=label)
        ax.legend()

xlim = 0
for i in range(0,len(df_list)): 
    if(len(df_list[i]) != 0):
        if(df_list[i]["rcv-time"].max() > xlim):
            xlim = df_list[i]["rcv-time"].max()
    

ax.set_xlim([0,xlim*1000*(1+10.0/100)])
plt.ylabel('packet-ID', fontsize = '14')
plt.xlabel('reception-time (ms)', fontsize = '14')
#plt.title('Packet Reception Times for Different TCPS Flows')  

plt.tight_layout()


plt.show()
#plt.savefig('./results/fig_exp_reg_dreg_case2.png', dpi=400)
#plt.savefig("./results/fig_exp_reg_dreg_case2.pdf")

ax.legend( prop={'size': 14})





