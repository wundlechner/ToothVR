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

# import vizard stuff
import viz
import vizinput
import vizshape
import vizconnect
import steamvr

# Start control config file to initialize HMDs, trackers, controller and more.
# Later imports depend on initialized controls
import config as cfg
import os.path
if os.path.isfile('vizconnect_config_' + cfg.control_scheme + '.py'):
	vizconnect.go('vizconnect_config_' + cfg.control_scheme + '.py')

# import project modules
import Simulation_Data
from GrabAndZoom import GrabAndZoom
import Controls
import HelpFunctions


class ToothVR(viz.EventClass):
	"""
	Class to start and manage the ToothVR application.
	"""
	def __init__(self):
		"""
		Initialize everything independent of the viewed data, so ToothVR can be started just by calling run()
		"""
		viz.EventClass.__init__(self)
		# Init variables
		self._simulation_data = None
		# ... for stressindicator function
		self._stressindicator_text = None
		self._stressindicator = None
		# ... for the clipping function
		self._clip_plane_present = False
		self._clip_plane = None
		# ... for the environment
		self._room = None
		self._ground = None
		
		# Setup the different parts
		r_tracker = vizconnect.getRawTracker('r_hand_tracker')
		l_tracker = vizconnect.getRawTracker('l_hand_tracker')
		self._grab_and_zoom = GrabAndZoom([r_tracker, l_tracker])
		self._setup_controls()
		# Stressindicator would be useless without a tracked controller
		if cfg.control_scheme == "steamvr":
			self._setup_stressindicator()
		self._setup_clip_plane()
		self._setup_environment()
		self._setup_vizard_configuration()
		
		
	def _setup_controls(self):
		"""
		Setup all callback events for the controls.
		"""
		# Events are triggered by the Controls module
		self.callback(Controls.CONTROL_NEW_FILE, self.select_file)
		self.callback(Controls.CONTROL_CLIP, self.clip_button_press)
		self.callback(Controls.CONTROL_TOGGLE_ENVIRONMENT, self.switch_environment)
		self.callback(Controls.CONTROL_CLOUD_INCREASE, lambda : self._simulation_data.set_cloud_point_size(self._simulation_data.get_cloud_point_size()+1))
		self.callback(Controls.CONTROL_CLOUD_DECREASE, lambda : self._simulation_data.set_cloud_point_size(self._simulation_data.get_cloud_point_size()-1))
		self.callback(Controls.CONTROL_TOGGLE_STRESSINDICATOR, self.toggle_stressindicator)
		self.callback(Controls.CONTROL_HAND_GRAB, self._grab_and_zoom.grab)
		self.callback(Controls.CONTROL_HAND_RELEASE, self._grab_and_zoom.ungrab)
		
		
		
	def _setup_stressindicator(self):
		"""
		Setup all objects for the stessindicator.
		"""
		# Create a 3D text to display the measured stress
		self._stressindicator_text = viz.addText3D('3D Text',pos=[0,-1,0])
		self._stressindicator_text.alignment(viz.ALIGN_LEFT_BOTTOM)
		self._stressindicator_text.color(viz.GREEN)
		self._stressindicator_text.setScale([.05,.05,.05])
		# Create a green sphere where the measurement takes place
		self._stressindicator = vizshape.addSphere(radius=0.01, color=viz.GREEN)
		self._stressindicator_text.setParent(self._stressindicator)
		self._stressindicator_text.setPosition([0,.1,0], viz.ABS_PARENT)
		# Create a group to add an offset to the measurement sphere
		tmp = viz.addGroup()
		self._stressindicator.setParent(tmp)
		self._stressindicator.setPosition([0,-.01,.05],viz.ABS_PARENT)
		self._stressindicator.setEuler([0,90,0],viz.ABS_PARENT)
		# Connect the stressindicator to the right controller
		viz.link(vizconnect.getRawTracker('r_hand_tracker'), tmp)
		# Hide the objects until the stressindicator gets used
		self._stressindicator.visible(False)


	def _setup_clip_plane(self):
		"""
		Create a plane with a sissors logo, a grid and a grey back.
		"""
		# Create the white center plane
		self._clip_plane = vizshape.addPlane(size=(.103,.103), axis=vizshape.AXIS_Y, cullFace=False, cornerRadius=0.0025, lighting=False)
		# Create the back side
		back = vizshape.addPlane(size=(.103,.103), axis=vizshape.AXIS_Y, cullFace=False, cornerRadius=0.0025, lighting=False, color=(0.7,0.7,0.7), parent=self._clip_plane)
		back.setPosition([0,0.002,0])
		# Create the front side with the sissors logo
		sissors = vizshape.addPlane(size=(.08,.08), axis=vizshape.AXIS_Y, cullFace=False, lighting=False, parent=self._clip_plane)
		sissors.setPosition([0,-0.002,0])
		tex = viz.addTexture('assets/sissors.png')
		sissors.texture(tex)
		# Create the grid so the user sees better where the cut goes
		grid = vizshape.addGrid(size=(.5,.5), step=.01, boldStep=0.0, axis=vizshape.AXIS_Y, lighting=False, parent=self._clip_plane)
		# Hide the objects until the clipping function is activated
		self._clip_plane.visible(False)


	def _setup_environment(self):
		"""
		Setup all objects to create the environments. Environments can be switched with the R key on the keyboard.
		"""
		# Add the comfortable "kitchen" room
		self._room = viz.addChild("Room.osgb")
		self._room.setScale(.01,.01,.01)
		
		# Create the clean "ground" environment (just a white round ground).
		# This environment isn't saved in a osgb file, because the lights couldn't be configured to use the light group 1 instead of 0.
		# Only 8 lights are allowed per light group. Room has already 8 lights.
		img = viz.addTexture('assets/ground.png')
		self._ground = vizshape.addQuad()
		self._ground.setScale(6,6,6)
		self._ground.setEuler(0,90,0)
		self._ground.texture(img)
		# Create the lights for the "ground" envirtonment.
		light_positions = [
			[0,  5,   0], # From top
			[0,  -5,  0], # From bottom
			[3,  1.5, 0],
			[-3, 1.5, 0],
			[0,  1.5, 3],
			[0,  1.5, -3]]
		for light_position in light_positions:
			light = viz.addLight(group = 1)
			light.setParent(self._ground)
			light.spread(45)
			light.intensity(1)
			light.spotexponent(3)
			light.setPosition(light_position, mode=viz.ABS_GLOBAL)
			light.lookAt(self._ground.getPosition())
		
		# Hide the second environment until the environment gets changed
		self._ground.visible(False)


	def _setup_vizard_configuration(self):
		"""
		Setup some stuff for Vizard
		"""
		viz.setMultiSample(cfg.multi_sample_level)
		
		# Disable the head light for better lighting
		viz.MainView.getHeadLight().disable()
		
		# Disable the mouse with controller controls.
		# Without deactivation, the controller would move the mouse.
		if cfg.control_scheme == "controller":
			# Trap the mouse in the graphics window.
			viz.mouse.setTrap(viz.ON)
			# Make the mouse invisible.
			viz.mouse.setVisible(viz.OFF)
			
		# Display models for the trackers
		tracker_names = ['r_hand_tracker', 'l_hand_tracker']
		for tracker_name in tracker_names:
			controller = vizconnect.getRawTracker(tracker_name)
			
			if cfg.control_scheme == "steamvr":
				if not isinstance(controller, viz.VizGroup):
					# Display HTC Vive controller model if the controller is connected
					model = controller.addModel()
					viz.link(controller, model)
				
			elif cfg.control_scheme == "controller":
				# Display a sphere, when controlled with a gamepad
				model = vizshape.addSphere(.05, color=viz.GRAY)
				viz.link(controller, model)


	def run(self):
		"""
		Start the application by selecting a file.
		"""
		self.select_file()
		
		
	def select_file(self):
		"""
		Select a file. If one is already loaded, it gets replaced.
		"""
		# Delete old data if available
		if self._simulation_data:
			self._simulation_data.remove()
		# Find the new file
		file = vizinput.fileOpen(title = "Please choose your file containing the simulation data.", filter=[('VTK Files','*.vtk')], directory=cfg.standard_directory)
		# If no file is selected close the application
		if file == '':
			viz.quit()
			return
		# Load data
		self._simulation_data = Simulation_Data.Simulation_Data(file)
		# Update Controls for new data
		self._grab_and_zoom.set_item(self._simulation_data.origin_node)
		Controls.set_material_range(self._simulation_data.get_material_range())
		self.callback(Controls.CONTROL_CYCLE_VIEW_MODE, self._simulation_data.cycle_view_mode)
		self.callback(Controls.CONTROL_MATERIAL, self._simulation_data.toggle_material)
		# Place model in a nice position
		self._simulation_data.origin_node.setPosition(0,1,0)
		self._simulation_data.origin_node.setScale(.1,.1,.1)
		self._simulation_data.origin_node.setEuler(0,0,-90)


	def toggle_stressindicator(self):
		"""
		Activate or deactivate the stressindicator function.
		Due to performance issues, it should be deactivated most of the time.
		"""
		# Toggle visibility and functionality in update loop
		if self._stressindicator.getVisible():
			self._stressindicator.visible(False)
			self.callback(viz.UPDATE_EVENT, None)
		else:
			self._stressindicator.visible(True)
			self.callback(viz.UPDATE_EVENT, self.update_stressindicator)


	def update_stressindicator(self, e=None):
		"""
		Update the meassured data.
		"""
		# Read indicator position
		indicator_position = self._stressindicator.getPosition(viz.ABS_GLOBAL)
				
		# Convert the indicator position to the position in the ParaView coordinate system.
		# Create a node3d object for the get_local_position() method
		tmp = viz.addGroup()
		tmp.setPosition(indicator_position)
		position = HelpFunctions.get_local_position(self._simulation_data.cloud_materials[1].getChildren()[0], tmp)
		tmp.remove()
		
		# Read the equivalent_stress from ParaView
		stress = self._simulation_data.get_probe_value(position)
		
		# Update the displayed text
		self._stressindicator_text.message(str(stress))


	def clip_button_press(self):
		"""
		Display the clipping plane with the first call and clip the object with the second call.
		"""
		if self._clip_plane.getVisible():
			# Second call to fulfill the clip
			self._clip_plane.visible(False)
			# Update clipping information
			self._simulation_data.clip_normal = HelpFunctions.get_local_normal(self._simulation_data.cloud_materials[1].getChildren()[0], self._clip_plane)
			self._simulation_data.clip_origin = HelpFunctions.get_local_position(self._simulation_data.cloud_materials[1].getChildren()[0], self._clip_plane)
			# Apply clip by reloading the models
			self._simulation_data.reload_models()
			# Update the controls to grab the object again
			self._grab_and_zoom.set_item(self._simulation_data.origin_node)
		else:
			# First call to diplay the clipping plane
			self._clip_plane.visible(True)
			self._clip_plane.setPosition(0,1,0, viz.ABS_GLOBAL)
			self._clip_plane.setEuler(0,180,0)
			# Update the controls to grab the clipping plane
			self._grab_and_zoom.set_item(self._clip_plane)
			
			
	def switch_environment(self):
		"""
		Switch the environment.
		"""
		self._ground.visible(not self._ground.getVisible())
		self._room.visible(not self._room.getVisible())
		# Light groups change between 0 (default) and 1 (for the "ground" environment)
		viz.setLightGroup(1-viz.getLightGroup())


if __name__ == "__main__":
	app = ToothVR()
	app.run()
