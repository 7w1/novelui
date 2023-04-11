from nodes.node import Node
from PyQt5.QtGui import QColor
from api.upscale import upscale
from PIL import Image
from io import BytesIO

class UpscaleNode(Node):
    def __init__(self, title="Upscale", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["image", "int", "image"])
        
        self.input_ports[0].label = "image"
        self.input_ports[1].label = "scale"
        self.output_ports[0].label = "upscaled image"

    def computeOutput(self):
        image = self.input_ports[0].connections[0].output_port.value
        scale = self.input_ports[1].connections[0].output_port.value

        image_but_opened = Image.open(BytesIO(image))

        zip = upscale(image, image_but_opened.width, image_but_opened.height, scale)
        
        return [zip.read("image.png")]
