import io
import zipfile
from nodes.node import Node

class ZipImagesNode(Node):
    def __init__(self, title="Zip Images", color="orange", num_input_ports=4):
        super().__init__(title, color, num_input_ports=num_input_ports, num_output_ports=1)
        self.output_ports[0].label = "zip_file"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]

        # Check if all input values are available
        if None in input_values:
            return None

        # Create a BytesIO object to hold the zip data
        zip_data = io.BytesIO()

        # Create a zipfile object with the BytesIO object
        with zipfile.ZipFile(zip_data, mode='w') as zip_file:
            # Iterate through the input values (PNG image data) and add them to the zip file
            for i, image_data in enumerate(input_values):
                image_name = f"image_{i}.png"
                zip_file.writestr(image_name, image_data)

        # Get the zip data as bytes
        zip_bytes = zip_data.getvalue()

        # Set the output value as the zip data
        self.output_ports[0].value = zip_bytes

        return zip_bytes
