# ToothVR

This is the final version of my program, which I've created for my bachelor thesis. The current state is more like a prototype than a finished product. I publish this work so that you can be inspired and use parts of it to come up with even better solutions. Also this program is specialized on that one use-case I've had (dentistry). With more effort you can generalize it and use it for more diverse vtk files (Visualization Toolkit). In the folder doc you can find my thesis in german language. I'm sad, that I can't provide an english version, but there are translators on the internet :). If my work helped you, it would be cool if you mention my name in your product and contact me just for information.

ToothVR uses a combination of Vizard and ParaView to inspect vtk files in Virtual Reality (Tested with HTC Vive). It enables the user to dive into the point cloud data and see the structure from the inside.

Vizard is used for the interaction with the user. In python scripts the input is handled and commands are forwarded to the python interface of ParaView. ParaView handles the manipulation of the loaded file and provides the coordinates of the surface, which Vizard renders then.

The vtk files were provided by my university (Hochschule Augsburg University of Applied Sciences). The files were created in a process of scanning a tooth, doing a finite element analysis (stress simulation) for the generated mesh and converting the results into the vtk format. The vtk file is an unstructured grid type.

I hope I helped you.

Andreas Wundlechner