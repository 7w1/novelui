from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodes.ports import *

class Node(QGraphicsItem):
    def __init__(self, title="", color="gray", num_input_ports=1, num_output_ports=1, port_size=10):
        super().__init__()

        self.title = title
        self.color = QColor(color)
        self.num_input_ports = num_input_ports
        self.num_output_ports = num_output_ports
        self.port_size = port_size
        self.port_spacing = 20
        self.width = 100
        self.height = 60
        self.input_ports = []
        self.output_ports = []
        self.hovered = False

        # self.port_labels = {}  # dictionary to map port labels to port objects

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(1)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)  # enable itemChange signal
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)  # enable caching for better performance

        self.updatePorts()

    def updatePortPos(self):
        # Compute the spacing between input and output ports
        total_height = self.num_input_ports * self.port_size + (self.num_input_ports + self.num_output_ports - 1) * self.port_spacing
        start_y = -total_height / 2 + self.port_size / 2
        port_spacing = total_height / (self.num_input_ports + self.num_output_ports)
        # Position input ports and add their labels to the dictionary
        for i, port in enumerate(self.input_ports):
            port_height = port.rect().height() if hasattr(port, "rect") else self.port_size
            port.setPos(-5 - self.width/2, start_y + (i + 1) * port_spacing - port_height / 2)
            # port.label = f"input {i+1}"
            port.update()
            # self.port_labels[port.label] = port

        # Position output ports and add their labels to the dictionary
        for i, port in enumerate(self.output_ports):
            port_height = port.rect().height() if hasattr(port, "rect") else self.port_size
            port.setPos(-5 + self.width/2, start_y + (i + 1) * port_spacing - port_height / 2)
            # port.label = f"output {i+1}"
            port.update()
            # self.port_labels[port.label] = port

    def updatePorts(self):
        # Currently set inside individual nodes | Create new input and output ports based on the current settings
        self.input_ports = [Port(type="input", parent=self, label=f"input {i+1}") for i in range(self.num_input_ports)]
        self.output_ports = [Port(type="output", parent=self, label=f"output {i+1}") for i in range(self.num_output_ports)]

        self.updatePortPos()

    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.prepareGeometryChange()

    def boundingRect(self):
        return QRectF(-self.width / 2, -self.height / 2, self.width, self.height)
    
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isSelected():
            painter.setPen(QPen(self.color.lighter(200), 2))
            painter.setBrush(self.color.lighter(150))
        else:
            painter.setPen(QPen(self.color.darker(200), 2))
            painter.setBrush(self.color)

        rect = QRectF(-self.width/2, -self.height/2, self.width, self.height)
        painter.drawRoundedRect(rect, 5, 5)

        if self.hovered:
            painter.setPen(QPen(Qt.black, 1, Qt.DotLine))
            painter.drawRect(rect)

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(QPointF(-self.width/2 + 10, -self.height/2 + 20), self.title)


    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def setSize(self, width, height):
        self.width = width
        self.height = height
        self.updatePortPos() # update ports when size is changed
        self.update() # update graphics

    def boundingRect(self):
        return QRectF(-self.width/2, -self.height/2, self.width, self.height)

