import io
from PIL import Image
from nodes.node import Node
from PyQt5.QtGui import QColor

class ImageResizeNode(Node):
    def __init__(self, title="Image Resize", color="orange"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=3, num_output_ports=1)

        self.input_ports[0].label = "width"
        self.input_ports[1].label = "height"
        self.input_ports[2].label = "image"
        self.output_ports[0].label = "resized image"

    def computeOutput(self):
        # Get input values
        width = self.input_ports[0].connections[0].output_port.value
        height = self.input_ports[1].connections[0].output_port.value
        image_data = self.input_ports[2].connections[0].output_port.value

        # Check if any input is None
        if None in (width, height, image_data):
            return None

        # Open image from raw data
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            print("Error opening image:", e)
            return None

        # Resize image
        try:
            image = image.resize((width, height))
        except Exception as e:
            print("Error resizing image:", e)
            return None

        # Save resized image to memory buffer
        output_buffer = io.BytesIO()
        try:
            image.save(output_buffer, format='PNG')
        except Exception as e:
            print("Error saving resized image:", e)
            return None

        # Get resized image data from memory buffer
        output_data = output_buffer.getvalue()

        return output_data
