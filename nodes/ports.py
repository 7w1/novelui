from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Connection(QGraphicsItem):
    def __init__(self, output_port, input_port=None):
        if input_port is not None: print(f"New connection from {output_port.label}, {output_port.parent.title} to {input_port.label}, {input_port.parent.title}.")
        super().__init__()
        self.output_port = output_port
        self.input_port = input_port
        self.end_point = None

    def paint(self, painter, option, widget):
        if not self.output_port:
            return
        path = QPainterPath()
        path.moveTo(self.output_port.scenePos() + QPointF(0, 5))
        if self.end_point:
            end_pos = self.end_point + QPointF(0, 5)
        elif self.input_port:
            end_pos = self.input_port.scenePos() + QPointF(0, 5)
        else:
            return
        x_diff = end_pos.x() - self.output_port.scenePos().x()
        control_point1 = self.output_port.scenePos() + QPointF(x_diff / 2, 0)
        control_point2 = self.output_port.scenePos() + QPointF(x_diff / 2, end_pos.y() - self.output_port.scenePos().y())
        path.cubicTo(control_point1, control_point2, end_pos)

        # Enable anti-aliasing
        painter.setRenderHint(QPainter.Antialiasing)

        # Get color based on format
        if self.output_port.format == "string":
            color = QColor("#9B59B6")  # purple
        elif self.output_port.format == "int":
            color = QColor("#AF7AC5")  # lighter purple
        elif self.output_port.format == "zip":
            color = QColor("#BB8FCE")  # light purple
        elif self.output_port.format == "image":
            color = QColor("#C39BD3")  # lightest purple
        else:
            color = QColor("#BDC3C7")  # light gray

        # Set pen color and draw path
        pen = QPen(color, 3)
        painter.setPen(pen)
        painter.drawPath(path)


    def setEndPoint(self, point):
        if self.end_point != point:
            self.end_point = point
            self.update()

    def boundingRect(self):
        return QRectF(0, 0, 0, 0)


class Port(QGraphicsItem):
    def __init__(self, type, label, parent, format):
        super().__init__(parent)

        self.width = 10
        self.height = 10
        self.type = type
        self.label = label
        self.connections = []
        self.value = None
        self.parent = parent
        self.format = format # string, int, zip, or image

        self.setAcceptHoverEvents(True)  # enable mouse hover tracking
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.mouse_pressed = False  # flag to prevent multiple mouseReleaseEvents
        self.setZValue(2) # So it gets selected above the nodes

        self.color = QColor("#FFFFFF") # ngl i forgot what these do
        self.text_color = Qt.white # but I'm too lazy to get rid of them :P

        self.temp_connection = None
        self.hovered = False
    
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        # Set the pen color to the color based on format and type
        color = {
            "string": QColor("#9B59B6"),  # purple
            "int": QColor("#AF7AC5"),  # lighter purple
            "zip": QColor("#BB8FCE"),  # light purple
            "image": QColor("#C39BD3")  # lightest purple
        }.get(self.format, QColor("#BDC3C7"))  # light gray
        out_color = {
            "string": QColor("#E67E22"),  # orange
            "int": QColor("#EB984E"),  # lighter orange
            "zip": QColor("#F5B041"),  # light orange
            "image": QColor("#F7DC6F")  # lightest orange
        }.get(self.format, QColor("#BDC3C7"))  # light gray

        
        if self.hovered or self.temp_connection:
            color = color.darker(150)

        if (self.hovered or self.temp_connection) and not self.connections:
            out_color = out_color.darker(100)
        elif self.connections and (self.hovered or self.temp_connection):
            out_color = out_color.lighter(150)
        elif self.connections:
            out_color = out_color
        else:
            out_color = QColor("#BDC3C7")
        painter.setPen(QPen(out_color, 1.5))
        
        # Make the center of the icon darker
        if not self.connections:
            color = color.darker(160)
        else:
            color = color.darker(200)

        painter.setBrush(QBrush(color))
        
        # Change shape based on the format value
        if self.format == "int":
            painter.drawRect(0, 0, self.width, self.height)
        elif self.format == "zip":
            side = min(self.width, self.height)
            x = (self.width - side) / 2 + side * 0.1
            y = (self.height - side * 0.5) / 2 - side * 0.25  # shift up by 10% of side
            path = QPainterPath()
            path.moveTo(x, y)
            path.lineTo(x + side, y + side * 0.5)
            path.lineTo(x, y + side)
            path.closeSubpath()
            painter.drawPath(path)
        elif self.format == "string":
            painter.drawEllipse(QRectF(0, 0, self.width, self.height))
        elif self.format == "image":
            path = QPainterPath()
            path.moveTo(self.width / 2, 0)
            path.lineTo(self.width, self.height / 2)
            path.lineTo(self.width / 2, self.height)
            path.lineTo(0, self.height / 2)
            path.closeSubpath()
            painter.drawPath(path)
        
        # Draw the label
        font = QFont("Arial", 9)

        fm = QFontMetrics(font)
        label_width = fm.boundingRect(self.label).width()
        
        out_color = QColor("#BDC3C7")
        painter.setFont(font)
        painter.setPen(QPen(out_color, 2))

        if self.type == "output":
            pos = QPointF(15, 8)
        else:
            pos = QPointF(-label_width - 5, 8)

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
                connection.scene().removeItem(connection)

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

