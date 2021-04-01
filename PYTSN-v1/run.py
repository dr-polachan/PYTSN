import simpy
import time
import os

from modules.traffic.dist import const, poisson
from modules.channel.blocks import link
from modules.terminals.blocks import terminal as terminal
from modules.terminals.blocks import tcps as tcps
from modules.tsn_switch_ds.blocks import switch as switch_ds
from modules.tsn_switch_ss.blocks import switch as switch_ss

# clean results folder
os.system("sudo rm -rf ./results/traffic/*.*")

pytsn = simpy.Environment()

execfile("./ini.py")
execfile("./"+ned_file)

pytsn.run(until=sim_time)


 