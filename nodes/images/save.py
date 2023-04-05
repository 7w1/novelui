import os
import datetime
from PyQt5.QtWidgets import QFileDialog, QPushButton, QGraphicsProxyWidget
from nodes.node import Node
from PyQt5.QtGui import QColor

class ImageSaveNode(Node):
    def __init__(self, title="Save Image", color="gray"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=0)

        # Create a button widget
        self.button = QPushButton("Select Location")
        self.button.clicked.connect(self.selectLocation)

        # Set up the graphics proxy widget
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.button)
        self.proxy.setPos(-40, 0)

        self.file_path = None

    def selectLocation(self):
        # Get the current date and time
        now = datetime.datetime.now()
            
        # Create the output folder if it doesn't exist
        output_folder = os.path.join(os.getcwd(), "output", now.strftime("%Y-%m-%d"))
        os.makedirs(output_folder, exist_ok=True)
        
        # Create the file path
        file_path = os.path.join(output_folder, now.strftime("%H-%M-%S") + ".png")
        
        # Ask the user to select a file to save the image
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self.widget, "Save Image", file_path, "PNG Images (*.png)", options=options)
        
        if file_name:
            self.file_path = file_name

    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value
        if input_value is not None:
            if self.file_path is None:
                # Get the current date and time
                now = datetime.datetime.now()

                # Create the output folder if it doesn't exist
                output_folder = os.path.join(os.getcwd(), "output", now.strftime("%Y-%m-%d"))
                os.makedirs(output_folder, exist_ok=True)

                # Create the file path
                self.file_path = os.path.join(output_folder, now.strftime("%H-%M-%S") + ".png")
                print(self.file_path)

            # Save the image to the selected file
            print("saved")
            with open(self.file_path, 'wb+') as f:
                f.write(input_value)

        return None
