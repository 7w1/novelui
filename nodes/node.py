from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodes.ports import *

class Node(QGraphicsItem):
    def __init__(self, title="", color="gray", num_input_ports=1, num_output_ports=1, port_size=10, port_formats=["string", "string"]):
        super().__init__()

        self.title = title
        self.color = QColor(color)
        self.num_input_ports = num_input_ports
        self.num_output_ports = num_output_ports
        self.port_size = port_size
        self.port_spacing = 20
        self.width = 100
        self.height = 70
        self.input_ports = []
        self.output_ports = []
        self.hovered = False
        self.port_formats = port_formats

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
        port_offset = 5  # gap between ports
        x_left = -self.width/2 - 5  # x position of left side
        x_right = x_left + self.width  # x position of right side
        y_start = -self.height / 2 + 10
        
        for i, port in enumerate(self.input_ports):
            port.setPos(x_left, y_start + i * (self.port_size + port_offset))
            
        y_start = -self.height / 2 + 10
        
        for i, port in enumerate(self.output_ports):
            port.setPos(x_right, y_start + i * (self.port_size + port_offset))



    def updatePorts(self):
        # Create new input and output ports based on the current settings
        self.input_ports = [Port(type="input", parent=self, label=f"input {i+1}", format=self.port_formats[i])
                            for i in range(self.num_input_ports)]
        self.output_ports = [Port(type="output", parent=self, label=f"output {i+1}", 
                            format=self.port_formats[i+self.num_input_ports]) for i in range(self.num_output_ports)]

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

