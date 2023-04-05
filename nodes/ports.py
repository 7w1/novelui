from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Connection(QGraphicsItem):
    def __init__(self, output_port, input_port=None):
        if input_port != None: print("New connection from "+output_port.label+" to input_port.")
        super().__init__()
        self.output_port = output_port
        self.input_port = input_port
        self.end_point = None

    def paint(self, painter, option, widget):
        if self.output_port and self.end_point:
            path = QPainterPath()
            path.moveTo(self.output_port.scenePos())
            control_point1 = self.output_port.scenePos() + QPointF((self.end_point.x() - self.output_port.scenePos().x()) / 2, 0)
            control_point2 = self.output_port.scenePos() + QPointF((self.end_point.x() - self.output_port.scenePos().x()) / 2, self.end_point.y() - self.output_port.scenePos().y())
            path.cubicTo(control_point1, control_point2, self.end_point)
            painter.drawPath(path)
        elif self.output_port and self.input_port:
            path = QPainterPath()
            path.moveTo(self.output_port.scenePos())
            control_point1 = self.output_port.scenePos() + QPointF((self.input_port.scenePos().x() - self.output_port.scenePos().x()) / 2, 0)
            control_point2 = self.output_port.scenePos() + QPointF((self.input_port.scenePos().x() - self.output_port.scenePos().x()) / 2, self.input_port.scenePos().y() - self.output_port.scenePos().y())
            path.cubicTo(control_point1, control_point2, self.input_port.scenePos())
            painter.drawPath(path)

    def setEndPoint(self, point):
        if self.end_point != point:
            self.end_point = point
            self.update()

class Port(QGraphicsItem):
    def __init__(self, type, label, parent):
        super().__init__(parent)

        self.width = 10
        self.height = 10
        self.type = type
        self.label = label
        self.connections = []
        self.value = None
        self.parent = parent

        self.setAcceptHoverEvents(True)  # enable mouse hover tracking
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.mouse_pressed = False  # flag to prevent multiple mouseReleaseEvents
        self.setZValue(2) # So it gets selected above the nodes

        if self.type == "input":
            self.color = QColor("#E91E63") # pink
            self.text_color = Qt.white
        else:
            self.color = QColor("#2196F3") # blue
            self.text_color = Qt.white

        self.temp_connection = None
        self.hovered = False
    
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1.5))
        
        if self.hovered:
            painter.setBrush(QBrush(self.color.lighter(150)))
        else:
            painter.setBrush(QBrush(self.color))
        
        painter.drawRect(0, 0, self.width, self.height)

        if self.value is not None:
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(QPointF(self.width/2, self.height/2), self.width/4, self.height/4)
        
        # Draw the label
        font = QFont("Arial", 8)
        fm = QFontMetrics(font)
        label_width = fm.width(self.label)
        painter.setPen(QPen(Qt.white, 2))

        if self.type == "input":
            pos = QPointF(-label_width - 5, self.height/2 + fm.height()/2 - 2)
            painter.drawText(pos, self.label)
        else:
            pos = QPointF(self.width + 5, self.height/2 + fm.height()/2 - 2)
            painter.drawText(pos, self.label)

    def connectTo(self, other_port):
        print("Connecting to "+other_port.label)
        if other_port.type == "input" and other_port.connections:
            print("Other port is input port. Clearing current connections.")
            # Input ports can only have one connection, so remove any existing connections
            for connection in other_port.connections:
                if connection.input_port == other_port:
                    self.scene().removeItem(connection)
                    other_port.connections.remove(connection)
                    connection.output_port.connections.remove(connection)
        print("Generating new connection.")
        connection = Connection(self, other_port)
        connection.output_port = self
        connection.input_port = other_port
        connection.update()

        self.connections.append(connection)
        other_port.connections.append(connection)
        self.scene().addItem(connection)
        
    def disconnect(self, other_port):
        for connection in self.connections:
            if connection.output_port == self and connection.input_port == other_port:
                # Remove the connection from the scene
                self.scene().removeItem(connection)

                # Remove the connection from the connections lists of both ports
                self.connections.remove(connection)
                other_port.connections.remove(connection)

                break
    
    def disconnectAll(self):
        for connection in self.connections:
            other_port = connection.input_port
            # TODO: Don't just catch errors and ignore them, stupid
            # Remove the connection from the scene
            try:
                self.scene().removeItem(connection)

                # Remove the connection from the connections lists of both ports
                self.connections.remove(connection)
                if connection in other_port.connections:
                    other_port.connections.remove(connection)
            except:
                return

            break

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def mouseMoveEvent(self, event):
        if self.temp_connection:
            self.temp_connection.setEndPoint(event.scenePos())
        super().mouseMoveEvent(event)

    def createTempConnection(self):
        self.temp_connection = Connection(self, None)
        self.scene().addItem(self.temp_connection)
        self.mouse_pressed = True  # set the flag

    def mousePressEvent(self, event):
        if self.type == "output":
            self.createTempConnection()
        elif self.type == "input":
            if self.connections:
                # Remove existing connection
                connection = self.connections[0]
                other_port = connection.output_port
                self.connections.remove(connection)
                other_port.connections.remove(connection)
                self.scene().removeItem(connection)

                # TODO: Below isnt working for some stupid reason
                #
                # Create new temporary connection on other_port
                # print(other_port.temp_connection)
                # print("creating connection")
                # other_port.createTempConnection()
                # print(other_port.temp_connection)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.temp_connection:
            items = self.scene().items(event.scenePos())
            for item in items:
                if isinstance(item, Port) and item.type != self.type:
                    self.connectTo(item)
            # Update one last time so we don't have a lingering final line
            self.temp_connection.setEndPoint(None)
            self.temp_connection.update()
            # Remove the temp connection from the scene
            self.scene().removeItem(self.temp_connection)
            self.temp_connection = None
        super().mouseReleaseEvent(event)


