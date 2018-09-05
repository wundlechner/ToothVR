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

# Directory, that opens when opening a new file.
standard_directory = 'C:\\Programmierzeug\\Testdaten\\'
# Directory to the python files of ParaView. Is ParaView installed in the standard directory, this should already work.
path_to_paraview_libs = 'C:\\Program Files\\ParaView 5.4.1-Qt5-OpenGL2-Windows-64bit\\bin\\Lib\\site-packages\\'
# Defines if the programm is controlled with a controller and keyboard, or with a SteamVR headset.
# Automatic detection of SteamVR by the lines of code below
control_scheme = 'controller'
# Change the level of multisample to 2, 4, 8 or 16 for nicer grafics but less performance
multi_sample_level = 4
# Change the displayed values. Values available in testdata: equivalent_stress, material
coloring_name = "equivalent_stress"
# Defines the name of the material array in the data. This is used to seperate the different parts. "material" should be fine.
material_name = "material"

# Check if steamvr is running to change controll scheme
import psutil
for pid in psutil.pids():
	p = psutil.Process(pid)
	if p.name() == "vrmonitor.exe":
		print("Found running SteamVR")
		control_scheme = 'steamvr'