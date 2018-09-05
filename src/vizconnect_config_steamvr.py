"""
This module was generated by Vizconnect.
Version: 1.04
Generated on: 2015-11-13 04:20:15.814000
"""

import viz
import vizconnect

#################################
# Parent configuration, if any
#################################

def getParentConfiguration():
	#VC: set the parent configuration
	_parent = ''
	
	#VC: return the parent configuration
	return _parent


#################################
# Pre viz.go() Code
#################################

def preVizGo():
	return True


#################################
# Pre-initialization Code
#################################

def preInit():
	"""Add any code here which should be called after viz.go but before any initializations happen.
	Returned values can be obtained by calling getPreInitResult for this file's vizconnect.Configuration instance."""
	return None


#################################
# Group Code
#################################

def initGroups(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawGroup = vizconnect.getRawGroupDict()
	
	#VC: return values can be modified here
	return None


#################################
# Display Code
#################################

def initDisplays(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawDisplay = vizconnect.getRawDisplayDict()

	#VC: initialize a new display
	_name = 'main_display'
	if vizconnect.isPendingInit('display', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set the window for the display
			_window = viz.MainWindow
			
			#VC: set some parameters
			index = 0
			
			#VC: create the raw object
			import steamvr
			# Get sensor from extension if not specified
			hmd = None
			sensor = None
			hmdList = steamvr.getExtension().getHMDList()
			if hmdList:
				try:
					sensor = hmdList[index]
				except IndexError:
					viz.logError("** ERROR: Not enough HMD's")
			else:
				viz.logError('** ERROR: Failed to detect SteamVR HMD')
			if sensor:
				hmd = steamvr.HMD(sensor=sensor, window=_window)
			_window.displayNode = hmd
			rawDisplay[_name] = _window
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addDisplay(rawDisplay[_name], _name, make='Valve', model='SteamVR HMD')
	
		#VC: set the parent of the node
		if initFlag&vizconnect.INIT_PARENTS:
			vizconnect.getDisplay(_name).setParent(vizconnect.getAvatar('main_avatar').getAttachmentPoint('head'))

	#VC: set the name of the default
	vizconnect.setDefault('display', 'main_display')

	#VC: return values can be modified here
	return None


#################################
# Tracker Code
#################################

def initTrackers(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTracker = vizconnect.getRawTrackerDict()

	#VC: initialize a new tracker
	_name = 'head_tracker'
	if vizconnect.isPendingInit('tracker', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 0
			
			#VC: create the raw object
			import steamvr
			try:
				tracker = steamvr.getExtension().getHMDList()[index]
			except IndexError:
				viz.logWarn("** WARNING: Not able to connect to tracker at index {0}. It's likely that not enough trackers are connected.".format(index))
				tracker = viz.addGroup()
				tracker.invalidTracker = True
			rawTracker[_name] = tracker
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addTracker(rawTracker[_name], _name, make='Valve', model='SteamVR HMD Tracker')

	#VC: initialize a new tracker
	_name = 'r_hand_tracker'
	if vizconnect.isPendingInit('tracker', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 0
			
			#VC: create the raw object
			import steamvr
			try:
				tracker = steamvr.getControllerList()[index]
			except IndexError:
				viz.logWarn("** WARNING: Not able to connect to tracker at index {0}. It's likely that not enough trackers are connected.".format(index))
				tracker = viz.addGroup()
				tracker.invalidTracker = True
			rawTracker[_name] = tracker
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addTracker(rawTracker[_name], _name, make='Valve', model='SteamVR Controller Tracker')

	#VC: initialize a new tracker
	_name = 'l_hand_tracker'
	if vizconnect.isPendingInit('tracker', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 1
			
			#VC: create the raw object
			import steamvr
			try:
				tracker = steamvr.getControllerList()[index]
			except IndexError:
				viz.logWarn("** WARNING: Not able to connect to tracker at index {0}. It's likely that not enough trackers are connected.".format(index))
				tracker = viz.addGroup()
				tracker.invalidTracker = True
			rawTracker[_name] = tracker
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addTracker(rawTracker[_name], _name, make='Valve', model='SteamVR Controller Tracker')

	#VC: set the name of the default
	vizconnect.setDefault('tracker', 'head_tracker')

	#VC: return values can be modified here
	return None


#################################
# Input Code
#################################

def initInputs(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawInput = vizconnect.getRawInputDict()

	#VC: initialize a new input
	_name = 'keyboard'
	if vizconnect.isPendingInit('input', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 0
			
			#VC: create the raw object
			d = viz.add('directinput.dle')
			device = d.getKeyboardDevices()[index]
			rawInput[_name] = d.addKeyboard(device)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addInput(rawInput[_name], _name, make='Generic', model='Keyboard')

	#VC: initialize a new input
	_name = 'r_hand_input'
	if vizconnect.isPendingInit('input', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 0
			
			#VC: create the raw object
			import steamvr
			try:
				input = steamvr.getControllerList()[index]
				input._isValid = True
			except IndexError:
				viz.logWarn("** WARNING: Not able to connect to a controller at index {0}. It's likely that not enough controllers are connected.".format(index))
				input = viz.VizExtensionSensor(-1)
				input.isButtonDown = lambda e: False
				input.getTrackpad = lambda: [0,0]
				input._isValid = False
			rawInput[_name] = input
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addInput(rawInput[_name], _name, make='HTC', model='Vive Controller')
	
		#VC: init the mappings for the wrapper
		if initFlag&vizconnect.INIT_WRAPPER_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(input):
					if rawInput['r_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Trigger
						input.setQuasimode()
				vizconnect.getInput(_name).setUpdateFunction(update)

	#VC: initialize a new input
	_name = 'l_hand_input'
	if vizconnect.isPendingInit('input', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			index = 1
			
			#VC: create the raw object
			import steamvr
			try:
				input = steamvr.getControllerList()[index]
				input._isValid = True
			except IndexError:
				viz.logWarn("** WARNING: Not able to connect to a controller at index {0}. It's likely that not enough controllers are connected.".format(index))
				input = viz.VizExtensionSensor(-1)
				input.isButtonDown = lambda e: False
				input.getTrackpad = lambda: [0,0]
				input._isValid = False
			rawInput[_name] = input
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addInput(rawInput[_name], _name, make='HTC', model='Vive Controller')

	#VC: set the name of the default
	vizconnect.setDefault('input', 'r_hand_input')

	#VC: return values can be modified here
	return None


#################################
# Event Code
#################################

def initEvents(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawEvent = vizconnect.getRawEventDict()

	#VC: initialize a new event
	_name = 'CONTROL_NEW_FILE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['keyboard'].isButtonDown(49):# make=Generic, model=Keyboard, name=keyboard, signal=Key N
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_CYCLE_VIEW_MODE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['l_hand_input'].isButtonDown(0):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Menu
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_MATERIAL_TRIGGER'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['r_hand_input'].isButtonDown(3):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Trackpad
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_CLIP'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['r_hand_input'].isButtonDown(1):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Grip
						event.sendOnce(e=viz.Event(mag=1))
					if rawInput['l_hand_input'].isButtonDown(1):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Grip
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_CLOUD_INCREASE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['l_hand_input'].getTrackpad()[1] > 0.01 and\
						rawInput['l_hand_input'].isButtonDown(3):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Trackpad Top (along with) make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Trackpad
						event.sendOnce(e=viz.Event(mag=abs(rawInput['l_hand_input'].getTrackpad()[1]) * 1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_CLOUD_DECREASE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['l_hand_input'].getTrackpad()[1] < -0.01 and\
						rawInput['l_hand_input'].isButtonDown(3):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Trackpad Bottom (along with) make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Trackpad
						event.sendOnce(e=viz.Event(mag=abs(rawInput['l_hand_input'].getTrackpad()[1]) * 1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_TOGGLE_STRESSINDICATOR'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['r_hand_input'].isButtonDown(0):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Menu
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_TOGGLE_ENVIRONMENT'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['keyboard'].isButtonDown(19):# make=Generic, model=Keyboard, name=keyboard, signal=Key R
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_LEFT_HAND_GRAB'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['l_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Trigger
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_LEFT_HAND_RELEASE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if not rawInput['l_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Trigger
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_RIGHT_HAND_GRAB'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['r_hand_input'].isInMode('super') and rawInput['r_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Trigger
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: initialize a new event
	_name = 'CONTROL_RIGHT_HAND_RELEASE'
	if vizconnect.isPendingInit('event', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: create the raw object
			from vizconnect.util import events
			rawEvent[_name] = events.CustomEvent(viz.getEventID(_name))
	
		#VC: init the mappings for the raw object
		if initFlag&vizconnect.INIT_MAPPINGS:
			#VC: per frame mappings
			if initFlag&vizconnect.INIT_MAPPINGS_PER_FRAME:
				#VC: get the raw input dict so we have access to signals
				import vizact
				rawInput = vizconnect.getConfiguration().getRawDict('input')
				#VC: set the update function which checks for input signals
				def update(event):
					if rawInput['r_hand_input'].isInMode('super') and not rawInput['r_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Trigger
						event.sendOnce(e=viz.Event(mag=1))
				rawEvent[_name].setUpdateFunction(update)
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addEvent(rawEvent[_name], _name, make='Vizconnect', model='Custom')

	#VC: return values can be modified here
	return None


#################################
# Transport Code
#################################

def initTransports(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTransport = vizconnect.getRawTransportDict()

	#VC: return values can be modified here
	return None


#################################
# Tool Code
#################################

def initTools(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawTool = vizconnect.getRawToolDict()

	#VC: return values can be modified here
	return None


#################################
# Avatar Code
#################################

def initAvatars(initFlag=vizconnect.INIT_INDEPENDENT, initList=None):
	#VC: place any general initialization code here
	rawAvatar = vizconnect.getRawAvatarDict()

	#VC: initialize a new avatar
	_name = 'main_avatar'
	if vizconnect.isPendingInit('avatar', _name, initFlag, initList):
		#VC: init the raw object
		if initFlag&vizconnect.INIT_RAW:
			#VC: set some parameters
			head = False
			rightHand = False
			leftHand = False
			torso = False
			lowerBody = False
			rightArm = False
			leftArm = False
			
			#VC: create the raw object
			# base avatar
			import vizfx
			avatar = vizfx.addChild('mark.cfg')
			avatar._bodyPartDict = {}
			avatar._handModelDict = {}
			avatar.visible(head, r'mark_head.cmf')
			avatar.visible(rightHand, r'mark_hand_r.cmf')
			avatar.visible(leftHand, r'mark_hand_l.cmf')
			avatar.visible(torso, r'mark_torso.cmf')
			avatar.visible(lowerBody, r'mark_legs.cmf')
			avatar.visible(rightArm, r'mark_arm_r.cmf')
			avatar.visible(leftArm, r'mark_arm_l.cmf')
			rawAvatar[_name] = avatar
	
		#VC: init the wrapper (DO NOT EDIT)
		if initFlag&vizconnect.INIT_WRAPPERS:
			vizconnect.addAvatar(rawAvatar[_name], _name, make='WorldViz', model='Mark')
	
		#VC: init the gestures
		if initFlag&vizconnect.INIT_GESTURES:
			#VC: need to get the raw input dict so we have access to signals
			import vizact
			rawInput = vizconnect.getConfiguration().getRawDict('input')
			
			#VC: gestures for the avatar's r_hand
			import hand
			def initHand():
				sensor = hand.InputSensor()
				rawAvatar[_name].handSensor = sensor
				sensor.createHandRenderer = lambda *args,**kw: hand._InputDeviceRenderer(*args,**kw)
				def appliedGetData():
					#VC: set the mappings for the gestures
					if rawInput['r_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=r_hand_input, signal=Button Trigger
						return (hand.GESTURE_FIST, False, False)# GESTURE_FIST
					#VC: end gesture mappings
					return (hand.GESTURE_FLAT_HAND,False,False)
				sensor.getData = appliedGetData
				return hand.AvatarHandModel(rawAvatar[_name], left=False, type=hand.GLOVE_5DT, sensor=sensor)
			rightHand = initHand()
			rawAvatar[_name]._bodyPartDict[vizconnect.AVATAR_R_HAND] = rightHand
			rawAvatar[_name]._handModelDict[vizconnect.AVATAR_R_HAND] = rightHand
			#VC: gestures for the avatar's l_hand
			import hand
			def initHand():
				sensor = hand.InputSensor()
				rawAvatar[_name].handSensor = sensor
				sensor.createHandRenderer = lambda *args,**kw: hand._InputDeviceRenderer(*args,**kw)
				def appliedGetData():
					#VC: set the mappings for the gestures
					if rawInput['l_hand_input'].isButtonDown(2):# make=HTC, model=Vive Controller, name=l_hand_input, signal=Button Trigger
						return (hand.GESTURE_FIST, False, False)# GESTURE_FIST
					#VC: end gesture mappings
					return (hand.GESTURE_FLAT_HAND,False,False)
				sensor.getData = appliedGetData
				return hand.AvatarHandModel(rawAvatar[_name], left=True, type=hand.GLOVE_5DT, sensor=sensor)
			leftHand = initHand()
			rawAvatar[_name]._bodyPartDict[vizconnect.AVATAR_L_HAND] = leftHand
			rawAvatar[_name]._handModelDict[vizconnect.AVATAR_L_HAND] = leftHand
			
			#VC: gestures may change the raw avatar, so refresh the raw in the wrapper
			vizconnect.getAvatar(_name).setRaw(rawAvatar[_name])
	
		#VC: init the animator
		if initFlag&vizconnect.INIT_ANIMATOR:
			# need to get the raw tracker dict for animating the avatars
			from vizconnect.util.avatar import animator
			from vizconnect.util.avatar import skeleton
			
			# get the skeleton from the avatar
			_skeleton = skeleton.CompleteCharactersHD(rawAvatar[_name])
			
			#VC: set which trackers animate which body part
			# format is: bone: (tracker, parent, degrees of freedom used)
			_trackerAssignmentDict = {
				vizconnect.AVATAR_HEAD:(vizconnect.getTracker('head_tracker').getNode3d(), None, vizconnect.DOF_6DOF),
				vizconnect.AVATAR_L_HAND:(vizconnect.getTracker('l_hand_tracker').getNode3d(), None, vizconnect.DOF_6DOF),
				vizconnect.AVATAR_R_HAND:(vizconnect.getTracker('r_hand_tracker').getNode3d(), None, vizconnect.DOF_6DOF),
			}
			
			#VC: create the raw object
			_rawAnimator = animator.Direct(rawAvatar[_name], _skeleton, _trackerAssignmentDict)
			
			#VC: set animator in wrapper (DO NOT EDIT)
			vizconnect.getAvatar(_name).setAnimator(_rawAnimator, make='Virtual', model='Direct')
	
		#VC: set the parent of the node
		if initFlag&vizconnect.INIT_PARENTS:
			vizconnect.getAvatar(_name).setParent(vizconnect.getRoot())

	#VC: set the name of the default
	vizconnect.setDefault('avatar', 'main_avatar')

	#VC: return values can be modified here
	return None


#################################
# Application Settings
#################################

def initSettings():
	#VC: apply general application settings
	viz.mouse.setTrap(False)
	viz.mouse.setVisible(viz.MOUSE_AUTO_HIDE)
	vizconnect.setMouseTrapToggleKey('')
	
	#VC: return values can be modified here
	return None


#################################
# Post-initialization Code
#################################

def postInit():
	"""Add any code here which should be called after all of the initialization of this configuration is complete.
	Returned values can be obtained by calling getPostInitResult for this file's vizconnect.Configuration instance."""
	return None


#################################
# Stand alone configuration
#################################

def initInterface():
	#VC: start the interface
	vizconnect.interface.go(__file__,
							live=True,
							openBrowserWindow=True,
							startingInterface=vizconnect.interface.INTERFACE_STARTUP)

	#VC: return values can be modified here
	return None


###############################################

if __name__ == "__main__":
	initInterface()
	viz.add('piazza.osgb')
	viz.add('piazza_animations.osgb')
