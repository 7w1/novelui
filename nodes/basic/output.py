from PyQt5.QtWidgets import QGraphicsProxyWidget, QLabel
from nodes.node import Node
from PyQt5.QtGui import QColor, QPixmap

class OutputNode(Node):
    def __init__(self, title="Output", color="gray"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=0)
        
        self.widget = QLabel("No input")
        
        # Set the widget stylesheet to make the background transparent
        self.widget.setStyleSheet("background-color: transparent;")
        
        # Set up the graphics proxy widget
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.widget)
        self.proxy.setPos(-25, 0)


    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value
        if input_value is not None:
            self.widget.setText(str(input_value))
        else:
            self.widget.setText("No input")

        # Update node size based on text width
        text_width = self.widget.fontMetrics().boundingRect(self.widget.text()).width()
        widget_width = self.widget.width()
        if text_width > widget_width:
            self.setSize(text_width + 20, self.height)
            self.proxy.resize(text_width + 20, self.proxy.size().height())

        return "No input" if input_value is None else str(input_value)


class ImageOutputNode(OutputNode):
    def __init__(self, title="Image Output", color="gray"):
        super().__init__(title, color)
        self.widget.setFixedSize(100, 100)

    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value
        if input_value is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(input_value)
            self.widget.setPixmap(pixmap)
            self.widget.setFixedSize(pixmap.width(), pixmap.height())
            self.proxy.setPos(-pixmap.width()/2, -pixmap.height()/2)
            self.setSize(pixmap.width() + 30, pixmap.height() + 50)
        else:
            self.widget.setPixmap(QPixmap(""))
            self.widget.setFixedSize(100, 100)
            self.setSize(130, 80)
        return None

