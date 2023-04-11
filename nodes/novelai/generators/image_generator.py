from nodes.node import Node
from PyQt5.QtGui import QColor
from api.generate_image import generate

class ImageGeneratorNode(Node):
    def __init__(self, title="Image Generator", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=1, port_formats=["string", "image"])
        
        self.input_ports[0].label = "prompt"
        self.setSize(150, self.height)

    def computeOutput(self):
        # Get input values from input ports
        prompt_builder_output = self.input_ports[0].connections[0].output_port.value

        return [generate(**prompt_builder_output)]

