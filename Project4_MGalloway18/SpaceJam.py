from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
import SpaceJamClasses
import DefensePaths

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        fullCyle = 100
        angle = 0

        self.SetupScene()
        self.SetCamera()

        for j in range(fullCyle):
            SpaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(SpaceJamClasses.Drone.droneCount)

            self.DrawCircleXDefense(self.Planet2, nickName, angle)
            self.DrawCircleYDefense(self.Planet4, nickName, angle)
            self.DrawCircleZDefense(self.Planet5, nickName, angle)
            angle = angle + 0.06
            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballDefense(self.SpaceStation, nickName, j, fullCyle, 2)
        
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

    def SetupScene(self):
        self.Universe = SpaceJamClasses.Universe(self.loader, "Assets/Universe/Universe.x", self.render, "Universe", "Assets/Textures/Sea-of-Stars.jpg", (0, 0, 0), 15000)

        self.Planet1 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet1", "Assets/Textures/Volcanic.png", (180, 4580, 70), 500)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet2", "Assets/Textures/Tropical.png", (6000, 8000, 20), 800)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet3", "Assets/Textures/Gaseous1.png", (1000, 50, 900), 100)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet4", "Assets/Textures/Martian.png", (400, 456, -2000), 50)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet5", "Assets/Textures/Venusian.png", (-10000, 36, 756), 78)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet6", "Assets/Textures/Icy.png", (-560, -54, -267), 85)

        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, "Assets/SpaceStation1B/spaceStation.egg", self.render, "SpaceStation", (0, 0, 0), 1)

        self.Spaceship = SpaceJamClasses.Spaceship(self.loader, self.accept, "Assets/Dumbledore/Dumbledore.egg", self.render, "Spaceship", (0, 0, 50), 1)
        self.Spaceship.SetKeyBindings()

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Spaceship.modelNode)
        self.camera.setFluidPos(0, -20, 0)

    def DrawCircleXDefense(self, targetObject, droneName, angle):
        unitVec = DefensePaths.CircleX(angle)
        unitVec.normalize()
        position = unitVec * (targetObject.modelNode.getSx() * 2 + 200) + targetObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, position, 2)

    def DrawCircleYDefense(self, targetObject, droneName, angle):
        unitVec = DefensePaths.CircleY(angle)
        unitVec.normalize()
        position = unitVec * (targetObject.modelNode.getSx() * 2 + 200) + targetObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, position, 2)
    
    def DrawCircleZDefense(self, targetObject, droneName, angle):
        unitVec = DefensePaths.CircleZ(angle)
        unitVec.normalize()
        position = unitVec * (targetObject.modelNode.getSx() * 2 + 200) + targetObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, position, 2)

    def DrawCloudDefense(self, targetObject, droneName):
        unitVec = DefensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * (targetObject.modelNode.getSx() * 2 + 200) + targetObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, position, 2)

    def DrawBaseballDefense(self, targetObject, droneName, step, numSeams, radius = 1):
        unitVec = DefensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * (targetObject.modelNode.getSx() * 1.3 + 150) + targetObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, droneName, position, 2)

game = Game()
game.run()