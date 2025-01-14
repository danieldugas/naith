# -*- coding: utf-8 -*-
# Copyright Tom SF Haines
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from panda3d.core import *


class Camera:
  """Does camera set up - will probably end up with lots of options."""
  def __init__(self,manager,xml):
    base.camNode.setCameraMask(BitMask32.bit(0))
    base.disableMouse()
    self.reload(manager,xml)


  def reload(self,manager,xml):
    # Get the cameras initial position from the configuration file - only matters if the camera isn't about to be made a child of a node to be controlled elsewhere...
    pos = xml.find('pos')
    if pos!=None:
      self.pos = (float(pos.get('x')),float(pos.get('y')),float(pos.get('z')))
    else:
      self.pos = None

    # Get the cameras initial looking at position - just like position this is pointless if the camera will be tracking a node...
    lookAt = xml.find('lookAt')
    if lookAt!=None:
      self.lookAt = (float(lookAt.get('x')),float(lookAt.get('y')),float(lookAt.get('z')))
    else:
      self.lookAt = None

    # Sets a parent node for the camera - the camera will then move and rotate how this node modes and rotates...
    track = xml.find('track')
    if track!=None:
      self.track = manager.get(track.get('plugin')).getNode(track.get('node'))
    else:
      self.track = None

    # Get the zooming parameters, used to set how the normal field of view and the field of view used when the player looks down the weapon...
    fov = xml.find('fov')
    self.zoomed = False
    if fov!=None:
      self.normal = float(fov.get('deg'))
      self.zoom = float(fov.get('zoom'))
      self.speed = (self.normal-self.zoom) / float(fov.get('zoomTime'))

      base.camLens.setNearFar(float(fov.get('near')),float(fov.get('far')))
    else:
      self.normal = 70.0
      self.zoom = 50.0
      self.speed = 200.0

    base.camLens.setFov(self.normal)


  def start(self):
    # Apply the camera details...
    if self.pos!=None:
      base.camera.setPos(self.pos[0],self.pos[1],self.pos[2])

    if self.lookAt!=None:
      base.camera.lookAt(self.lookAt[0],self.lookAt[1],self.lookAt[2])

    if self.track!=None:
      base.camera.reparentTo(self.track)
      base.camera.setPos(0.0,0.0,0.0)
      base.camera.lookAt(0.0,1.0,0.0)
    
    # Create a task that tweaks the cameras fov to do the zooming in requiured when the player looks down a gun...
    def trackZoom(task):
      fov = base.camLens.getFov()[0]
      if self.zoomed:
        fov = max(self.zoom,fov - self.speed*globalClock.getDt())
      else:
        fov = min(self.normal,fov + self.speed*globalClock.getDt())
      base.camLens.setFov(fov)
      return task.cont

    self.zoomTask = taskMgr.add(trackZoom,'Camera Zoom Control')


  def stop(self):
    # Remove the camera zooming task...
    taskMgr.remove(self.zoomTask)
    self.zoomTask = None


  def oobe(self):
    base.oobe()

  def setZoomed(self,s):
    self.zoomed = s
