from nodes.node import Node
from deepdanbooru_onnx import DeepDanbooru
from PIL import Image
from PyQt5.QtGui import QColor
import io

class DeepDanbooruNode(Node):
    def __init__(self, title="DeepDanbooru", color="#4B0082"):
        super().__init__(title, QColor(color).darker(200), num_input_ports=2, num_output_ports=1, port_formats=["image", "int", "string"])

        self.input_ports[0].label = "image"
        self.input_ports[1].label = "threshold"
        self.output_ports[0].label = "tags"
        
        self.setSize(self.width + 10, self.height)

    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value

        threshold = self.input_ports[1].connections[0].output_port.value if self.input_ports[1].connections else 0.6

        try:
            image = Image.open(io.BytesIO(input_value))
        except Exception as e:
            print("Error opening image:", e)
            return None

        danbooru = DeepDanbooru(threshold=threshold)
        result = danbooru(image)
        keys = list(result.keys())  # Extract keys from dictionary
        keys_string = ', '.join(keys)  # Combine keys into a string separated by comma and space
        return keys_string