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

class AdvancedClusterGeneratorNode(Node):
    def __init__(self, title="Image Generator", color="#330066", cluster_size=(3,3)):
        super().__init__(title, QColor(color).darker(150), num_input_ports=3, num_output_ports=2, port_formats=["string", "string", "string", "image", "zip"])
        self.input_ports[0].label = "base prompt"
        self.input_ports[1].label = "row prompt"
        self.input_ports[2].label = "column prompt"
        self.output_ports[0].label = "image"
        self.output_ports[1].label = "zip"
        self.grid_size = cluster_size
        self.setSize(240, self.height)

    def computeOutput(self):
        # Get input values from input ports
        base_prompt = self.input_ports[0].connections[0].output_port.value
        row_prompt = self.input_ports[1].connections[0].output_port.value
        col_prompt = self.input_ports[2].connections[0].output_port.value

        # Calculate differences between the prompts
        row_differences = {}
        col_differences = {}
        row_diff_to_draw = {}
        col_diff_to_draw = {}
        for key in base_prompt:
            if isinstance(base_prompt[key], int):
                row_differences[key] = round(row_prompt[key]) - round(base_prompt[key])
                if row_differences[key] != 0:
                    row_diff_to_draw[key] = row_differences[key]

                col_differences[key] = round(col_prompt[key]) - round(base_prompt[key])
                if col_differences[key] != 0:
                    col_diff_to_draw[key] = col_differences[key]

            elif isinstance(base_prompt[key], float):
                row_differences[key] = row_prompt[key] - base_prompt[key]
                if row_differences[key] != 0:
                    row_diff_to_draw[key] = row_differences[key]

                col_differences[key] = col_prompt[key] - base_prompt[key]
                if col_differences[key] != 0:
                    col_diff_to_draw[key] = col_differences[key]

        # Generate images
        image_files = []
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                # Check if image already exists
                image_file = f"output/cluster/temp/{row}x{col}.png"
                if os.path.isfile(image_file):
                    print(f"Image {image_file} already exists. Skipping generation...")
                    image_files.append(image_file)
                    continue

                modified_prompt = {}
                for key in base_prompt:
                    if isinstance(base_prompt[key], int):
                        modified_prompt[key] = round(base_prompt[key] + (col / (self.grid_size[1] - 1)) * col_differences[key] + (row / (self.grid_size[0] - 1)) * row_differences[key])
                    elif isinstance(base_prompt[key], float):
                        modified_prompt[key] = base_prompt[key] + (col / (self.grid_size[1] - 1)) * col_differences[key] + (row / (self.grid_size[0] - 1)) * row_differences[key]
                    else:
                        modified_prompt[key] = base_prompt[key]

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

                # Draw text
                for key in row_diff_to_draw:
                    modified_key = key.replace('_', ' ').title()
                    value = modified_prompt[key]
                    if isinstance(value, bool):
                        value = str(value)
                    elif isinstance(value, float):
                        value = "{:.2f}".format(value)
                    text += modified_key + ": " + str(value) + "\n"

                # Draw text
                for key in col_diff_to_draw:
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
                image_file = f"output/cluster/temp/{row}x{col}.png"
                with open(image_file, 'wb') as f:
                    image.save(f, 'PNG')
                image_files.append(image_file)

                # Wait a bit so we don't overload the api since we're nice :P
                if endtime - starttime > 500:
                    pausetime = 10
                else:
                    pausetime = endtime - starttime
                print(f"Pausing for {pausetime} seconds.")
                time.sleep(pausetime)
        
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

        # Header
        output_image = self.add_top_area(base_prompt, row_prompt, col_prompt, output_image)
        
        # Zip for second output
        folder_path = "output/cluster/temp"
        output_buffer = BytesIO()
        zip_file = zipfile.ZipFile(output_buffer, mode="w")
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                zip_file.write(file_path, file_name)

        zip_file.close()
        compressed_data = output_buffer.getvalue()
        
        # Delete temp files
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return [output_image, compressed_data]
    

    def add_top_area(self, base_prompt, row_prompt, col_prompt, output_image):
        # Define top area dimensions
        font = ImageFont.truetype('arial.ttf', 8)
        padding = 5
        heading_font = ImageFont.truetype('arial.ttf', 20)
        subheading_font = ImageFont.truetype('arial.ttf', 12)

        heading_text = "NovelUI for NovelAI"
        subheading_text = "Made by 7w1"

        if 'action' not in base_prompt or base_prompt['action'] == 'generate':
            subheading_text += "\nImage Generation"
        elif base_prompt['action'] and base_prompt['action'] == 'img2img':
            subheading_text += "\nImage to Image"
            base_prompt['image'] = '[image data]'
            row_prompt['image'] = '[image data]'
            col_prompt['image'] = '[image data]'

        if 'controlnet_model' in base_prompt and base_prompt['controlnet_model'] is not None:
            subheading_text += "\nControlNet Model: " + base_prompt['controlnet_model']
            base_prompt['controlnet_condition'] = '[image data]'
            row_prompt['controlnet_condition'] = '[image data]'
            col_prompt['controlnet_condition'] = '[image data]'

        heading_color = (138, 43, 226) # purple
        subheading_color = (128, 128, 128) # gray
        text_color = (189, 195, 199)

        heading_width, heading_height = heading_font.getsize(heading_text)

        # split the subheading text into lines and calculate the width of each line
        subheading_lines = subheading_text.splitlines()
        subheading_widths = [subheading_font.getsize(line)[0] for line in subheading_lines]

        # find the maximum width of all the lines and use that as the subheading width
        subheading_width = max(subheading_widths)
        subheading_height = subheading_font.getsize(subheading_text)[1]

        # Calculate prompt1, prompt2 and prompt3 text dimensions
        base_prompt_text = ""
        for key, value in base_prompt.items():
            base_prompt_text += f"{key}: {value}\n"
        base_prompt_text_width, base_prompt_text_height = font.getsize(base_prompt_text)

        row_prompt_text = ""
        for key, value in row_prompt.items():
            row_prompt_text += f"{key}: {value}\n"
        row_prompt_text_width, row_prompt_text_height = font.getsize(row_prompt_text)

        col_prompt_text = ""
        for key, value in col_prompt.items():
            col_prompt_text += f"{key}: {value}\n"
        col_prompt_text_width, col_prompt_text_height = font.getsize(col_prompt_text)

        # Calculate top area height and width
        max_text_width = max(base_prompt_text_width, col_prompt_text_width)
        top_area_height = max(heading_height + subheading_height + padding*2, base_prompt_text_height*base_prompt_text.count("\n"), col_prompt_text_height*col_prompt_text.count("\n")) + padding*4

        # Create top area image
        top_area_image = Image.new('RGBA', (output_image.width, top_area_height), (29, 29, 32, 255))
        draw = ImageDraw.Draw(top_area_image)

        # Draw headings
        draw.text(((output_image.width-heading_width)//2, padding), heading_text, font=heading_font, fill=heading_color, align="center")
        draw.text(((output_image.width-subheading_width)//2, heading_height+padding*2), subheading_text, font=subheading_font, fill=subheading_color, align="center")

        # Create row prompt image
        row_prompt_image = Image.new('RGBA', (output_image.height+top_area_image.height, top_area_height), (29, 29, 32, 255))
        row_draw = ImageDraw.Draw(row_prompt_image)
        row_draw.text((padding, padding), row_prompt_text, font=font, fill=text_color)

        # Rotate row prompt image by 90 degrees
        row_prompt_image = row_prompt_image.transpose(Image.ROTATE_90)

        # Combine images
        # create a new RGBA image with the desired dimensions and transparent background
        combined_image = Image.new('RGBA', (output_image.width + row_prompt_image.width, output_image.height + top_area_height), (255, 255, 255, 0))

        # paste the images onto the combined image at the desired positions
        combined_image.paste(top_area_image, (0, 0))
        combined_image.paste(row_prompt_image, (0, top_area_height))
        combined_image.paste(output_image, (row_prompt_image.width, top_area_height))
        # paste the images onto the combined image at the desired positions
        combined_image.paste(row_prompt_image, (0, 0))
        combined_image.paste(top_area_image, (row_prompt_image.width, 0))
        combined_image.paste(output_image, (row_prompt_image.width, top_area_height))

        draw = ImageDraw.Draw(combined_image)

        # Draw prompt base text
        draw.text((padding, padding), base_prompt_text, font=font, fill=text_color)

        # Draw prompt col text
        draw.text((combined_image.width-padding-col_prompt_text_width, padding), col_prompt_text, font=font, fill=text_color, align="right")

        # Output combined image as PNG
        output = BytesIO()
        combined_image.save(output, format='PNG')

        return output.getvalue()
