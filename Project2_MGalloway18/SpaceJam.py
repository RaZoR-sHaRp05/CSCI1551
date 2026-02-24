from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
import SpaceJamClasses

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

    def SetupScene(self):
        self.Universe = SpaceJamClasses.Universe(self.loader, "Assets/Universe/Universe.x", self.render, "Universe", "Assets/Textures/Sea-of-Stars.jpg", 15000)

        self.Planet1 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet1", "Assets/Textures/Volcanic.png", (180, 4580, 70), 500)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet2", "Assets/Textures/Tropical.png", (6000, 8000, 20), 800)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet3", "Assets/Textures/Gaseous1.png", (1000, 50, 900), 100)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet4", "Assets/Textures/Martian.png", (400, 456, -2000), 50)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet5", "Assets/Textures/Venusian.png", (-10000, 36, 756), 78)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet6", "Assets/Textures/Icy.png", (-560, -54, -267), 85)

        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, "Assets/SpaceStation1B/spaceStation.x", self.render, "SpaceStation", (0, 0, 0), 1)

        self.SpaceShip = SpaceJamClasses.SpaceShip(self.loader, "Assets/Phaser/phaser.x", self.render, "SpaceShip", (0, 0, 50), 1)

game = Game()
game.SetupScene()
game.run()