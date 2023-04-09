from nodes.node import Node
from PyQt5.QtGui import QColor
from api.annotate_image import annotate

class ControlNetNode(Node):
    def __init__(self, title="ControlNet", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=6, num_output_ports=2, port_formats=["string", "image", "int", "int", "int", "int", "image", "image"])
        
        self.input_ports[0].label = "model"
        self.input_ports[1].label = "image"
        self.input_ports[2].label = "palette lock/hed - low threshold"
        self.input_ports[3].label = "palette lock/hed - high threshold"
        self.input_ports[4].label = "building control/mlsd - distance threshold"
        self.input_ports[5].label = "building control/mlsd - value threshold"
        self.output_ports[0].label = "controlnet_condition"
        self.output_ports[1].label = "midas/form lock extra image"

        self.setSize(self.width, 110)

    def computeOutput(self):
        model = self.input_ports[0].connections[0].output_port.value
        image = self.input_ports[1].connections[0].output_port.value
        try:
            low_threshold = self.input_ports[2].connections[0].output_port.value
        except:
            low_threshold = None
        try:
            high_threshold = self.input_ports[3].connections[0].output_port.value
        except:
            high_threshold = None
        try:
            distance_threshold = self.input_ports[4].connections[0].output_port.value
        except:
            distance_threshold = None
        try:
            value_threshold = self.input_ports[5].connections[0].output_port.value
        except:
            value_threshold = None

        if model == 'hed' and low_threshold is not None and high_threshold is not None:
            zip = annotate(model, image, low_threshold=low_threshold, high_threshold=high_threshold)
        elif model == 'mlsd' and distance_threshold is not None and value_threshold is not None:
            zip = annotate(model, image, distance_threshold=distance_threshold, value_threshold=value_threshold)
        else:
            zip = annotate(model, image)

        try:
            image_1 = zip.read("image_1.png")
        except KeyError:
            image_1 = None
        
        return [zip.read("image_0.png"), image_1]
