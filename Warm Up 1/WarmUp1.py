from direct.showbase.ShowBase import ShowBase
from panda3d.core import Filename

import math, sys, random

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.fighter = self.loader.loadModel("Assets/sphere")
        self.fighter.reparentTo(self.render)
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0)

        self.accept('escape', self.quit)

    def quit(self):
        sys.exit()

app = MyApp()
app.run()