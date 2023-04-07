from nodes.node import Node
from PyQt5.QtGui import QColor
from api.annotate_image import annotate

class ControlNetNode(Node):
    def __init__(self, title="ControlNet", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=2, port_formats=["string", "image", "image", "image"])
        
        self.input_ports[0].label = "model"
        self.input_ports[1].label = "image"

    def computeOutput(self):
        model = self.input_ports[0].connections[0].output_port.value
        image = self.input_ports[1].connections[0].output_port.value

        zip = annotate(model, image)

        try:
            image_1 = zip.read("image_1.png")
        except KeyError:
            image_1 = None
        
        return [zip.read("image_0.png"), image_1]
