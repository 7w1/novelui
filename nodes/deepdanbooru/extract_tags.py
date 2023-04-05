from nodes.node import Node
from PyQt5.QtGui import QColor

class ExtractTagsNode(Node):
    def __init__(self, title="Extract Deepbooru Tags", color="purple"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=1)
        self.input_ports[0].label = "input dictionary"
        self.output_ports[0].label = "keys string"

    def extract_keys_from_dict(self, input_dict):
        keys = list(input_dict.keys())  # Extract keys from dictionary
        keys_string = ', '.join(keys)  # Combine keys into a string separated by comma and space
        return keys_string

    def computeOutput(self):
        input_dict = self.input_ports[0].connections[0].output_port.value
        if input_dict is None or not isinstance(input_dict, dict):
            return None
        keys_string = self.extract_keys_from_dict(input_dict)
        return keys_string
