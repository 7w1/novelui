from zipfile import ZipFile
from io import BytesIO
from PIL import Image
from PyQt5.QtGui import QColor
from nodes.node import Node

# TODO: Fix this

class ImageGridNode(Node):
    def __init__(self, title="Image Grid 2x2", color="#4B0082", grid_size=(2, 2)):
        super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=1, port_formats=["zip", "image"])

        self.input_ports[0].label = "images"
        self.output_ports[0].label = "image"

        self.grid_size = grid_size
        self.output_image = None

    def computeOutput(self):
        input_value = self.input_ports[0].connections[0].output_port.value
        if input_value is None:
            return None

        # Extract images from zip file
        with ZipFile(BytesIO(input_value), 'r') as zip_file:
            image_files = sorted([f for f in zip_file.namelist() if f.lower().endswith('.png')])
            if not image_files:
                return None

            # Compute grid dimensions
            num_images = len(image_files)
            num_rows = min(self.grid_size[0], num_images)
            num_cols = min(self.grid_size[1], (num_images + num_rows - 1) // num_rows)

            # Compute grid cell size
            grid_width, grid_height = 0, 0
            for i, image_file in enumerate(image_files):
                with zip_file.open(image_file) as f:
                    image = Image.open(f)
                    if i % num_cols == 0:
                        cell_width = 0
                        cell_height = 0
                    cell_width = max(cell_width, image.width)
                    cell_height = max(cell_height, image.height)
                    if (i + 1) % num_cols == 0 or i == num_images - 1:
                        grid_width += cell_width
                        grid_height += cell_height

            # Create output image
            output_image = Image.new('RGBA', (grid_width, grid_height), (255, 255, 255, 0))
            x, y = 0, 0
            for i, image_file in enumerate(image_files):
                with zip_file.open(image_file) as f:
                    image = Image.open(f).convert('RGBA')
                    cell_width = image.width
                    cell_height = image.height
                    if i % num_cols == 0:
                        x = 0
                        y += cell_height
                    output_image.paste(image, (x, y))
                    x += cell_width

        # Convert output image to bytes
        with BytesIO() as output:
            output_image.save(output, format='PNG')
            self.output_image = output.getvalue()

        return self.output_image
