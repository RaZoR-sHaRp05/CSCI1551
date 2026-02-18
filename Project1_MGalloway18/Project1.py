from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        base.camera.setPos(0.0, 0.0, 250.0)
        base.camera.setHpr(0.0, -90.0, 0.0)

        self.Universe = self.loader.loadModel("Assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)

        texUni = self.loader.loadTexture("Assets/Universe/starfield-in-blue.jpg")
        self.Universe.setTexture(texUni, 1)

        self.Planet1 = self.loader.loadModel("Assets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150, 5000, 67)
        self.Planet1.setScale(350)
    
        
    
    


game = Game()
game.run()