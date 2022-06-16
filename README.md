# PYTSN
A discrete-event network simulator for TSN

# OS Requirement
Ubuntu 18.04 or Windows 10 

# Package Requirements
python==2.7,
simpy==3.0.13,
pandas==0.24.2,
matplotlib==2.2.3,

# PYTSN-v2.0
Supports eDDSCH-TSN protocol.

Run directory = PYTSN-v2

## Exp: Demonstration of eDDSCH-TSN protocol

### Network Topology

<img width="500" alt="" src="https://user-images.githubusercontent.com/48801729/113296718-761bdb00-9317-11eb-9ed2-669b303159fa.png">


### Running Experiments

Step-1: Go to run directory PYTSN-v2

Step-2: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet reception times, you may use the plot_packet_reception_times.py script in ./tools

# PYTSN-v1.0
Initial version

Run directory = PYTSN-v1

## Exp-A: Demonstration and Validation of PYTSN

### Network Topology

<img width="291" alt="fig_exp_eval_setup_pytsn" src="https://user-images.githubusercontent.com/48801729/93668790-9d623780-faac-11ea-9963-8c09e63df7cb.png">

### Running Experiments

Step-1: Go to run directory PYTSN-v1

Step-2: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-A, configuration-1, set sim_time = 100e-3 and ned_file = "ned_exp_a_conf_1.py"

Step-3: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools
  
## Exp-B: ST/BE Ratio Method vs. Our Method of Gate Slot Design

### Network Topology

<img width="382" alt="fig_exp_eval_setup_low_gcl" src="https://user-images.githubusercontent.com/48801729/93668940-e49cf800-faad-11ea-9f62-a37aeacc5ace.png">

### Running Experiments

Step-1: Go to run directory PYTSN-v1

Step-2: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-B, configuration-ST/BE ration method for CT=50us, set sim_time = 100e-3 and ned_file = "ned_exp_b_stbe_50u.py"

Step-3: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools

## Exp-D: Evaluation of Our Decentralized Dynamic Gate Scheduling Algorithm

### Network Topology

<img width="288" alt="fig_exp_stbe" src="https://user-images.githubusercontent.com/48801729/102997072-38562c00-454a-11eb-9714-80e919491366.png">

### Running Experiments

Step-1: Go to run directory PYTSN-v1

Step-2: Edit the simulation parameters in file "ini". Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-D, configuration-1, set sim_time = 100e-3 and ned_file = "ned_exp_d_conf_1_rev2.py" and to simulate configuration-2, set ned_file = "ned_exp_d_conf_2_rev2.py"

Step-3: Type the following command, $ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
  
For plotting packet latencies, you may also use the plt_latency.py script in ./tools
  
# Citation
  
If you are using PYTSN for your work, do cite the following manuscripts,
  
1. Kurian Polachan, Chandramani Singh, and T. V. Prabhakar. 2021. Decentralized Dynamic Scheduling of TCPS flows and a Simulator for Time-Sensitive Networking. ACM Trans. Internet Technol. Just Accepted (November 2021). https://doi.org/10.1145/3498729

2. K. Polachan, C. Singh and T. V. Prabhakar, "Decentralized Dynamic Gate Scheduling of IEEE 802.1Qbv Time Aware Shaper and a TSN Simulator for Tactile Cyber-Physical Systems," 2021 IFIP/IEEE International Symposium on Integrated Network Management (IM), 2021, pp. 45-53.

# Contact Information

If you have questions on how to use the network simulator do contact me at kurianpol@gmail.com. 
  
my website - https://sites.google.com/view/kurianpolachan/home
