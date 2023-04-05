from nodes.node import Node
from deepdanbooru_onnx import DeepDanbooru
from PIL import Image
from PyQt5.QtGui import QColor
import io

class DeepDanbooruNode(Node):
    def __init__(self, title="DeepDanbooru", color="purple"):
        super().__init__(title, QColor(color).darker(200), num_input_ports=1, num_output_ports=1)

        self.input_ports[0].label = "image"
        self.output_ports[0].label = "tags"
        
        self.setSize(self.width + 10, self.height)

    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value

        try:
            image = Image.open(io.BytesIO(input_value))
        except Exception as e:
            print("Error opening image:", e)
            return None

        danbooru = DeepDanbooru()
        print(danbooru(image))
        return danbooru(image)