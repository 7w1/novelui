from PIL import Image, ImageDraw, ImageFont
from nodes.node import Node
from PyQt5.QtGui import QColor
from api.generate_image import generate
from PIL import Image
from io import BytesIO
import colorsys
import time
import os

class ClusterGeneratorNode(Node):
    def __init__(self, title="Image Generator", color="#330066", cluster_size=(3,3)):
        super().__init__(title, QColor(color).darker(150), num_input_ports=2, num_output_ports=1, port_formats=["string", "string", "image"])
        self.input_ports[0].label = "prompt 1"
        self.input_ports[1].label = "prompt 2"
        self.grid_size = cluster_size
        self.setSize(180, 280)

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

        return output_image


    

    def add_top_area(self, prompt1, prompt2, output_image):
        # Define top area dimensions
        top_area_height = 100
        top_area_width = output_image.width

        # Create top area image
        top_area_image = Image.new('RGBA', (top_area_width, top_area_height), (29, 29, 32, 255))

        # Define font and text color
        font = ImageFont.truetype('arial.ttf', 8)
        text_color = (189, 195, 199)

        # Define default values
        defaults = {
            "input": "masterpiece",
            "action": "generate",
            "model": "nai-diffusion",
            "width": 512,
            "height": 768,
            "scale": 11,
            "sampler": "k_dpmpp_2m",
            "steps": 28,
            "smea": False,
            "smea_dyn": False,
            "dynamic_thresholding": False,
            "controlnet_strength": 1,
            "legacy": False,
            "seed": None,
            "negative_prompt": "lowres",
            "dynamic_thresholding_percentile": 0.999,
            "dynamic_threshold_mimic": 10.0
        }

        # Fill missing values with defaults
        prompt1 = {**defaults, **prompt1}
        prompt2 = {**defaults, **prompt2}

        # Define max text width
        max_text_width = (top_area_width - 40) // 2

        # Add prompt 1 text
        prompt1_text = "Input: {}, Action: {}, Model: {}, Width: {}, Height: {}, Scale: {}, Sampler: {}, Steps: {}, Smea: {}, Smea_dyn: {}, Dynamic_thresholding: {}, Controlnet_strength: {}, Legacy: {}, Seed: {}, Negative_prompt: {}, Dynamic_thresholding_percentile: {}, Dynamic_threshold_mimic: {}".format(
            prompt1["input"], prompt1["action"], prompt1["model"], prompt1["width"], prompt1["height"], prompt1["scale"], prompt1["sampler"], prompt1["steps"], prompt1["smea"], prompt1["smea_dyn"], prompt1["dynamic_thresholding"], prompt1["controlnet_strength"], prompt1["legacy"], prompt1["seed"], prompt1["negative_prompt"], prompt1["dynamic_thresholding_percentile"], prompt1["dynamic_threshold_mimic"])
        prompt1_lines = self.wrap_text(prompt1_text, font, max_text_width)
        prompt1_y = 20
        for line in prompt1_lines:
            line_width, line_height = font.getsize(line)
            prompt1_x = 20
            prompt1_draw = ImageDraw.Draw(top_area_image)
            prompt1_draw.text((prompt1_x, prompt1_y), line, font=font, fill=text_color)
            prompt1_y += line_height + 5

        # Add prompt 2 text
        prompt2_text = "Input: {}, Action: {}, Model: {}, Width: {}, Height: {}, Scale: {}, Sampler: {}, Steps: {}, Smea: {}, Smea_dyn: {}, Dynamic_thresholding: {}, Controlnet_strength: {}, Legacy: {}, Seed: {}, Negative_prompt: {}, Dynamic_thresholding_percentile: {}, Dynamic_threshold_mimic: {}".format(
            prompt2["input"], prompt2["action"], prompt2["model"], prompt2["width"], prompt2["height"], prompt2["scale"], prompt2["sampler"], prompt2["steps"], prompt2["smea"], prompt2["smea_dyn"], prompt2["dynamic_thresholding"], prompt2["controlnet_strength"], prompt2["legacy"], prompt2["seed"], prompt2["negative_prompt"], prompt2["dynamic_thresholding_percentile"], prompt2["dynamic_threshold_mimic"])
        prompt2_lines = self.wrap_text(prompt2_text, font, max_text_width)
        prompt2_y = 20
        for line in prompt2_lines:
            line_width, line_height = font.getsize(line)
            prompt2_x = top_area_width - line_width - 20
            prompt2_draw = ImageDraw.Draw(top_area_image)
            prompt2_draw.text((prompt2_x, prompt2_y), line, font=font, fill=text_color)
            prompt2_y += line_height + 5

        # Combine images
        combined_image = Image.new('RGBA', (output_image.width, output_image.height + top_area_height), (255, 255, 255, 0))
        combined_image.paste(top_area_image, (0, 0))
        combined_image.paste(output_image, (0, top_area_height))

        # Output combined image as PNG
        output = BytesIO()
        combined_image.save(output, format='PNG')

        return output.getvalue()

    def wrap_text(self, text, font, max_width):
        # Wrap text to fit within max_width
        lines = []
        words = text.split()
        current_line = words[0]
        for word in words[1:]:
            if font.getsize(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

