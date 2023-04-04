from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodes.basic.operations import *
from nodes.basic.input import *
from nodes.basic.output import *
from nodes.novelai.gen_img_basic import *
from nodes.novelai.random_seed import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NovelAI Visual Scripting | Pre Pre Pre Pre Pre Alpha Build")
        self.setGeometry(100, 100, 800, 600)

        # Create the scene and view
        self.scene = QGraphicsScene(self)

        # Background grid
        grid = QPixmap(60, 60)
        grid.fill(Qt.black)
        painter = QPainter(grid)
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawLine(0, 2, 4, 2)
        painter.drawLine(2, 0, 2, 4)
        painter.end()  # Release the painting resources
        self.scene.setBackgroundBrush(QBrush(grid))


        self.view = QGraphicsView(self.scene, self)
        self.view.setViewport(QOpenGLWidget()) # For faster rendering
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.setCentralWidget(self.view)

        # Create the toolbar
        self.toolbar = QToolBar("Toolbar", self)
        self.addToolBar(self.toolbar)

        self.basic_math_menu = QMenu("Basic Math", self)
        self.basic_math_menu.addAction("Add", lambda: self.create_node("Add"))
        self.basic_math_menu.addAction("Subtract", lambda: self.create_node("Subtract"))
        self.basic_math_menu.addAction("Multiply", lambda: self.create_node("Multiply"))
        self.basic_math_menu.addAction("Divide", lambda: self.create_node("Divide"))
        self.basic_math_action = self.toolbar.addAction(self.basic_math_menu.menuAction())

        self.basic_io_menu = QMenu("Basic Input/Output", self)
        self.basic_io_menu.addAction("Input Int", lambda: self.create_node("Input Int"))
        self.basic_io_menu.addAction("Input Float", lambda: self.create_node("Input Float"))
        self.basic_io_menu.addAction("Input Text", lambda: self.create_node("Input Text"))
        self.basic_io_menu.addAction("Output", lambda: self.create_node("Output"))
        self.basic_io_menu.addAction("Image Output", lambda: self.create_node("Image Output"))
        self.basic_io_action = self.toolbar.addAction(self.basic_io_menu.menuAction())

        self.novelai_menu = QMenu("NovelAI", self)
        self.novelai_menu.addAction("Generate Image Basic", lambda: self.create_node("Gen Image Basic"))
        self.novelai_menu.addAction("Random Seed", lambda: self.create_node("Random Seed"))
        self.novelai_action = self.toolbar.addAction(self.novelai_menu.menuAction())

        # Add the "Execute Script" action to the toolbar
        self.execute_script_action = QAction("Execute Script", self, triggered=self.runScript)
        self.toolbar.addAction(self.execute_script_action)
        
        self.nodes = []

        # Add zoom slider
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setRange(1, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.valueChanged.connect(self.zoom_view)
        self.statusBar().addWidget(self.zoom_slider)

    def zoom_view(self, value):
        factor = value / 100
        self.view.setTransform(QTransform().scale(factor, factor))


    def create_node(self, node_type):
        # Create a new node of the given type and add it to the scene
        if node_type == "Add":
            node = AddNode()
        elif node_type == "Subtract":
            node = SubtractNode()
        elif node_type == "Multiply":
            node = MultiplyNode()
        elif node_type == "Divide":
            node = DivideNode()
        elif node_type == "Input Int":
            node = InputNode(title="Input Int", input_type=int)
        elif node_type == "Input Float":
            node = InputNode(title="Input Float", input_type=float)
        elif node_type == "Input Text":
            node = InputNode(title="Input Text", input_type=str)
        elif node_type == "Output":
            node = OutputNode()
        elif node_type == "Image Output":
            node = ImageOutputNode()
        elif node_type == "Gen Image Basic":
            node = GenerateImageBasicNode()
        elif node_type == "Random Seed":
            node = RandomSeedNode()
        else:
            return

        self.scene.addItem(node)
        self.nodes.append(node)

    def runScript(self):
        # Find the output node
        output_nodes = [node for node in self.scene.items() if isinstance(node, OutputNode)]
        if not output_nodes:
            return

        # Traverse the graph of connected nodes and compute the output value of each
        node_values = {}
        processed_nodes = set()
        for node in output_nodes:
            self.traverseNode(node, node_values, processed_nodes)

        # Update the output node's widget with its computed output value
        for node in output_nodes:
            node.computeOutput()

    def traverseNode(self, node, node_values, processed_nodes):
        if node in processed_nodes:
            return

        # Traverse input ports and compute values of connected nodes
        for port in node.input_ports:
            if not port.connections:
                continue
            
            connected_port = port.connections[0].output_port
            connected_node = connected_port.parent

            self.traverseNode(connected_node, node_values, processed_nodes)

            # Set the value of the output port of the connected node
            connected_port.value = connected_node.value

        # Compute and store output value of current node
        node.value = node.computeOutput()
        print("Node " + node.title + " output set to " + str(node.value))

        processed_nodes.add(node)



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
