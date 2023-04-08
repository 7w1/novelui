from nodes.node import Node
from PyQt5.QtGui import QColor
import base64
import math

class PromptBuilderNode(Node):
    def __init__(self, title="Prompt Builder", color="#330066"):
        super().__init__(title, QColor(color).darker(150), num_input_ports=24, num_output_ports=1, port_formats=["string", "string", "string", "int", "int", "int", "string", "int", "int", "int", "int", "int", "int", "string", "image", "int", "image", "int", "int", "string", "int", "int", "int", "int", "string"])
        
        # Set labels for input ports
        self.input_ports[0].label = "input"
        self.input_ports[1].label = "action"
        self.input_ports[2].label = "model"
        self.input_ports[3].label = "width"
        self.input_ports[4].label = "height"
        self.input_ports[5].label = "scale"
        self.input_ports[6].label = "sampler"
        self.input_ports[7].label = "steps"
        self.input_ports[8].label = "n_samples"
        self.input_ports[9].label = "smea"
        self.input_ports[10].label = "smea_dyn"
        self.input_ports[11].label = "dynamic_thresholding"
        self.input_ports[12].label = "controlnet_strength"
        self.input_ports[13].label = "controlnet_model"
        self.input_ports[14].label = "controlnet_condition"
        self.input_ports[15].label = "legacy"
        self.input_ports[16].label = "image"
        self.input_ports[17].label = "seed"
        self.input_ports[18].label = "extra_noise_seed"
        self.input_ports[19].label = "negative_prompt"
        self.input_ports[20].label = "dynamic_thresholding_percentile"
        self.input_ports[21].label = "dynamic_threshold_mimic"
        self.input_ports[22].label = "noise"
        self.input_ports[23].label = "strength"
        
        self.output_ports[0].label = "prompt"

        self.setSize(180, 350)

    def computeOutput(self):
        # Get input values from input ports
        input_values = [port.connections[0].output_port.value if port.connections else None for port in self.input_ports]

        input, action, model, width, height, scale, sampler, steps, n_samples, smea, smea_dyn, dynamic_thresholding, controlnet_strength, controlnet_model, controlnet_condition, legacy, image, seed, extra_noise_seed, negative_prompt, dynamic_thresholding_percentile, dynamic_threshold_mimic, noise, strength = input_values

        kwargs = {}
        if input is not None:
            kwargs['input'] = input
        if action is not None:
            kwargs['action'] = action
        if model is not None:
            kwargs['model'] = model
        if width is not None: 
            kwargs['width'] = math.floor(width)
        if height is not None:
            kwargs['height'] = math.floor(height)
        if scale is not None:
            kwargs['scale'] = math.floor(scale)
        if sampler is not None:
            kwargs['sampler'] = sampler
        if steps is not None:
            kwargs['steps'] = math.floor(steps)
        if n_samples is not None:
            kwargs['n_samples'] = math.floor(n_samples)
        if smea is not None:
            kwargs['smea'] = not not math.floor(smea)
        if smea_dyn is not None:
            kwargs['smea_dyn'] = not not math.floor(smea_dyn)
        if dynamic_thresholding is not None:
            kwargs['dynamic_thresholding'] = not not math.floor(dynamic_thresholding)
        if controlnet_strength is not None:
            kwargs['controlnet_strength'] = controlnet_strength
        if controlnet_model is not None:
            kwargs['controlnet_model'] = controlnet_model
        if controlnet_condition is not None:
            kwargs['controlnet_condition'] = base64.b64encode(controlnet_condition).decode('utf-8')
        if legacy is not None:
            kwargs['legacy'] = not not math.floor(legacy)
        if image is not None:
            kwargs['image'] = base64.b64encode(image).decode('utf-8')
        if seed is not None:
            kwargs['seed'] = math.floor(seed)
        if extra_noise_seed is not None:
            kwargs['extra_noise_seed'] = math.floor(extra_noise_seed)
        if negative_prompt is not None:
            kwargs['negative_prompt'] = negative_prompt
        if dynamic_thresholding_percentile is not None:
            kwargs['dynamic_thresholding_percentile'] = dynamic_thresholding_percentile
        if dynamic_threshold_mimic is not None:
            kwargs['dynamic_threshold_mimic'] = math.floor(dynamic_threshold_mimic)
        if noise is not None:
            kwargs['noise'] = noise
        if strength is not None:
            kwargs['strength'] = strength

        return [kwargs]
