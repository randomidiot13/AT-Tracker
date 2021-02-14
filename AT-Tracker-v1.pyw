from tkinter import *
from tkinter import filedialog as fd
import os
import json

BIOMES = ["Beach", "Birch Forest", "Birch Forest Hills", "Cold Beach",
          "Cold Taiga", "Cold Taiga Hills", "Deep Ocean", "Desert",
          "DesertHills", "Extreme Hills", "Extreme Hills+", "Forest",
          "ForestHills", "FrozenRiver", "Ice Mountains", "Ice Plains",
          "Jungle", "JungleEdge", "JungleHills", "Mega Taiga",
          "Mega Taiga Hills", "Mesa", "Mesa Plateau", "Mesa Plateau F",
          "MushroomIsland", "MushroomIslandShore", "Ocean", "Plains",
          "River", "Roofed Forest", "Savanna", "Savanna Plateau",
          "Stone Beach", "Swampland", "Taiga", "TaigaHills"]

class Tracker(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        self.title("AT Tracker v1")
        self.wm_attributes("-topmost", 1)

        self.directory_default_button = Button(self, text = "Default Directory", command = self.default_directory, relief = FLAT)
        self.directory_default_button.grid(row = 0, column = 0)
        
        self.display_title = Label(self, text = "Adventuring Time Tracker")
        self.display_title.grid(row = 0, column = 1, columnspan = 2)

        self.directory_set_button = Button(self, text = "Change Directory", command = self.set_directory, relief = FLAT)
        self.directory_set_button.grid(row = 0, column = 3)
        
        self.biomes = [Label(self, text = biome, bg = 'IndianRed1', width = 20)
                       for biome in BIOMES]
        for count, biome in enumerate(self.biomes):
            biome.grid(row = 1 + count // 4, column = count % 4)
            
        self.errors = Label(self, text = "")
        self.errors.grid(columnspan = 4)

        self.default_directory()
        
        self.id = self.after(1000, self.update)

    def default_directory(self):
        self.directory = os.path.join(os.getenv('APPDATA'), r'.minecraft')

    def set_directory(self):
        self.directory = fd.askdirectory(title = "Select Folder")

    @property
    def saves(self):
        return os.path.join(self.directory, 'saves')

    def get_newest_world(self):
        return max([os.path.join(self.saves, name)
                    for name in os.listdir(self.saves)],
                   key = os.path.getmtime)

    def get_stats_json(self, world_file):
        stats_folder = os.path.join(world_file, 'stats')
        with open(os.path.join(stats_folder, os.listdir(stats_folder)[0])) as f:
            data = json.load(f)
        return data

    def update(self):
        try:
            world = self.get_newest_world()
        except:
            self.errors.configure(text = "No world file detected")
            for biome in self.biomes:
                biome.configure(bg = 'IndianRed1')
        else:
            try:
                stats = self.get_stats_json(world)
            except:
                world_name = world.split('\\')[-1]
                if len(world_name) > 50:
                    world_name = world_name[:50] + '...'
                self.errors.configure(text = f"Reading from {world_name} - No stats file detected")
                for biome in self.biomes:
                    biome.configure(bg = 'IndianRed1')
            else:
                world_name = world.split('\\')[-1]
                if len(world_name) > 50:
                    world_name = world_name[:50] + '...'
                self.errors.configure(text = f"Reading from {world_name}")
                if 'achievement.exploreAllBiomes' in stats:
                    biomes_list = stats['achievement.exploreAllBiomes']['progress']
                    for count, biome in enumerate(BIOMES):
                        if biome in biomes_list:
                            self.biomes[count].configure(bg = 'SpringGreen3')
                        else:
                            self.biomes[count].configure(bg = 'IndianRed1')
                else:
                    for biome in self.biomes:
                        biome.configure(bg = 'IndianRed1')
                            
        self.id = self.after(1000, self.update)

Tracker().mainloop()
