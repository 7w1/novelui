from PyQt5.QtWidgets import QFileDialog, QGraphicsProxyWidget, QPushButton
from nodes.node import Node
from PyQt5.QtGui import QColor
from PIL import Image
import io

class ImageOpenNode(Node):
    def __init__(self, title="Open Image", color="#702963"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=0, num_output_ports=1, port_formats=["image"])
        
        # Create a button widget
        self.button = QPushButton("Open Image")
        self.button.clicked.connect(self.openImage)

        # Set up the graphics proxy widget
        self.proxy = QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.button)
        self.proxy.setPos(-38, 0)

        self.image_data = None

    def openImage(self):
        # Ask the user to select an image file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.parentWidget(), "Open Image", "", "Image Files (*.png)", options=options)

        if file_name:
            # Read the image data from the selected file using PIL
            image = Image.open(file_name)

            output_buffer = io.BytesIO()
            try:
                image.save(output_buffer, format='PNG')
            except Exception as e:
                print("Error saving resized image:", e)
                return None

            self.image_data = output_buffer.getvalue()


    def computeOutput(self):
        # Return the raw PNG image data
        return [self.image_data]
