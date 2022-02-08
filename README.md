# Data_Extractor
Program to extract data from an image of a line or scatter plot. 

Dependencies: matplotlib v3.3.2, numpy v1.19.2, PIL v8.0.1, tkinter v8.6

The main file is data_extractor.py.
input_UI, lineplot and scatterplot are modules required by data_extractor.

The folder graph_images contains a few graphs to test.
They can be placed anywhere: a file dialog will allow the user to open them.

The UI is pretty straightforward. Note that the points on the axes can be reselected by 
pressing the buttons again.

The results will be displayed as a matplotlib.pyplot plot and saved as CSV in the cd.
The files will be called absolute, and centred or thinned (for scatter or line, respectively).
The absolute file has all the data pixels contained in the image.
The centred or thinned file has the points estimated to be in the centre of the scatter point
or the line, respectively.
