from PIL import Image, ImageDraw, ImageFont
from nodes.node import Node
from PyQt5.QtGui import QColor
from api.generate_image import generate
from PIL import Image
from io import BytesIO
import colorsys
import time
import os
import zipfile

class ClusterGeneratorNode(Node):
    def __init__(self, title="Image Generator", color="#330066", cluster_size=(3,3)):
        super().__init__(title, QColor(color).darker(150), num_input_ports=4, num_output_ports=2, port_formats=["string", "string", "int", "int", "image", "zip"])
        self.input_ports[0].label = "prompt 1"
        self.input_ports[1].label = "prompt 2"
        self.input_ports[2].label = "header toggle"
        self.input_ports[3].label = "increment details toggle"
        self.output_ports[0].label = "image"
        self.output_ports[1].label = "zip"
        self.grid_size = cluster_size
        self.setSize(150, self.height)

    def computeOutput(self):
        # Get input values from input ports
        prompt1 = self.input_ports[0].connections[0].output_port.value
        prompt2 = self.input_ports[1].connections[0].output_port.value


        # Calculate differences between the prompts
        differences = {}
        diff_to_draw = {}
        for key in prompt1:
            if isinstance(prompt1[key], int):
                differences[key] = round(prompt2[key]) - round(prompt1[key])
                if differences[key] != 0:
                    diff_to_draw[key] = differences[key]
            elif isinstance(prompt1[key], float):
                differences[key] = prompt2[key] - prompt1[key]
                if differences[key] != 0:
                    diff_to_draw[key] = differences[key]

        # Generate images
        image_files = []
        for i in range(self.grid_size[0] * self.grid_size[1]):
            modified_prompt = {}
            for key in prompt1:
                if isinstance(prompt1[key], int):
                    modified_prompt[key] = round(prompt1[key] + (i / ((self.grid_size[0] * self.grid_size[1]) - 1)) * differences[key])
                elif isinstance(prompt1[key], float):
                    modified_prompt[key] = prompt1[key] + (i / ((self.grid_size[0] * self.grid_size[1]) - 1)) * differences[key]
                else:
                    modified_prompt[key] = prompt1[key]

            # Generate image
            starttime = time.time()
            img_data = generate(**modified_prompt)
            endtime = time.time()
            image = Image.open(BytesIO(img_data))  # Create Image object from raw byte data

            # Add text to image
            font_size = 16
            font = ImageFont.truetype('arial.ttf', font_size)
            text = ""
            text_color = 'white'  # Default text color
            bg_color = colorsys.rgb_to_hsv(*image.getpixel((image.width - 1, image.height - 1)))  # Get bottom right pixel color
            if bg_color[2] < 0.5:  # If the background is dark, use white text
                text_color = 'white'
            else:  # If the background is light, use black text
                text_color = 'black'
            draw = ImageDraw.Draw(image)

            for key in diff_to_draw:
                modified_key = key.replace('_', ' ').title()
                value = modified_prompt[key]
                if isinstance(value, bool):
                    value = str(value)
                elif isinstance(value, float):
                    value = "{:.2f}".format(value)
                text += modified_key + ": " + str(value) + "\n"

            text_width, text_height = draw.textsize(text, font=font)
            x = image.width - text_width - 10  # Padding
            y = image.height - text_height - 10  # Padding
            draw.text((x, y), text, font=font, fill=text_color)

            # Save images
            if not os.path.exists('output/cluster/temp'):
                os.makedirs('output/cluster/temp')
            image_file = f"output/cluster/temp/{i}.png"
            with open(image_file, 'wb') as f:
                image.save(f, 'PNG')
            image_files.append(image_file)

            # Wait a bit so we don't overload the api since we're nice :P
            time.sleep(endtime - starttime)

        # Create grid of images
        num_images = len(image_files)
        first_image = Image.open(image_files[0]).convert('RGBA')
        cell_width, cell_height = first_image.size
        num_rows = min(self.grid_size[0], num_images)
        num_cols = min(self.grid_size[1], (num_images + num_rows - 1) // num_rows)
        canvas_width = num_cols * cell_width  # Width of the canvas
        canvas_height = num_rows * cell_height  # Height of the canvas
        output_image = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
        for i, image_file in enumerate(image_files):
            image = Image.open(image_file).convert('RGBA')
            image = image.resize((cell_width, cell_height))
            row = i // num_cols
            col = i % num_cols
            x = col * cell_width
            y = row * cell_height
            output_image.paste(image, (x, y))

        output_image = self.add_top_area(prompt1, prompt2, output_image)

        # # Zip for second output, gives a zip of all images
        # zip_bytes = BytesIO()
        # with zipfile.ZipFile(zip_bytes, 'w', zipfile.ZIP_DEFLATED) as zip_obj:
        #     for filenames in os.walk("output/cluster/temp"):
        #         for filename in filenames:
        #             zip_obj.write(filename)
# 
        # # Delete all temp files
        # for filename in os.listdir("output/cluster/temp"):
        #     try:
        #         if os.path.isfile(filename):
        #             os.remove(filename)
        #     except Exception as e:
        #         print(f"Error deleting file: {filename} - {e}")

        return [output_image, None] # zip_bytes.getvalue()]

    def add_top_area(self, prompt1, prompt2, output_image):
        # Define top area dimensions
        font = ImageFont.truetype('arial.ttf', 8)
        padding = 5
        heading_font = ImageFont.truetype('arial.ttf', 20)
        subheading_font = ImageFont.truetype('arial.ttf', 12)

        heading_text = "NovelUI for NovelAI"
        subheading_text = "Made by 7w1"

        if 'action' not in prompt1 or prompt1['action'] == 'generate':
            subheading_text += "\nImage Generation"
        elif prompt1['action'] and prompt1['action'] == 'img2img':
            subheading_text += "\nImage to Image"

        if 'controlnet_model' in prompt1 and prompt1['controlnet_model'] is not None:
            subheading_text += "\nControlNet Model: " + prompt1['parameters']['controlnet_model']

        heading_color = (138, 43, 226) # purple
        subheading_color = (128, 128, 128) # gray
        text_color = (189, 195, 199)

        heading_width, heading_height = heading_font.getsize(heading_text)
        subheading_width, subheading_height = subheading_font.getsize(subheading_text)

        # Calculate prompt1 and prompt2 text dimensions
        prompt1_text = ""
        for key, value in prompt1.items():
            prompt1_text += f"{key}: {value}\n"
        prompt1_text_width, prompt1_text_height = font.getsize(prompt1_text)

        prompt2_text = ""
        for key, value in prompt2.items():
            prompt2_text += f"{key}: {value}\n"
        prompt2_text_width, prompt2_text_height = font.getsize(prompt2_text)

        # Calculate top area height
        max_text_width = max(prompt1_text_width, prompt2_text_width)
        top_area_height = heading_height + subheading_height + prompt1_text_height*prompt1_text.count("\n") + padding*4

        # Create top area image
        top_area_image = Image.new('RGBA', (output_image.width, top_area_height), (29, 29, 32, 255))
        draw = ImageDraw.Draw(top_area_image)

        # Draw headings# Draw headings
        draw.text(((output_image.width-heading_width)//2, padding), heading_text, font=heading_font, fill=heading_color, align="center")
        draw.text(((output_image.width-subheading_width)//2, heading_height+padding*2), subheading_text, font=subheading_font, fill=subheading_color, align="center")

        # Draw prompt1 text
        draw.text((padding, heading_height+subheading_height+padding*3), prompt1_text, font=font, fill=text_color)

        # Draw prompt2 text# Draw prompt2 text
        draw.text((output_image.width-prompt2_text_width-padding, heading_height+subheading_height+padding*3), prompt2_text, font=font, fill=text_color, align="right")


        # Combine images
        combined_image = Image.new('RGBA', (output_image.width, output_image.height + top_area_height), (255, 255, 255, 0))
        combined_image.paste(top_area_image, (0, 0))
        combined_image.paste(output_image, (0, top_area_height))

        # Output combined image as PNG
        output = BytesIO()
        combined_image.save(output, format='PNG')

        return output.getvalue()


