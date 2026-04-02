from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.core import MouseWatcher, GraphicsWindow
from direct.task import Task
from CollideObjectBase import *
from typing import Callable
from panda3d.core import CollisionHandlerEvent, CollisionTraverser
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
from direct.gui.DirectGui import *
import re
import sys

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Planet(SphereCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(CapsuleCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)

class Spaceship(SphereCollidableObject):
    def __init__(self, loader: Loader, accept: Callable[[str, Callable], None], traverser: CollisionTraverser, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.35, 0, 0.2), 1.5)
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)

        self.isMoving = False
        self.isBoosting = False
        self.baseSpeed = 5
        self.boostSpeed = 30
        self.currentSpeed = self.baseSpeed
        self.maxBoost = 300
        self.currentBoost = self.maxBoost
        self.recharging = False

        self.energyMeter = EnergyMeter(self.maxBoost, self.currentBoost)

        self.reloadTime = 0.25
        self.missileDistance = 4000
        self.missileBay = 1

        self.cntExplode = 0
        self.explodeIntervals = {}

        self.traverser = traverser

        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)

        self.mouseWatcher = base.mouseWatcherNode
        self.mouseSens = 1000

        self.winXSize = base.win.getXSize()
        self.winYSize = base.win.getYSize()
        self.prevMouseXPos = 0
        self.prevMouseYPos = 0

        taskMgr.add(self.SetPlayerRotation, 'mousePos')
        taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        taskMgr.add(self.BoostMeterLogic, 'fuel')

    def Thrust(self, keyDown):
        if keyDown:
            taskMgr.add(self.ApplyThrust, 'forward-thrust')
            self.isMoving = True
        else:
            taskMgr.remove('forward-thrust')
            self.isMoving = False
    
    def ApplyThrust(self, task):
        trajectory = render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * self.currentSpeed)

        return Task.cont
    
    def Boost(self, keyDown):
        if keyDown and self.isMoving == True and self.recharging == False:
            taskMgr.add(self.ApplyBoost, 'boost')
            self.isBoosting = True
        elif not keyDown and self.isMoving == True:
            taskMgr.remove('boost')
            self.isBoosting = False
            self.currentSpeed = self.baseSpeed

    def ApplyBoost(self, task):
        self.currentSpeed = self.boostSpeed

        return Task.cont
    
    def BoostMeterLogic(self, task):
        if self.isBoosting == True and self.recharging == False:
            self.currentBoost -= 1

            if self.currentBoost < 0:
                self.recharging = True
                self.energyMeter.RechargeMode()
                self.Boost(False)
                self.currentBoost = 0
            
            self.energyMeter.Update(self.currentBoost)
        else:
            self.currentBoost += 0.7

            if self.currentBoost > self.maxBoost:
                self.recharging = False
                self.energyMeter.Reset()
                self.currentBoost = self.maxBoost

            self.energyMeter.Update(self.currentBoost)

        #print("Boost remaining: ", self.currentBoost)
        #print(self.recharging)
        return task.cont

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
    
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            tag = 'Missile' + str(Missile.missileCount + 1)
            posVec = self.modelNode.getPos() + inFront + (6.5, 0, 4)
            currentMissile = Missile(loader, 'Assets/Phaser/phaser.egg', render, tag, posVec, 4.0)
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

            Missile.intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.intervals[tag].start()

            self.missileBay -= 1
        else:
            if not taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
            
    def CheckIntervals(self, task):
        for i in Missile.intervals:
            if not Missile.intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()

                del Missile.intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]

                print(i + ' has reached the end of its path.')

                break
        return Task.cont
            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            if self.missileBay > 1:
                self.missileBay = 1
            print("Reload complete.")
            return Task.done
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
    
    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(render))

        tempVar = fromNode.split('_')
        print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        print("TempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        print("TempVar2: " + str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))

        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)

        if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "SpaceStation"):
            print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)

        print(shooter + ' is done.')
        Missile.intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = render.find(hitID)
        nodeID.detachNode()

        self.explodeNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()

    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig("Assets/Part-Efx/basic_xpld_efx.ptf")
        self.explodeEffect.setScale(20)
        self.explodeNode = render.attachNewNode('ExplosionEffects')

    def SetKeyBindings(self):
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('shift', self.Boost, [1])
        self.accept('shift-up', self.Boost, [0])
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
        self.accept('f', self.Fire)
        self.accept('escape', self.Quit)

    def SetPlayerRotation(self, task):
        delta = globalClock.getDt()
        if self.mouseWatcher.hasMouse():
            currentMouseXPos = self.mouseWatcher.getMouseX()
            currentMouseYPos = self.mouseWatcher.getMouseY()

            #currentHead = self.modelNode.getH()
            #currentPitch = self.modelNode.getP()
            #print(currentHead, currentPitch)
            #if self.isMoving == False:
                #print("Stationary")
            #elif self.isMoving == True and self.isBoosting == False:
                #print("Moving")
            #elif self.isBoosting == True:
                #print("Boosting")

            hChange = -currentMouseXPos * delta * self.mouseSens
            pChange = currentMouseYPos * delta * self.mouseSens

            self.modelNode.setH(self.modelNode, hChange) 
            self.modelNode.setP(self.modelNode, pChange)

            base.win.movePointer(0, self.winXSize // 2, self.winYSize // 2)
             
        return task.cont
    
    def Quit(self):
        sys.exit()

class EnergyMeter(ShowBase):
    def __init__(self, max: int, current: float):
        self.maxEnergy = max
        self.currentEnergy = current
        self.meter = DirectWaitBar(value = self.currentEnergy, range = self.maxEnergy)
        self.meter['barColor'] = (0, 100, 0, 100)
        self.meter['frameSize'] = (0.6, -0.6, 0.05, -0.05)
        self.meter.setPos(-1.2, 0, 0)
        self.meter.setR(90)

    def Update(self, energy):
        self.meter['value'] = energy

    def RechargeMode(self):
        self.meter['barColor'] = (100, 0, 0, 100)

    def Reset(self):
        self.meter['barColor'] = (0, 100, 0, 100)

class Missile(SphereCollidableObject):
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    intervals = {}
    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)
        Missile.missileCount += 1

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()

        print("Firing torpedo #" + str(Missile.missileCount))

class Drone(SphereCollidableObject):
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)