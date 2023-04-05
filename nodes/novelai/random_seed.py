import random
import math
from nodes.node import Node
from PyQt5.QtGui import QColor

class RandomSeedNode(Node):
    def __init__(self, title="Random Seed", color="gray"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=0, num_output_ports=1)
        self.output_ports[0].label = "Seed"

    def computeOutput(self):
        return math.floor(random.random()*(2**32)-1)
