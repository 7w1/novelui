import dill
import time
import os

class Savinator():
    def __init__(self):
        self.objects_to_save = []

    def save(self):
        print("Saving...")
        dirpath = f"output/saves/{time.strftime('%Y-%m-%d', time.localtime())}"
        filename = f"Node Chart - {time.strftime('%H-%M-%S', time.localtime())}.novelui"
        fullpath = dirpath+"/"+filename
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(fullpath, 'wb+') as f:
            dill.settings['recurse'] = True
            dill.dump(self.objects_to_save, f)
        print(f"Saved your data to {fullpath}!")
    
    def load(self, filepath):
        print("Loading...")
        with open(filepath, 'rb') as f:
            objects_loaded = dill.load(f)
        self.objects_to_save = objects_loaded
        print(f"Loaded your data from {filepath}!")