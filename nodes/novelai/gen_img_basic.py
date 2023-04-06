# from nodes.node import Node
# from PyQt5.QtGui import QColor
# from api.generate_image import generate
# 
# class PromptBuilderNode(Node):
#     def __init__(self, title="Prompt Builder", color="orange"):
#         super().__init__(title, QColor(color).darker(150), num_input_ports=16, num_output_ports=1)
#         
#         # Set labels for input ports
#         self.input_ports[0].label = "input"
#         self.input_ports[1].label = "action"
#         self.input_ports[2].label = "model"
#         self.input_ports[3].label = "width"
#         self.input_ports[4].label = "height"
#         self.input_ports[5].label = "scale"
#         self.input_ports[6].label = "sampler"
#         self.input_ports[7].label = "steps"
#         self.input_ports[8].label = "images"
#         self.input_ports[9].label = "smea"
#         self.input_ports[10].label = "smea_dyn"
#         self.input_ports[11].label = "dynamic_thresholding"
#         self.input_ports[12].label = "controlnet_strength"
#         self.input_ports[13].label = "legacy"
#         self.input_ports[14].label = "seed"
#         self.input_ports[15].label = "negative_prompt"
#         
#         # Set default values for input variables
#         self.input_ports[1].value = "generate"
#         self.input_ports[2].value = "nai-diffusion"
#         self.input_ports[3].value = 512
#         self.input_ports[4].value = 768
#         self.input_ports[5].value = 11
#         self.input_ports[6].value = "k_dpmpp_2m"
#         self.input_ports[7].value = 28
#         self.input_ports[8].value = 1
# 
#         self.setSize(200, 450)
# 
#     def computeOutput(self):
#         # Get input values from input ports
#         input_values = [port.connections[0].output_port.value if port.connections else None for port in self.input_ports]
# 
#         # Return input values as a dictionary
#         return {
#             'input': input_values[0],
#             'action': input_values[1],
#             'model': input_values[2],
#             'width': input_values[3],
#             'height': input_values[4],
#             'scale': input_values[5],
#             'sampler': input_values[6],
#             'steps': input_values[7],
#             'images': input_values[8],
#             'smea': input_values[9],
#             'smea_dyn': input_values[10],
#             'dynamic_thresholding': input_values[11],
#             'controlnet_strength': input_values[12],
#             'legacy': input_values[13],
#             'seed': input_values[14],
#             'negative_prompt': input_values[15]
#         }
# 
# 
# class GenerateImageNode(Node):
#     def __init__(self, title="Generate Image", color="orange"):
#         super().__init__(title, QColor(color).darker(150), num_input_ports=1, num_output_ports=1)
# 
#         self.setSize(self.width + 10, self.height)
# 
#     def computeOutput(self):
#         # Get input values from PromptBuilderNode
#         input_values = self.input_ports[0].connections[0].output_port.value
# 
#         # Call generate method with input variables
#         return generate(**input_values)

from nodes.node import Node
from PyQt5.QtGui import QColor
from api.generate_image import generate

class GenerateImageBasicNode(Node):
    def __init__(self, title="Generate Image - Basic", color="orange"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=16, num_output_ports=1, port_formats=["string", "string", "string", "int", "int", "int", "string", "int", "image", "int", "int", "int", "int", "int", "int", "string", "image"])
        
        # Set labels for input ports
        self.input_ports[0].label = "input"
        self.input_ports[1].label = "action"
        self.input_ports[2].label = "model"
        self.input_ports[3].label = "width"
        self.input_ports[4].label = "height"
        self.input_ports[5].label = "scale"
        self.input_ports[6].label = "sampler"
        self.input_ports[7].label = "steps"
        self.input_ports[8].label = "images"
        self.input_ports[9].label = "smea"
        self.input_ports[10].label = "smea_dyn"
        self.input_ports[11].label = "dynamic_thresholding"
        self.input_ports[12].label = "controlnet_strength"
        self.input_ports[13].label = "legacy"
        self.input_ports[14].label = "seed"
        self.input_ports[15].label = "negative_prompt"
        
        # Set default values for input variables
        self.input_ports[1].value = "generate"
        self.input_ports[2].value = "nai-diffusion"
        self.input_ports[3].value = 512
        self.input_ports[4].value = 768
        self.input_ports[5].value = 11
        self.input_ports[6].value = "k_dpmpp_2m"
        self.input_ports[7].value = 28
        self.input_ports[8].value = 1

        self.setSize(200, 450)

    def computeOutput(self):
        # Get input values from input ports
        input_values = [port.connections[0].output_port.value if port.connections else None for port in self.input_ports]


        # Check if all input ports are connected
        # if None in input_values:
        #     QMessageBox.warning(None, "Error", "Please connect all input ports.")
        #     return None

        # Call generate method with input variables
        input, action, model, width, height, scale, sampler, steps, images, smea, smea_dyn, dynamic_thresholding, controlnet_strength, legacy, seed, negative_prompt = input_values

        kwargs = {}
        if input is not None:
            kwargs['input'] = input # 1
        if action is not None:
            kwargs['action'] = action # 2
        if model is not None:
            kwargs['model'] = model # 3
        if width is not None: 
            kwargs['width'] = width # 4
        if height is not None:
            kwargs['height'] = height # 5
        if scale is not None:
            kwargs['scale'] = scale # 6
        if sampler is not None:
            kwargs['sampler'] = sampler # 7
        if steps is not None:
            kwargs['steps'] = steps # 8
        if images is not None:
            kwargs['images'] = images # 9
        if smea is not None:
            kwargs['smea'] = smea # 10
        if smea_dyn is not None:
            kwargs['smea_dyn'] = smea_dyn # 11
        if dynamic_thresholding is not None:
            kwargs['dynamic_thresholding'] = dynamic_thresholding # 12
        if controlnet_strength is not None:
            kwargs['controlnet_strength'] = controlnet_strength # 13
        if legacy is not None:
            kwargs['legacy'] = legacy # 14
        if seed is not None:
            kwargs['seed'] = seed # 15
        if negative_prompt is not None:
            kwargs['negative_prompt'] = negative_prompt # 16

        return generate(**kwargs)
