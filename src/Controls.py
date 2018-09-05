"""
Copyright 2018 Andreas Wundlechner

GNU Lesser General Public License Usage
This file has to be used under the terms of the GNU Lesser
General Public License version 3 or later as published by the Free Software
Foundation and appearing in the file LICENSE included in the
packaging of this file. Please review the following information to
ensure the GNU Lesser General Public License version 3 requirements
will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
"""

"""
This file takes care of the controls.
The events of vizconnect couldn't be used here, because it always sends an event object as first parameter.
Altering the subscribed function to recieve that object results in bad function signatures.
"""

import viz
import vizconnect
import math


# Define the Events, which can be subscribed to
CONTROL_NEW_FILE = viz.getEventID("CONTROL_NEW_FILE_INTERNAL")
CONTROL_CLIP = viz.getEventID("CONTROL_CLIP_INTERNAL")
CONTROL_TOGGLE_ENVIRONMENT = viz.getEventID("CONTROL_TOGGLE_ENVIRONMENT_INTERNAL")
CONTROL_CLOUD_INCREASE = viz.getEventID("CONTROL_CLOUD_INCREASE_INTERNAL")
CONTROL_CLOUD_DECREASE = viz.getEventID("CONTROL_CLOUD_DECREASE_INTERNAL")
CONTROL_CYCLE_VIEW_MODE = viz.getEventID("CONTROL_CYCLE_VIEW_MODE_INTERNAL")
CONTROL_MATERIAL = viz.getEventID("CONTROL_MATERIAL_INTERNAL")
CONTROL_TOGGLE_STRESSINDICATOR = viz.getEventID("CONTROL_TOGGLE_STRESSINDICATOR_INTERNAL")
CONTROL_HAND_GRAB = viz.getEventID("CONTROL_HAND_GRAB_INTERNAL")
CONTROL_HAND_RELEASE = viz.getEventID("CONTROL_HAND_RELEASE_INTERNAL")


class _Controls(viz.EventClass):
	"""
	This class is only used to register the forwarding callbacks.
	Otherwise the global events had to be used, which could result in problems with other scripts.
	"""
	def __init__(self):
		viz.EventClass.__init__(self)

_c = _Controls()
_right_hand_number = 0
_left_hand_number = 1
# Register the forwarding callbacks
_c.callback(viz.getEventID("CONTROL_NEW_FILE"), lambda e: viz.sendEvent(CONTROL_NEW_FILE))
_c.callback(viz.getEventID("CONTROL_CLIP"), lambda e: viz.sendEvent(CONTROL_CLIP))
_c.callback(viz.getEventID("CONTROL_TOGGLE_ENVIRONMENT"), lambda e: viz.sendEvent(CONTROL_TOGGLE_ENVIRONMENT))
_c.callback(viz.getEventID("CONTROL_CLOUD_INCREASE"), lambda e: viz.sendEvent(CONTROL_CLOUD_INCREASE))
_c.callback(viz.getEventID("CONTROL_CLOUD_DECREASE"), lambda e: viz.sendEvent(CONTROL_CLOUD_DECREASE))
_c.callback(viz.getEventID("CONTROL_CYCLE_VIEW_MODE"), lambda e: viz.sendEvent(CONTROL_CYCLE_VIEW_MODE))
_c.callback(viz.getEventID("CONTROL_TOGGLE_STRESSINDICATOR"), lambda e: viz.sendEvent(CONTROL_TOGGLE_STRESSINDICATOR))
_c.callback(viz.getEventID("CONTROL_RIGHT_HAND_GRAB"), lambda e: viz.sendEvent(CONTROL_HAND_GRAB, _right_hand_number))
_c.callback(viz.getEventID("CONTROL_LEFT_HAND_GRAB"), lambda e: viz.sendEvent(CONTROL_HAND_GRAB, _left_hand_number))
_c.callback(viz.getEventID("CONTROL_RIGHT_HAND_RELEASE"), lambda e: viz.sendEvent(CONTROL_HAND_RELEASE, _right_hand_number))
_c.callback(viz.getEventID("CONTROL_LEFT_HAND_RELEASE"), lambda e: viz.sendEvent(CONTROL_HAND_RELEASE, _left_hand_number))


# Keyboard specifics
def _on_key_down(key):
	"""
	Call the CONTROL_MATERIAL event dependent on the pressed number key.
	"""
	try:
		number = int(key)
		viz.sendEvent(CONTROL_MATERIAL, number)
	except:
		pass
_c.callback(viz.KEYDOWN_EVENT, _on_key_down)


# Vive Controller specifics
_material_range = (1,2)

def set_material_range(range):
	"""
	Adjust the amount of available materials
	"""
	global _material_range
	_material_range=range

def _on_material_trigger(e):
	"""
	Function for the CONTROL_MATERIAL_TRIGGER event.
	This function triggers the CONTROL_MATERIAL event depending on the touch position on the vive controller.
	"""
	trackpad = vizconnect.getRawInput('r_hand_input').getTrackpad()
	# Calculate distance from the center of the touchpad to disable the event there.
	# Controls in that region would be unprecise.
	magnitude = math.sqrt(trackpad[0]**2+trackpad[1]**2)
	if magnitude <=.2:
		return
	# Calculate the angle between the x-axis and the trackpad point. (counter clockwise)
	# Results reach from 0 to 2 pi radiants.
	# trackpad/magnitude is used to get a vector with length 1
	if trackpad[1] >= 0:
		angle = math.acos(trackpad[0]/magnitude)
	else:
		angle = 2 * math.pi - math.acos(trackpad[0]/magnitude)
	# Divide the trackpad in equal sized sectors
	num_materials = float(_material_range[1] - _material_range[0]+1)
	number = int(angle * num_materials / (2 * math.pi))
	# Trigger the event
	viz.sendEvent(CONTROL_MATERIAL, number + _material_range[0])
_c.callback(viz.getEventID("CONTROL_MATERIAL_TRIGGER"), _on_material_trigger)
