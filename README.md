# NovelUI
> **Note**
> This is currently being remade for better ui and usability. The current version is still fully functional and will continue to recieve hotfixes for any bugs until I finish the new version. Inpainting will only be added to the new version.
> 
> Finished: Image gen, save and load, node ui redesign.
> 
> Todo: Toolbar improvements, ControlNet, Image manipulation, settings window, tutorial, bug fixing.

a node-based user-interface for NovelAI

## Installation (Windows, other platforms, you're on your own for now)
1. Download source code and extract to a folder.
2. Install Python 3.
3. Open command prompt in the folder with `main.py`.
4. Run `pip install -r requirements.txt` in command prompt.
5. Create a file called `.env` and add in the line `key='NOVELAI_TOKEN_HERE'`.
6. Run `python3 main.py` in command prompt.
7. Profit. Ask me on discord if you have any questions.

## Usage - Probably missing a lot.
The top bar has lists of nodes.
- Each node has some inputs and an output, not all need to be filled. In the prompt builder every input/output (other than controlnet and img2img) has a default value.
- Each node has ports, the inputs and outputs, different shapes/colors indicate different types of data, but they are not all inclusive. Booleans are stored as ints, ints and floats are stored together, dictionaries are stored as strings, and the generic output node can display anything other than an image/zip file.
- Scroll, or use the slider at the bottom, to zoom in and out.
- Press and hold M and you can move around the screen with your mouse.
- Arrow keys move around the scene.
- Click on an output node to spawn a connection, let go on top of an input node to add it.
- Click an input node to delete its connection.
- Select nodes by using your mouse to draw a selection or just click on one and press delete to delete it.
- Selected nodes can also be moved around together.
- Hit `Execute` at the top to run your script. A window will popup with progress and logs.
- Cluster nodes automatically detect the difference between two prompts and slowly transfer between them. The advanced does it with three. They do not support differences in input strings yet.
