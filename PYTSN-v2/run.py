import simpy
import time
import os

from modules.traffic import const, poisson

#from modules.channel.blocks import link
#from modules.terminals.blocks import terminal as terminal
#from modules.terminals.blocks import tcps as tcps
#from modules.tsn_switch_ds.blocks import switch as switch_ds
#from modules.tsn_switch_ss.blocks import switch as switch_ss

from modules.channel.blocks import link

from modules.terminals import tcps
from modules.terminals import terminal

#from modules.tsn_switch_ds_v2 import tx
#from modules.tsn_switch_ds_v2 import rx
#from modules.tsn_switch_ds_v2 import pcl
#from modules.tsn_switch_ds_v2 import port
#from modules.tsn_switch_ds_v2 import scl
from modules.tsn_switch_ds_v2 import switch

from modules.traffic import traffic_sink
from modules.traffic import debug_sink

t = time.time()

# clean results folder
os.system("sudo rm -rf ./results/traffic/*.*")

pytsn = simpy.Environment()

execfile("./ini.py")
execfile("./ned.py")

pytsn.run(until=sim_time)


print "+++simulation time =",round(time.time()-t,2),"s"


 