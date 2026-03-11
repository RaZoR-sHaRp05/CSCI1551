from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task

class Universe(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Planet(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(ShowBase):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)

class Spaceship(ShowBase):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)

    def Thrust(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            taskMgr.remove('forward-thrust')
    
    def ApplyThrust(self, task):
        rate = 5
        trajectory = render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont
    
    def LeftTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
        rate = .5
        self.modelNode.setH(self.modelNode, rate)

        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):
        rate = -.5
        self.modelNode.setH(self.modelNode, rate)

        return Task.cont
    
    def UpTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyUpTurn, 'up-turn')
        else:
            taskMgr.remove('up-turn')

    def ApplyUpTurn(self, task):
        rate = .5
        self.modelNode.setP(self.modelNode, rate)

        return Task.cont
    
    def DownTurn(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyDownTurn, 'down-turn')
        else:
            taskMgr.remove('down-turn')

    def ApplyDownTurn(self, task):
        rate = -.5
        self.modelNode.setP(self.modelNode, rate)

        return Task.cont
    
    def RotateRight(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyRotateRight, 'rotate-right')
        else:
            taskMgr.remove('rotate-right')

    def ApplyRotateRight(self, task):
        rate = .5
        self.modelNode.setR(self.modelNode, rate)

        return Task.cont
    
    def RotateLeft(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyRotateLeft, 'rotate-left')
        else:
            taskMgr.remove('rotate-left')

    def ApplyRotateLeft(self, task):
        rate = -.5
        self.modelNode.setR(self.modelNode, rate)

        return Task.cont
    
    def SetKeyBindings(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('arrow_left', self.LeftTurn, [1])
        self.accept('arrow_left-up', self.LeftTurn, [0])
        self.accept('arrow_right', self.RightTurn, [1])
        self.accept('arrow_right-up', self.RightTurn, [0])
        self.accept('arrow_up', self.UpTurn, [1])
        self.accept('arrow_up-up', self.UpTurn, [0])
        self.accept('arrow_down', self.DownTurn, [1])
        self.accept('arrow_down-up', self.DownTurn, [0])
        self.accept('x', self.RotateRight, [1])
        self.accept('x-up', self.RotateRight, [0])
        self.accept('z', self.RotateLeft, [1])
        self.accept('z-up', self.RotateLeft, [0])



class Drone(ShowBase):
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)