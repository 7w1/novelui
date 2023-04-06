#############################################################################
#               This is a placeholder node for testing.                     #
#                                                                           #
#  It does absolutely nothing and should only be used for developing and    #
#       testing graphical changes to nodes, connections, or ports.          #
#                                                                           #
#############################################################################

from nodes.node import Node
from PyQt5.QtGui import QColor

class PlaceholderNode(Node):
    def __init__(self, title="Placeholder", color="purple"):
        super().__init__(title, QColor(color).darker(200), num_input_ports=4, num_output_ports=4, port_formats=["string", "int", "zip", "image", "string", "int", "zip", "image"])

        self.input_ports[0].label = "string"
        self.input_ports[1].label = "int"
        self.input_ports[2].label = "zip"
        self.input_ports[3].label = "image"
        self.output_ports[0].label = "string"
        self.output_ports[1].label = "int"
        self.output_ports[2].label = "zip"
        self.output_ports[3].label = "image"
        
    def computeOutput(self):
        # simply passes through the values give to it
        self.output_ports[1].value = self.input_ports.connections[1].output_port.value
        self.output_ports[2].value = self.input_ports.connections[2].output_port.value
        self.output_ports[3].value = self.input_ports.connections[3].output_port.value
        # Return sets the first output port.
        return self.input_ports.connections[0].output_port.value