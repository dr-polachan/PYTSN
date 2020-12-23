import pandas as pd
import matplotlib.pyplot as plt

## user settings
terminal_id = 10 #5 #4
src_id = 9
plot = False


## read data
df = pd.read_csv('../results/traffic/ts'+str(terminal_id)+'.txt')

## filtering
dfx = df[df["src-id"]==src_id].copy()

## process data
dfx['latency_in_ms'] = 1000*(dfx['rcv-time'] - dfx['snd-time'])
dfx['latency_in_us'] = 1000*(dfx['latency_in_ms'])

ylimit_max = dfx['latency_in_us'].max()
ylimit_min = dfx['latency_in_us'].min()

print "src-id:", src_id, ", dst-id:", terminal_id
print "count of packets:", len(dfx)
print "latency-minimum (us):", round(ylimit_min,2)
print "latency-maximum (us):", round(ylimit_max,2)

## plot data
if(plot==True):
    ## close all open plots
    plt.close('all')
    ax = dfx.plot(kind='bar',x='msg-id', y='latency_in_us', fontsize='12',figsize=(7, 4))
    ax.set_ylim([0,1e-10+ylimit_max*(1+10.0/100)])
    ax.get_legend().remove()
    plt.xlabel('message-id', fontsize = '14')
    plt.ylabel('latency (us)', fontsize = '14')
    plt.tight_layout()


