from direct.actor.Actor import Actor
import sys

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame


class Player:
    def __init__(self, position, land):
        self.player = Actor('sours minecraft/ralph',
            {
                'walk': 'sours minecraft/ralph_walk',
                'run': 'sours minecraft/ralph_run'
            }
        )
        self.player.setTexture(loader.loadTexture('sours minecraft/ralph.jpg'))
        self.player.reparentTo(render)
        self.player.setPos(position)
        self.player.setScale(0.3)
        self.player.setH(45)
        self.eventHandler()
        self.firstFace()
        self.create_pause_menu()
        self.lastX = None
        self.lastY = None
        self.is_recenter = True
        self.mouseMagnitute = 10
        self.rotateX =0
        self.rotateY =0
        self.land = land

        # taskMgr.add(self.gravity, 'gravity')
        taskMgr.add(self.checkPos, 'checkPos')

        taskMgr.add(self.checkZ, 'checkZ')
    def firstFace(self):
        base.disableMouse()
        base.camera.reparentTo(self.player)
        base.camera.setZ(1.5)
        base.camera.setH(180)


    def eventHandler(self):
        base.accept('a', self.left)
        base.accept('d', self.right)
        base.accept('w', self.up)
        base.accept('s', self.down)
        base.accept("escape", self.pause)
        base.accept("mouse1",self.spawn_block)
        base.accept("mouse3",self.remove_block)

    def pause(self):
        self.panel.show()
        self.is_recenter = False

    def left(self):
        self.player.setX(self.player.getX() - 1)
    def right(self):
        self.player.setX(self.player.getX() + 1)
    def up(self):
        self.player.setY(self.player.getY() - 1)
    def down(self):
        self.player.setY(self.player.getY() + 1)



    def gravity(self, task):
        x,y,z = self.player.getPos()
        if self.land.is_empty((x, y, z-1)):
            self.player.setZ(self.player.getZ() - 1)
        else:
            print(z)
        
        return task.cont

    def checkZ(self, task):
        if self.player.getZ() < -100:
           sys.exit()
        return task.cont   

    def checkPos(self, task):
        mw = base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            # get the window manager's idea of the mouse position
            x, y = mw.getMouseX(), mw.getMouseY()

            if self.lastX is not None:
                # get the delta
                if self.is_recenter:
                    # when recentering, the position IS the delta
                    # since the center is reported as 0, 0
                    dx, dy = x, y
                else:
                    dx, dy = x - self.lastX, y - self.lastY
            else:
                # no data to compare with yet
                dx, dy = 0, 0

            self.lastX, self.lastY = x, y

        else:
            x, y, dx, dy = 0, 0, 0, 0

        if self.is_recenter:
            # move mouse back to center
            self.reCenterMouse()
            self.lastX, self.lastY = 0, 0

        self.rotateX += dx * 10 * self.mouseMagnitute
        self.rotateY += dy * 10 * self.mouseMagnitute

        self.player.setH(-self.rotateX)
        self.player.setP(-self.rotateY)

        return task.cont


    def reCenterMouse(self):
        base.win.movePointer(0,int(base.win.getProperties().getXSize()/2),int(base.win.getProperties().getYSize()/2))# I debil

    def create_pause_menu(self):
        self.panel = DirectFrame(frameColor=(1,1,1,0.5),frameSize=(-5,5, 0.5, -0.5, 0.5))
        self.exitbutton = DirectButton(parent=self.panel,text='exit',scale=0.2,command=sys.exit)
        self.exitbutton.setPos(-0.1, 0, -0.1)
        self.panel.hide()


    def get_block(self,angle):
        if angle >= 0 and angle < 20 or angle >= 335 and angle < 360:
            return 0, -1
        elif angle >= 20 and angle < 65:
            return 1, -1
        elif angle >= 65 and angle < 110:
            return  1, 0
        elif angle >= 110 and angle < 155:
            return  1, 1
        elif angle >= 155 and angle < 200:
            return  0, 1
        elif angle >= 200 and angle < 245:
            return  -1, 1
        elif angle >= 245 and angle < 290:
            return  -1, 0
        elif angle >= 290 and angle < 335:
            return  -1, -1

    def spawn_block(self):
        x,y,z = self.player.getPos()
        dX, dY =  self.get_block(self.player.getH()%360)
        if self.land.is_empty((x+dX, y+dY, z)):
            self.land.create_block((x + dX, y + dY, z))
            
    def remove_block(self):
        x, y, z = self.player.getPos()
        dX, dY =  self.get_block(self.player.getH() % 360)
        if not self.land.is_empty((x + dX, y + dY, z)):
            self.land.delete_block((x + dX, y + dY, z))
            
    