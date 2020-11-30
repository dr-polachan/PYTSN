# PYTSN-v1.0
A discrete-event network simulator for TSN

# OS Requirement
Ubuntu 18.04 or Windows 10 

# Package Requirements
python==2.7,
simpy==3.0.13,
pandas==0.24.2,
matplotlib==2.2.3,


## Exp-A: Demonstration and Validation of PYTSN

### Network Topology

<img width="291" alt="fig_exp_eval_setup_pytsn" src="https://user-images.githubusercontent.com/48801729/93668790-9d623780-faac-11ea-9963-8c09e63df7cb.png">

### Running Experiments

Step-1: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-A, configuration-1, set sim_time = 100e-3 and ned_file = "ned_exp_a_conf_1.py"

Step-2: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools
  
## Exp-B: ST/BE Ratio Method vs. Our Method of Gate Slot Design

### Network Topology

<img width="382" alt="fig_exp_eval_setup_low_gcl" src="https://user-images.githubusercontent.com/48801729/93668940-e49cf800-faad-11ea-9f62-a37aeacc5ace.png">

### Running Experiments

Step-1: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-B, configuration-ST/BE ration method for CT=50us, set sim_time = 100e-3 and ned_file = "ned_exp_b_stbe_50u.py"

Step-2: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools

## Exp-D: Evaluation of Our Decentralized Dynamic Gate Scheduling Algorithm

### Network Topology

<img width="429" alt="fig_exp_decentralized_ds_setup" src="https://user-images.githubusercontent.com/48801729/93668986-347bbf00-faae-11ea-8160-1b3bee63302b.png">

### Running Experiments

Step-1: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-D, configuration-1, set sim_time = 100e-3 and ned_file = "ned_exp_d_conf_1.py"

Step-2: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools

