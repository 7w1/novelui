from PyQt5.QtWidgets import QGraphicsProxyWidget, QLineEdit, QMessageBox
from nodes.node import Node
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class InputNode(Node):
    def __init__(self, title="Input", color="gray", input_type=float):
        super().__init__(title, QColor(color).darker(150), num_input_ports=0, num_output_ports=1)

        self.input_type = input_type

        # Create the widget
        self.widget = QLineEdit()
        self.widget.returnPressed.connect(self.on_input_changed)

        # Set up the graphics proxy widget
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(-100, 0)

        self.setSize(220, self.height)

    def computeOutput(self):
        try:
            value = self.input_type(self.widget.text())
            return value
        except ValueError:
            QMessageBox.warning(None, "Error", "Please enter a valid input value.")
            return None

    def on_input_changed(self):
        self.updateConnectedNodes()  # Update the graph when the input changes
