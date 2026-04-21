from direct.showbase.ShowBase import ShowBase
from panda3d.core import PandaNode, NodePath
from panda3d.core import Filename
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import MouseWatcher
from panda3d.core import *
import SpaceJamClasses
import DefensePaths
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import Point3, Point2
from direct.task import Task
from direct.gui.DirectGui import *
import sys

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        fullCyle = 100
        angle = 0
        
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)

        self.paused = False

        self.dummy = NodePath('dummy')
        self.dummy.reparentTo(self.render)
        self.target = NodePath('target')
        self.target2 = NodePath('target2')

        self.EnableHUD()
        self.SetupScene()
        self.SetCamera()

        self.target.setScale(0.25)
        self.target.reparentTo(self.Spaceship.modelNode)
        self.target.setPos(0.35, 15, 0)
        self.target2.setScale(0.25)
        self.target2.reparentTo(self.Spaceship.modelNode)
        self.target2.setPos(0.35, 20, 0)
        
        self.title = OnscreenText(text = "PAUSED", scale = 0.3, pos = (0, 0.6))
        self.title["fg"] = (1, 1, 1, 1)
        self.title.hide()
        self.resumeButton = DirectButton(text = "RESUME", scale = 0.2, pos = (0, 0, 0.2))
        self.resumeButton["command"] = self.Pause
        self.resumeButton["state"] = DGG.DISABLED
        self.resumeButton.hide()
        self.quitButton = DirectButton(text = "QUIT", scale = 0.2, pos = (0, 0, -0.4))
        self.quitButton["state"] = DGG.DISABLED
        self.quitButton['command'] = self.Quit
        self.quitButton.hide()

        for j in range(fullCyle):
            SpaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(SpaceJamClasses.Drone.droneCount)

            #self.DrawCircleXDefense(self.Planet2, nickName, angle)
            self.DrawCircleYDefense(self.Planet4, nickName, angle)
            self.DrawCircleZDefense(self.Planet5, nickName, angle)
            angle = angle + 0.06
            #self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballDefense(self.SpaceStation, nickName, j, fullCyle, 2)
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

        self.accept('escape', self.Pause)

    def SetupScene(self):
        self.Universe = SpaceJamClasses.Universe(self.loader, "Assets/Universe/Universe.x", self.render, "Universe", "Assets/Textures/Sea-of-Stars.jpg", (0, 0, 0), 15000)

        self.Planet1 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet1", "Assets/Textures/Volcanic.png", (180, 4580, 70), 500)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet2", "Assets/Textures/Tropical.png", (6000, 8000, 20), 800)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet3", "Assets/Textures/Gaseous1.png", (1000, 50, 900), 100)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet4", "Assets/Textures/Martian.png", (400, 456, -2000), 50)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet5", "Assets/Textures/Venusian.png", (-10000, 36, 756), 78)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "Assets/protoPlanet.x", self.render, "Planet6", "Assets/Textures/Icy.png", (-560, -54, -267), 85)

        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, "Assets/SpaceStation1B/spaceStation.egg", self.render, "SpaceStation", (0, 0, 0), 1)

        self.Spaceship = SpaceJamClasses.Spaceship(self.loader, self.dummy, self.Hud, self.Hud2, self.accept, self.cTrav, "Assets/Dumbledore/Dumbledore.egg", self.render, "Spaceship", (0, 0, 50), 1)
        self.Spaceship.SetKeyBindings()
        
        self.Sentinel1 = SpaceJamClasses.Orbiter(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Planet6, 500, "MLB", self.Spaceship)
        self.Sentinel2 = SpaceJamClasses.Orbiter(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Planet3, 500, "MLB", self.Spaceship)
        self.Sentinel3 = SpaceJamClasses.Orbiter(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Planet1, 900, "Cloud", self.Spaceship)
        self.Sentinel4 = SpaceJamClasses.Orbiter(self.loader, "Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Planet2, 900, "Cloud", self.Spaceship)

        self.Wanderer1 = SpaceJamClasses.Wanderer(self.loader,"Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Spaceship)
        self.Wanderer1.setInterval(self.Planet1.modelNode.getPos(), self.Planet2.modelNode.getPos(), self.Planet3.modelNode.getPos())
        self.Wanderer2 = SpaceJamClasses.Wanderer(self.loader,"Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 6.0, self.Spaceship)
        self.Wanderer2.setInterval(self.Planet4.modelNode.getPos(), self.Planet5.modelNode.getPos(), self.Planet6.modelNode.getPos())

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.dummy)
        self.camera.setFluidPos(0.3, -8, 2)

    def Pause(self):
        if not self.paused:
            self.Show()
            self.Spaceship.Pause()
            self.Sentinel1.Pause()
            self.Sentinel2.Pause()
            self.Sentinel3.Pause()
            self.Sentinel4.Pause()
            self.Wanderer1.Pause()
            self.Wanderer2.Pause()
            self.paused = True
        else:
            self.Hide()
            self.Spaceship.Pause()
            self.Sentinel1.Pause()
            self.Sentinel2.Pause()
            self.Sentinel3.Pause()
            self.Sentinel4.Pause()
            self.Wanderer1.Pause()
            self.Wanderer2.Pause()
            self.paused = False

    def Show(self):
        self.title.show()
        self.resumeButton.show()
        self.resumeButton["state"] = DGG.NORMAL
        self.quitButton.show()
        self.quitButton["state"] = DGG.NORMAL

    def Hide(self):
        self.title.hide()
        self.resumeButton.hide()
        self.resumeButton["state"] = DGG.DISABLED
        self.quitButton.hide()
        self.quitButton["state"] = DGG.DISABLED

    def Quit(self):
        sys.exit()

    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 3)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
        self.Hud.reparentTo(self.target)
        self.Hud.setBillboardPointEye()
        self.Hud.setBin('fixed', 1)
        self.Hud.setDepthTest(False)
        self.Hud2 = OnscreenImage(image = "Assets/Hud/Reticle3b.png", pos = Vec3(0, 0, 0), scale = 2)
        self.Hud2.setTransparency(TransparencyAttrib.MAlpha)
        self.Hud2.reparentTo(self.target2)
        self.Hud2.setBillboardPointEye()
        self.Hud2.setBin('fixed', 0)
        self.Hud2.setDepthTest(False)

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