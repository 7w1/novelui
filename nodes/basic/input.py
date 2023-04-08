from PyQt5.QtWidgets import QGraphicsProxyWidget, QLineEdit, QPlainTextEdit
from nodes.node import Node
from PyQt5.QtGui import QColor


class InputNode(Node):
    def __init__(self, title="Input", color="#5F9EA0", input_type=float, export_type="int"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=0, num_output_ports=1, port_formats=[export_type])

        self.input_type = input_type

        # Create the widget
        if self.input_type == str:
            self.widget = QPlainTextEdit()
            self.widget.setFixedSize(200, 120)
            self.height = 160
            self.posY = -50
            self.widget.setPlaceholderText("Enter some text...")
        else:
            self.widget = QLineEdit()
            self.posY = -1
            self.widget.setPlaceholderText("Enter a number...")
            self.height -= 10

        # Set up the graphics proxy widget
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(-100, self.posY)

        self.setSize(220, self.height)

    def computeOutput(self):
        try:
            value = self.input_type(self.widget.toPlainText() if self.input_type == str else self.widget.text())
            return [value]
        except ValueError:
            return None
        
    def __getstate__(self):
        state = self.__dict__.copy()
        state["widget_text"] = self.widget.text()  # save the widget text
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.widget = QLineEdit(state["widget_text"])  # create a new widget with the saved text
        self.widget.returnPressed.connect(self.on_input_changed)
        self.proxy = None  # don't restore the graphics proxy widget