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
This file contains general functions, which don't belong to specific purposes.
"""
import viz
import math


def get_local_position(semi_parent, semi_child):
	"""
	This function calculates the position of the semi_child in relation to the semi_parent.
	"""
	# Save semi_child information
	parents = semi_child.getParents()
	child_pos = semi_child.getPosition(viz.ABS_GLOBAL)
	# Change parent
	semi_child.setParent(semi_parent)
	semi_child.setPosition(child_pos, viz.ABS_GLOBAL)
	# Read the relative position
	position = semi_child.getPosition(viz.ABS_PARENT)
	# Undo the changes
	semi_child.setParent(viz.WORLD)
	for parent in parents:
		semi_child.addParent(parent)
	semi_child.setPosition(child_pos, viz.ABS_GLOBAL)
	
	return position


def get_local_normal(semi_parent, semi_child):
	"""
	This function calculates the normal of the semi_child in relation to the semi_parent.
	"""
	# Save semi_child information
	parents = semi_child.getParents()
	child_euler = semi_child.getEuler(viz.ABS_GLOBAL)
	# Change parent
	semi_child.setParent(semi_parent)
	semi_child.setEuler(child_euler, viz.ABS_GLOBAL)
	# Read the relative normal
	normal = semi_child.getNormal(1, viz.ABS_PARENT)
	# Undo the changes
	semi_child.setParent(viz.WORLD)
	for parent in parents:
		semi_child.addParent(parent)
	semi_child.setEuler(child_euler, viz.ABS_GLOBAL)
	
	return normal


def get_distance(start, end):
	"""
	This function calculates the distance between two points.
	"""
	# Calculate vector between start and end
	x = end[0] - start[0]
	y = end[1] - start[1]
	z = end[2] - start[2]
	# Calculate magnitude of the vector
	return math.sqrt(x*x + y*y + z*z)


def set_parent_without_changing_transform(obj, parent):
	"""
	This function changes the parent of obj without changing its viz.ABS_GLOBAL properties.
	"""
	#	Save position/rotation/scale
	pos = obj.getPosition(viz.ABS_GLOBAL)
	euler = obj.getEuler(viz.ABS_GLOBAL)
	scale = obj.getScale(viz.ABS_GLOBAL)
	# 	Set Parent
	obj.setParent(parent)
	# 	Restore position/rotation/scale
	obj.setPosition(pos, viz.ABS_GLOBAL)
	obj.setEuler(euler, viz.ABS_GLOBAL)
	obj.setScale(scale)


def get_parent(obj):
	"""
	Returns the first parent if it has any, else it returns viz.WORLD (instead of None; normal behaviour)
	"""
	parents = obj.getParents()
	if len(parents)==0:
		return viz.WORLD
	else:
		return parents[0]



# Code to test the behaviour. (No functionality for the project)
if __name__ == "__main__":
	viz.go()
	# TODO: unittests draus machen
	ball_1 = viz.addChild('white_ball.wrl')
	ball_1.setPosition([0,1,0])
	ball_1.setEuler([0,-90,0])
	ball_2 = viz.addChild('white_ball.wrl')
	ball_2.setPosition([0,2,0])
	position = get_local_position(ball_1,ball_2)
	print("--------------Test1-------------")
	print("expected: [0.0, 0.0, 1.0]")
	print("actual:", position)
	
	obj1 = viz.addChild('white_ball.wrl')
	obj2 = viz.addChild('white_ball.wrl')
	ball_2.setParent(obj1)
	ball_2.addParent(obj2)
	ball_2.setPosition([0,2,0], viz.ABS_GLOBAL)
	position = get_local_position(ball_1,ball_2)
	print("--------------Test2-------------")	
	print("expected parents:", obj1, obj2)
	print("actual parents:", ball_2.getParents())
	
	print("--------------Test3-------------")	
	distance = get_distance([1,2,3], [2,5,10])
	print("expected: 7.681145747868608")
	print("actual:", distance)
