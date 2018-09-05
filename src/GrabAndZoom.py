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

import viz
import HelpFunctions


class GrabAndZoom(viz.EventClass):
	"""
	Class for grabbing and zooming into objects.
	To grab an object use the grab() method with the number of the hand.
	The number of the hand (in grab(hand_number) and ungrab(hand_number)) is the index of the hand in the tracker list.
	"""
	def __init__(self, trackers, obj=None):
		"""
		Initialize the object which handles the grabs and zooming.
		"""
		viz.EventClass.__init__(self)
		self._obj = obj
		if len(trackers) > 2:
			raise ValueError("Currently only up to 2 trackers are supported. Please use less trackers.")
		
		# variables to save the current state
		self._grabs = {0:None, 1:None}
		self._zooming_object = None

		# Grabber objects which follow the controllers
		self._grabbers = []
		for tracker in trackers:
			tmp = viz.addGroup()
			viz.link(tracker, tmp)
			self._grabbers.append(tmp)
		
		# Zooming objects which follow the controllers and are needed for the zooming calculation.
		# Different objects than grabbers are needed to use different linking modes.
		self._zoomers = []
		for tracker in trackers:
			tmp = viz.addGroup()
			viz.link(tracker, tmp, mask=viz.LINK_POS)
			self._zoomers.append(tmp)


	def set_item(self, obj):
		"""
		Set the item, which can be grabbed and zoomed.
		"""
		self._obj = obj


	def grab(self, hand_number):
		"""
		Trigger the grab.
		hand_number is the index of the hand in the tracker list.
		"""
		# if you're currently not zooming
		if self._zooming_object is None:
			self._grabs[hand_number] = _Grab(self._grabbers[hand_number], self._obj)
		
		# if you're currently not zooming and both grabbed objects are the same
		if self._zooming_object is None and self._grabs[0] is not None and self._grabs[1] is not None: 
			if self._grabs[0].grabbed_object is self._grabs[1].grabbed_object:
				# release grabs in reverse order to keep the original parents of the object
				self.ungrab(hand_number)
				self.ungrab(1-hand_number)
				self._zooming_object = _Zoom(self._obj, self._zoomers[0], self._zoomers[1])
				self.callback(viz.UPDATE_EVENT, self._zooming_object.update)


	def ungrab(self, hand_number):
		"""
		Trigger the release of an object.
		hand_number is the index of the hand in the tracker list.
		"""
		if self._zooming_object is None:
			if not self._grabs[hand_number] is None:
				# if you're currently NOT in zooming mode
				self._grabs[hand_number].stop()
				self._grabs[hand_number] = None
		else:
			# if you're currently in zooming mode
			self.callback(viz.UPDATE_EVENT, None)
			self._zooming_object.stop()
			self._zooming_object = None
			# Grab with all grabbers except hand_number
			for i in range(len(self._grabs)):
				if not i == hand_number:
					self.grab(i)



class _Zoom:
	"""
	Execute the zoom of the obj between two grabbers
	"""
	def __init__(self, obj, grabber0, grabber1):
		# Initialize the variables
		self._grabbed_object = obj
		self._initial_grab_distance = HelpFunctions.get_distance(
												grabber0.getPosition(mode=viz.ABS_GLOBAL),
												grabber1.getPosition(mode=viz.ABS_GLOBAL))
		# helper_node is the grabber which still holdes the object (parent relationship)
		self._helper_node = grabber0
		# distant_grabber is used to define the orientation of the obj and to calculate the distance
		self._distant_grabber = grabber1

		# Prepare grabbers for zooming
		self._helper_node.lookAt(self._distant_grabber.getPosition(), mode=viz.ABS_GLOBAL)
		self._helper_node.setScale([1.0, 1.0, 1.0])

		# Save original parent of the object to restore it later
		self._grabbed_object_old_parent = HelpFunctions.get_parent(self._grabbed_object)
		
		# Prepare object for zooming
		HelpFunctions.set_parent_without_changing_transform(self._grabbed_object, self._helper_node) 


	def update(self, e):
		"""
		Update the current orientation and scale.
		"""
		self._helper_node.lookAt(self._distant_grabber.getPosition(), mode=viz.ABS_GLOBAL)
		new_distance = HelpFunctions.get_distance(
						self._helper_node.getPosition(mode=viz.ABS_GLOBAL),
						self._distant_grabber.getPosition(mode=viz.ABS_GLOBAL))
		self._helper_node.setScale([new_distance / self._initial_grab_distance]*3)


	def stop(self):
		"""
		Restore original values.
		"""
		# Restore original parant of the zoomed object
		HelpFunctions.set_parent_without_changing_transform(self._grabbed_object, self._grabbed_object_old_parent)
		
		# Restore defaults of the grabber
		self._helper_node.setScale([1.0, 1.0, 1.0])



class _Grab:
	"""
	Execute the grab of the obj
	"""
	def __init__(self, grabber, obj):
		"""
		Start the grab.
		"""
		self.grabbed_object = obj
		self._grabber = grabber
		
		# Save original parent of the object to restore it later
		self._grabbed_object_old_parent = HelpFunctions.get_parent(self.grabbed_object)
		
		# Prepare object for grabbing
		HelpFunctions.set_parent_without_changing_transform(self.grabbed_object, self._grabber)


	def stop(self):
		"""
		Stop the grab.
		"""
		# Restore original parant of the zoomed object
		HelpFunctions.set_parent_without_changing_transform(self.grabbed_object, self._grabbed_object_old_parent)



# Code to test the behaviour. (No functionality for the project)
if __name__ == "__main__":
	import vizconnect
	import Controls
	
	vizconnect.go("vizconnect_config_steamvr.py")

	r_input = vizconnect.getRawInput('r_hand_input')
	l_input = vizconnect.getRawInput('l_hand_input')
	inputs = [r_input, l_input]

	r_tracker = vizconnect.getRawTracker('r_hand_tracker')
	l_tracker = vizconnect.getRawTracker('l_hand_tracker')
	trackers = [r_tracker, l_tracker]
	
	r_model = r_tracker.addModel()
	viz.link(r_tracker, r_model)
	l_model = l_tracker.addModel()
	viz.link(l_tracker, l_model)

	environment = viz.addChild('sky_day.osgb')
	obj = viz.addChild('soccerball.osgb',pos=[0,1.8,0])
	gaz = GrabAndZoom(trackers, obj)
	gaz.callback(Controls.CONTROL_HAND_GRAB, gaz.grab)
	gaz.callback(Controls.CONTROL_HAND_RELEASE, gaz.ungrab)
