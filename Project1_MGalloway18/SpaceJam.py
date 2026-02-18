from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.Universe = self.loader.loadModel("Assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)

        texUni = self.loader.loadTexture("Assets/Universe/starfield-in-blue.jpg")
        self.Universe.setTexture(texUni, 1)

        self.Planet1 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(180, 4580, 70)
        self.Planet1.setScale(500)

        self.Planet2 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(6000, 8000, 20)
        self.Planet2.setScale(800)

        self.Planet3 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(1000, 50, 900)
        self.Planet3.setScale(100)

        self.Planet4 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(400, 456, -2000)
        self.Planet4.setScale(50)

        self.Planet5 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(-10000, 36, 756)
        self.Planet5.setScale(78)

        self.Planet6 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(-560, -54, -267)
        self.Planet6.setScale(85)

        texPlan1 = self.loader.loadTexture("Assets/Textures/Volcanic.png")
        self.Planet1.setTexture(texPlan1, 1)
        texPlan2 = self.loader.loadTexture("Assets/Textures/Tropical.png")
        self.Planet2.setTexture(texPlan2, 1)
        texPlan3 = self.loader.loadTexture("Assets/Textures/Gaseous1.png")
        self.Planet3.setTexture(texPlan3, 1)
        texPlan4 = self.loader.loadTexture("Assets/Textures/Martian.png")
        self.Planet4.setTexture(texPlan4, 1)
        texPlan5 = self.loader.loadTexture("Assets/Textures/Venusian.png")
        self.Planet5.setTexture(texPlan5, 1)
        texPlan6 = self.loader.loadTexture("Assets/Textures/Icy.png")
        self.Planet6.setTexture(texPlan6, 1)

        self.SpaceStation = self.loader.loadModel("Assets/SpaceStation1B/spaceStation.x")
        self.SpaceStation.reparentTo(self.render)

        self.SpaceShip = self.loader.loadModel("Assets/Phaser/phaser.x")
        self.SpaceShip.reparentTo(self.render)
        self.SpaceShip.setPos(0, 0, 50)
    
        
    
    


game = Game()
game.run()