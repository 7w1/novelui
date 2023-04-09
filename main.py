from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from save_load import *
from progress_popup import *
from nodes.basic.operations import *
from nodes.basic.input import *
from nodes.basic.output import *
from nodes.basic.text_operations import *
from nodes.deepdanbooru.deepdanbooru import *
from nodes.files.zip import *
from nodes.images.open import *
from nodes.images.save import *
from nodes.images.grid_gen import *
from nodes.images.basic_resize import *
from nodes.novelai.image_generator import *
from nodes.novelai.cluster_generator import *
from nodes.novelai.cluster_generator_advanced import *
from nodes.novelai.prompt_builder import *
from nodes.novelai.random_seed import *
from nodes.novelai.controlnet.annotate_image import *
from nodes.placeholder import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.savinator = Savinator()

        self.setWindowTitle("NovelUI for NovelAI | Pre Pre Pre Pre Alpha Build")
        self.setGeometry(100, 100, 800, 600)

        # Create the scene and view
        self.scene = QGraphicsScene(self)

        # Background grid
        grid = QPixmap(60, 60)
        grid.fill(QColor("#1D1D20"))
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

        # Create progress popup
        self.progress_popup = ProgressPopup()

        self.image_menu = QMenu("Files", self)
        # self.image_menu.addAction("Save Node Layout", lambda: self.savinator.save())
        # self.image_menu.addAction("Load Node Layout", lambda: self.prompt_load())
        self.image_menu.addAction("Open Image", lambda: self.create_node("Open Image"))
        self.image_menu.addAction("Save Image", lambda: self.create_node("Save Image"))
        self.image_menu.addAction("Grid Generator", lambda: self.create_node("Gen Grid"))
        self.image_menu.addAction("Resize Image (Basic)", lambda: self.create_node("Resize"))
        self.image_menu.addAction("Zip Images", lambda: self.create_node("Zip"))
        self.image_action = self.toolbar.addAction(self.image_menu.menuAction())

        self.basic_io_menu = QMenu("User Input", self)
        self.basic_io_menu.addAction("Input Number", lambda: self.create_node("Input Number"))
        self.basic_io_menu.addAction("Input Text", lambda: self.create_node("Input Text"))
        self.basic_io_action = self.toolbar.addAction(self.basic_io_menu.menuAction())

        self.display_menu = QMenu("Display", self)
        self.display_menu.addAction("Output", lambda: self.create_node("Output"))
        self.display_menu.addAction("Image Output", lambda: self.create_node("Image Output"))
        self.display_action = self.toolbar.addAction(self.display_menu.menuAction())

        self.basic_math_menu = QMenu("Math", self)
        self.basic_math_menu.addAction("Add", lambda: self.create_node("Add"))
        self.basic_math_menu.addAction("Subtract", lambda: self.create_node("Subtract"))
        self.basic_math_menu.addAction("Multiply", lambda: self.create_node("Multiply"))
        self.basic_math_menu.addAction("Divide", lambda: self.create_node("Divide"))
        self.basic_math_action = self.toolbar.addAction(self.basic_math_menu.menuAction())

        self.text_math_menu = QMenu("Text", self)
        self.text_math_menu.addAction("Add Text", lambda: self.create_node("Add Text"))
        self.text_math_menu.addAction("Subtract Text", lambda: self.create_node("Subtract Text"))
        self.text_math_menu.addAction("Multiply Text", lambda: self.create_node("Multiply Text"))
        self.text_math_menu.addAction("Cut Words", lambda: self.create_node("Cut Words"))
        self.text_math_menu.addAction("Cut Characters", lambda: self.create_node("Cut Characters"))
        self.text_math_action = self.toolbar.addAction(self.text_math_menu.menuAction())

        self.novelai_menu = QMenu("NovelAI", self)
        self.novelai_menu.addAction("Generate Image Basic", lambda: self.create_node("Gen Image"))
        self.novelai_menu.addAction("Generate Image Cluster Basic", lambda: self.create_node("Gen Cluster"))
        self.novelai_menu.addAction("Generate Image Cluster Advanced", lambda: self.create_node("Gen Cluster Adv"))
        self.novelai_menu.addAction("Prompt Builder", lambda: self.create_node("Prompt Builder"))
        self.novelai_menu.addAction("Random Seed", lambda: self.create_node("Random Seed"))
        self.novelai_menu.addAction("ControlNet", lambda: self.create_node("ControlNet"))
        self.novelai_action = self.toolbar.addAction(self.novelai_menu.menuAction())

        self.dd_menu = QMenu("DeepDanbooru", self)
        self.dd_menu.addAction("DeepDanbooru", lambda: self.create_node("DeepDanbooru"))
        self.dd_action = self.toolbar.addAction(self.dd_menu.menuAction())
        
        self.debug_menu = QMenu("Debug/Testing", self)
        self.debug_menu.addAction("Placeholder", lambda: self.create_node("Placeholder"))
        self.debug_action = self.toolbar.addAction(self.debug_menu.menuAction())

        # Add the "Execute Script" action to the toolbar
        self.execute_script_action = QAction("Execute Script", self, triggered=self.runScript)
        self.toolbar.addAction(self.execute_script_action)
        
        self.nodes = []

        # keyboard stuff
        self.view.installEventFilter(self)
        self.view.viewport().installEventFilter(self)

        # Add zoom slider
        self.zoom_slider = QSlider(Qt.Horizontal, self)
        self.zoom_slider.setRange(1, 500)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.valueChanged.connect(self.zoom_view)
        self.statusBar().addWidget(self.zoom_slider)

        # Custom console
        self.console_stream = ConsoleStream(self.progress_popup.console_log)
        sys.stdout = self.console_stream
        
        # Thread
        self.thread = QThread()

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
        elif node_type == "Input Number":
            node = InputNode(title="Input Number", input_type=float, export_type="int")
        elif node_type == "Input Text":
            node = InputNode(title="Input Text", input_type=str, export_type="string")
        elif node_type == "Output":
            node = OutputNode()
        elif node_type == "Image Output":
            node = ImageOutputNode()
        elif node_type == "Gen Image":
            node = ImageGeneratorNode()
        elif node_type == "Prompt Builder":
            node = PromptBuilderNode()
        elif node_type == "Random Seed":
            node = RandomSeedNode()
        elif node_type == "DeepDanbooru":
            node = DeepDanbooruNode()
        elif node_type == "Open Image":
            node = ImageOpenNode()
        elif node_type == "Save Image":
            node = ImageSaveNode()
        elif node_type == "Add Text":
            node = TextAddNode()
        elif node_type == "Subtract Text":
            node = TextSubtractNode()
        elif node_type == "Multiply Text":
            node = TextMultiplyNode()
        elif node_type == "Cut Words":
            node = TextCutWordsNode()
        elif node_type == "Cut Characters":
            node = TextCutCharactersNode()
        elif node_type == "Gen Grid":
            dialog = GridSizeDialog()
            if dialog.exec_() == QDialog.Accepted:
                grid_size = dialog.get_grid_size()
                title = f"Image Grid ({grid_size[0]}x{grid_size[1]})"
                node = ImageGridNode(title=title, grid_size=grid_size)
            else:
                node = None
        elif node_type == "Gen Cluster":
            dialog = GridSizeDialog()
            if dialog.exec_() == QDialog.Accepted:
                grid_size = dialog.get_grid_size()
                title = f"Cluster Generator ({grid_size[0]}x{grid_size[1]})"
                node = ClusterGeneratorNode(title=title, cluster_size=grid_size)
            else:
                node = None
        elif node_type == "Gen Cluster Adv":
            dialog = GridSizeDialog()
            if dialog.exec_() == QDialog.Accepted:
                grid_size = dialog.get_grid_size()
                title = f"Advanced Cluster Generator ({grid_size[0]}x{grid_size[1]})"
                node = AdvancedClusterGeneratorNode(title=title, cluster_size=grid_size)
            else:
                node = None
        elif node_type == "Resize":
            node = ImageResizeNode()
        elif node_type == "Zip":
            dialog = ZipSizeDialog()
            if dialog.exec_() == QDialog.Accepted:
                zip_size = dialog.get_zip_size()
                title = f"Zip Images ({zip_size})"
                port_formats = ["image"] * zip_size + ["zip"]
                node = ZipImagesNode(title=title, num_input_ports=zip_size, port_formats=port_formats)
            else:
                node = None
        elif node_type == "ControlNet":
            node = ControlNetNode()
        elif node_type == "Placeholder":
            node = PlaceholderNode()
        else:
            return

        self.scene.addItem(node)
        self.nodes.append(node)
        self.savinator.objects_to_save.append(node)

    def delete_selected_nodes(self):
        # Get a list of selected items
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return

        # Remove each selected item from the scene and from the list of nodes
        for item in selected_items:
            if item in self.nodes:
                for port in item.input_ports + item.output_ports:
                    port.disconnectAll()
                    port.parent.scene().removeItem(port)
                self.nodes.remove(item)
                item.scene().removeItem(item)


    def prompt_load(self):
        # Create a file dialog to let the user select a node chart file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Node chart files (*.novelui)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            # Load the selected file using Savinator.load()
            if os.path.isfile(file_path):
                self.savinator.load(file_path)


    def eventFilter(self, obj, event):
        if obj == self.view:
            if event.type() == QEvent.KeyPress:
                # Check for keybinds
                if event.key() == Qt.Key_Delete:
                    self.delete_selected_nodes()
                elif event.key() == Qt.Key_Up:
                    self.view.verticalScrollBar().setValue(self.view.verticalScrollBar().value() - 20)
                elif event.key() == Qt.Key_Down:
                    self.view.verticalScrollBar().setValue(self.view.verticalScrollBar().value() + 20)
                elif event.key() == Qt.Key_Left:
                    self.view.horizontalScrollBar().setValue(self.view.horizontalScrollBar().value() - 20)
                elif event.key() == Qt.Key_Right:
                    self.view.horizontalScrollBar().setValue(self.view.horizontalScrollBar().value() + 20)
                # Add more custom key press event handling here if needed
            elif event.type() == QEvent.KeyRelease:
                # Movement controls
                if event.key() in (Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
                    event.accept()
            # Drag
            if event.type() == QEvent.KeyPress and event.key() == Qt.Key_M:
                self.view.setDragMode(QGraphicsView.ScrollHandDrag) # Set drag mode to ScrollHandDrag
                event.accept()
            elif event.type() == QEvent.KeyRelease and event.key() == Qt.Key_M:
                self.view.setDragMode(QGraphicsView.RubberBandDrag) # Set drag mode back to RubberBandDrag
                event.accept()

            # TODO: Isn't working for some reason...
            # elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
            #     self.view.setDragMode(QGraphicsView.ScrollHandDrag) # Set drag mode to ScrollHandDrag
            #     event.accept()
            # elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.MiddleButton:
            #     self.view.setDragMode(QGraphicsView.RubberBandDrag) # Set drag mode back to RubberBandDrag
            #     event.accept()

        # Zoom zoom zoom
        if obj is self.view.viewport() and event.type() == QEvent.Wheel:
            # Get the zoom value from the event
            zoom_delta = event.angleDelta().y() / 120
            zoom_factor = 1.0 + zoom_delta / 10
            zoom_value = int(self.zoom_slider.value() * zoom_factor)

            # Limit the zoom value within the slider range
            zoom_value = max(self.zoom_slider.minimum(), min(zoom_value, self.zoom_slider.maximum()))

            # Set the updated zoom value to the slider
            self.zoom_slider.setValue(zoom_value)
    
            event.accept()

        return super().eventFilter(obj, event)
    
    def runScript(self):
        # Disable start button to prevent multiple clicks
        self.execute_script_action.setEnabled(False)

        # Show progress dialog
        self.progress_popup.show()

        # Start worker thread
        self.thread.start()

        # Create a worker thread for the computeOutput() function
        self.worker = Worker(self._runScript)

        # Connect signals
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.progress.connect(self.progress_popup.update_progress)
        self.worker.error.connect(self.handle_error)
        self.worker.progress.connect(self.progress_popup.update_progress)

        # Start worker thread
        self.worker.start()

    def on_worker_finished(self):
        self.execute_script_action.setEnabled(True)

    def handle_error(self, error_message):
        print(f"Error occurred: {error_message}")
        self.execute_script_action.setEnabled(True)

    def _runScript(self):
        # Find the output node
        output_nodes = [node for node in self.scene.items() if isinstance(node, Node) and node.num_output_ports == 0]
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

        # Progress updater
        progress_percent = len(processed_nodes) / len(self.nodes) * 100
        self.worker.progress.emit(progress_percent)

    def traverseNode(self, node, node_values, processed_nodes):
        # Progress updater
        progress_percent = len(processed_nodes) / len(self.nodes) * 100
        self.worker.progress.emit(progress_percent)

        if node in processed_nodes:
            return
    
        # Traverse input ports and compute values of connected nodes
        for port in node.input_ports:
            if not port.connections:
                continue
            
            connected_port = port.connections[0].output_port
            connected_node = connected_port.parent
    
            self.traverseNode(connected_node, node_values, processed_nodes)
    
            # Set the value of each output port of the connected node
            for out_port in connected_node.output_ports:
                if out_port in connected_port.connections:
                    out_port.value = port.value
    
        # Compute and store output values of current node for each output port
        output_values = node.computeOutput()
        for i, out_port in enumerate(node.output_ports):
            out_port.value = output_values[i]
        
        print("Node " + node.title + " processed.")
    
        processed_nodes.add(node)

class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(float)
    error = pyqtSignal(str)

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            self.function(*self.args, **self.kwargs)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class GridSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Grid Size")
        
        self.width_edit = QLineEdit()
        self.height_edit = QLineEdit()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Width:"))
        layout.addWidget(self.width_edit)
        layout.addWidget(QLabel("Height:"))
        layout.addWidget(self.height_edit)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def get_grid_size(self):
        return (int(self.width_edit.text()), int(self.height_edit.text()))
    
class ZipSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zip Files")
        
        self.width_edit = QLineEdit()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.width_edit)
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def get_zip_size(self):
        return int(self.width_edit.text())



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
