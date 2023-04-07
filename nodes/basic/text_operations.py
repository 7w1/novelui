from nodes.node import Node
from PyQt5.QtGui import QColor

class TextAddNode(Node):
    def __init__(self, title="Text Add", color="#9932CC"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "string"])

        self.input_ports[0].label = "string 1"
        self.input_ports[1].label = "string 2"
        self.output_ports[0].label = "result"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [input_values[0] + input_values[1]]


class TextSubtractNode(Node):
    def __init__(self, title="Text Subtract", color="#9932CC"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "string"])

        self.input_ports[0].label = "string 1"
        self.input_ports[1].label = "string 2"
        self.output_ports[0].label = "result"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [input_values[0].replace(input_values[1], "")]


class TextMultiplyNode(Node):
    def __init__(self, title="Text Multiply", color="#9932CC"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "string"])

        self.input_ports[0].label = "string"
        self.input_ports[1].label = "multiplier"
        self.output_ports[0].label = "result"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [input_values[0] * input_values[1]]

class TextCutCharactersNode(Node):
    def __init__(self, title="Text Cut Characters", color="#9932CC"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "string"])

        self.input_ports[0].label = "input string"
        self.input_ports[1].label = "number of characters"
        self.output_ports[0].label = "result"

    def computeOutput(self):
        input_string = self.input_ports[0].connections[0].output_port.value
        num_characters = self.input_ports[1].connections[0].output_port.value
        if input_string is None or num_characters is None:
            return None
        return [input_string[:num_characters]]

class TextCutWordsNode(Node):
    def __init__(self, title="Text Cut Words", color="#9932CC"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "string"])

        self.input_ports[0].label = "input string"
        self.input_ports[1].label = "number of words"
        self.output_ports[0].label = "result"

    def computeOutput(self):
        input_string = self.input_ports[0].connections[0].output_port.value
        num_words = self.input_ports[1].connections[0].output_port.value
        if input_string is None or num_words is None:
            return None
        words = input_string.split()
        return [" ".join(words[:num_words])]