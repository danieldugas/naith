#! /usr/bin/env python
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
from __future__ import print_function



# Entry point - sets up the plugin system by giving it the config file to load and then releases panda to do its thing...

# Important: this must be first
from panda3d.core import loadPrcFile, loadPrcFileData
loadPrcFile("config/settings.prc")
loadPrcFileData("window-disable", "window-type none")
from direct.showbase.ShowBase import ShowBase
import direct.stdpy.file as pfile
from direct.task import Task

from bin.manager import *

import sys

base = ShowBase()
#messenger.toggleVerbose()

# Detect if we are in a multifile and, if so, jump through hoops that shouldn't exist...
if base.appRunner!=None:
  print('In multifile, root = '+base.appRunner.multifileRoot)
  baseDir = base.appRunner.multifileRoot+'/'
else:
  baseDir = ''

# Create the manager - this does it all...
plugin = Manager(baseDir)

# Create a task to do the work of getting the game going...
def firstLight(task):
  if len(sys.argv)>1:
    cn = sys.argv[1]
  else:
    cn = 'menu'
  
  print('Starting configuration ' + cn)
  plugin.transition(cn)
  return Task.done

taskMgr.add(firstLight,'firstLight')
base.run()
