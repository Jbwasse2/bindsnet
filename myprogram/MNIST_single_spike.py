import bindsnet

import pdb
import math

from bindsnet.datasets import MNIST
from bindsnet.network import Network
from bindsnet.pipeline import Pipeline
from bindsnet.learning import MSTDPET
from bindsnet.encoding import timing
from bindsnet.network.topology import Connection
from bindsnet.environment import DatasetEnvironment
from bindsnet.network.nodes import Input, LIFNodes
from bindsnet.pipeline.action import select_multinomial

N_INPUT = 784
N_HIDDEN = 1000
N_OUT = 50
ALPHA = 1.5

W_COEFF = 500

# Build network.
network = Network(dt=1.0)

# Layers of neurons.
input = Input(n=N_INPUT, shape=[N_INPUT], traces=True)
hidden = LIFNodes(n=N_HIDDEN, traces=True, thresh=1.0, decay=0.1)
output = LIFNodes(n=N_OUT, refrac=0, traces=True, thresh=1.0, decay=0.1)

in_hidden = Connection(source=input, target=hidden, wmin=0.3, wmax=0.5)
hidden_out = Connection(source=hidden, target=output, wmin=0.3, wmax=0.5)

# Add all layers and connections to the network.
network.add_layer(input, name='IN')
network.add_layer(hidden, name='HIDDEN')
network.add_layer(output, name='OUT')
network.add_connection(in_hidden, source='IN', target='HIDDEN')
network.add_connection(hidden_out, source='HIDDEN', target='OUT')

environment = DatasetEnvironment(dataset=MNIST(path='../../data/MNIST',
                                 download=True), train=True)

pipeline = Pipeline(network, environment, encoding=timing,
                    time=100, plot_interval=1)

# Run environment simulation and network training.
n_episode = 0
n_step = 0
while True:
    pipeline.step()
    n_step += 1
    print('{}th episode\'s {}th step'.format(n_episode,n_step))
    if pipeline.done:
        n_episode += 1
        n_step = 0
        pipeline.reset_()
