import random
import math
from nodes.node import Node
from PyQt5.QtGui import QColor

class RandomSeedNode(Node):
    def __init__(self, title="Random Seed", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=0, num_output_ports=1, port_formats=["int"])
        self.output_ports[0].label = "seed"
        self.setSize(self.width+20, self.height)

    def computeOutput(self):
        return [math.floor(random.random()*(2**32)-1)]
