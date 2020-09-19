# PYTSN-v1.0
A discrete-event network simulator for TSN

## Exp-A: Demonstration and Validation of PYTSN

### Network Topology

<img width="291" alt="fig_exp_eval_setup_pytsn" src="https://user-images.githubusercontent.com/48801729/93668790-9d623780-faac-11ea-9963-8c09e63df7cb.png">

### Running Experiments

Step-1: Edit the ned file simulation parameters. Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-A, configuration-1
sim_time = 10e-3
ned_file = "ned_exp_a_conf_1.py"

Step-2: Type the following command,
$ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
For plotting packet latencies, you may also use the plt_latency.py script in ./tools
  
## Exp-B: ST/BE Ratio Method vs. Our Method of Gate Slot Design

### Network Topology

<img width="291" alt="fig_exp_eval_setup_pytsn" src="https://user-images.githubusercontent.com/48801729/93668790-9d623780-faac-11ea-9963-8c09e63df7cb.png">

### Running Experiments

Step-1: Edit the ned file simulation parameters. Choose the ned file for simulating the appropriate experiment-A configuraiton.
e.g., to simulate experiment-A, configuration-1
sim_time = 10e-3
ned_file = "ned_exp_a_conf_1.py"

Step-2: Type the following command,
$ sudo python run.py

### Viewing Resutls

Packets received by the terminals are stored in the file./results/traffic/ts<terminal-id>
For plotting packet latencies, you may also use the plt_latency.py script in ./tools

