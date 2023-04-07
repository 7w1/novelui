from PyQt5.QtWidgets import QMessageBox
from nodes.node import Node
from PyQt5.QtGui import QColor

class AddNode(Node):
    def __init__(self, title="Add", color="#BF00FF"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["int", "int", "int"])

        self.input_ports[0].label = "augend"
        self.input_ports[1].label = "addend"
        self.output_ports[0].label = "sum"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [sum(input_values)]


class SubtractNode(Node):
    def __init__(self, title="Subtract", color="#BF00FF"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["int", "int", "int"])

        self.input_ports[0].label = "minuend"
        self.input_ports[1].label = "subtrahend"
        self.output_ports[0].label = "difference"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [input_values[0] - input_values[1]]


class MultiplyNode(Node):
    def __init__(self, title="Multiply", color="#BF00FF"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["int", "int", "int"])

        self.input_ports[0].label = "factor 1"
        self.input_ports[1].label = "factor 2"
        self.output_ports[0].label = "product"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        return [input_values[0] * input_values[1]]


class DivideNode(Node):
    def __init__(self, title="Divide", color="#BF00FF"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["int", "int", "int"])

        self.input_ports[0].label = "dividend"
        self.input_ports[1].label = "divisor"
        self.output_ports[0].label = "quotient"

    def computeOutput(self):
        input_values = [port.connections[0].output_port.value for port in self.input_ports]
        if None in input_values:
            return None
        if input_values[1] == 0:
            QMessageBox.warning(None, "Error", "Cannot divide by zero.")
            return None
        return [input_values[0] / input_values[1]]
