import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np

im_path=None

class Graph:
    def __init__(self,im_path, x_axis, y_axis, x_axis_values,y_axis_values, graph_type):
        self.path=im_path
        self.x_axis=np.rint(np.array(x_axis))
        self.y_axis=np.rint(np.array(y_axis))
        self.x_axis_values=x_axis_values
        self.y_axis_values=y_axis_values
        self.type=graph_type.get()
        self.RGB_limit=250

def initialise():
    """Creates a tkinter user interface to open an image of a graph.
    It asks for
    - the type of graph (scatter or line),
    - two points on the x-axis and their coordinates,
    - two points on the y-axis and their coordinates.
    It returns a class object with all the above information."""

    x_axis_connect=None
    x_axis_plot=None

    y_axis_connect=None
    y_axis_plot=None

    root=tk.Tk()
    root.wm_title("Data extractor")

    #create a plt.figure and place it in a canvas which is placed in the root
    fig=plt.figure(figsize=(5, 4), dpi=100)
    canvas=FigureCanvasTkAgg(fig, master=root)  
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=8, columnspan=4)

    #places the plt toolbar under the canvas
    toolbarFrame=tk.Frame(master=root)
    toolbarFrame.grid(row=9,column=1, columnspan=4)
    NavigationToolbar2Tk(canvas, toolbarFrame)

    def draw_graph(fig,canvas,image_path=None):
        """plots image on the canvas """
        global im_path
        im_path=image_path
        if im_path:
            img=mpimg.imread(im_path)
            fig.add_subplot(111) #returns axes
            plt.imshow(img)
            plt.axis('off')
            canvas.draw()
    

    def open_file():
        """Command for dropdown menu, which provides path of image to display."""
        ftypes=[('Image','*.PNG')]
        dlg=tk.filedialog.Open(root,filetypes=ftypes)
        fl=dlg.show()
        draw_graph(fig,canvas,image_path=fl)
    
    def file_dialog():
        """Creates menubar with option to open a file"""
        menubar=tk.Menu(root)
        fileMenu=tk.Menu(menubar)
        fileMenu.add_command(label='Open',font=('', '12'), command=open_file)
        menubar.add_cascade(label='File', menu=fileMenu)
        root.config(menu=menubar)
    file_dialog()

    def pick_x_axis(event):
        """"Function that adds the coordinates of two points on the x-axis,
        if clicked with the mouse right button.
        It then plots the two points on the canvas."""
        global x_axis
        if event.button==3:
            x=(event.xdata, event.ydata)
            x_axis.append(x)

            if len(x_axis)==2:
                global  x_axis_plot,x_axis_connect
                canvas.mpl_disconnect(x_axis_connect) #disconnects event from canvas
                x=np.array(x_axis)[:,0]
                y=np.array(x_axis)[:,1]
                x_axis_plot=plt.scatter(x,y, marker='+')
                canvas.draw()

    def x_axis_selection():
        """Connects the pick_x_axis event to the canvas.
        It also empties the list of the points on the x-axis
        and removes the plot of the two points if present."""
        global x_axis,x_axis_plot, x_axis_connect
        x_axis=[]
        try:
            x_axis_plot.remove() #removes plot of x-points if present
        except:
            pass    
        canvas.draw()
        x_axis_connect=canvas.mpl_connect("button_press_event", pick_x_axis) #connects event to canvas
        
        
    button_x_axis=tk.Button(root,text="Right click on two\npoints on the x-axis",width=30,font=('Helvetica', '14'), command=x_axis_selection)
    button_x_axis.grid(row=5, column=0,padx=10,pady=10)

    def pick_y_axis(event):
        """"Function that adds the coordinates of two points on the y-axis,
        if clicked with the mouse right button.
        It then plots the two points on the canvas."""
        global y_axis
        if event.button==3:
            y=event.xdata, event.ydata
            y_axis.append(y)
            if len(y_axis)==2:
                global y_axis_plot, y_axis_connect
                canvas.mpl_disconnect(y_axis_connect)
                x=np.array(y_axis)[:,0]
                y=np.array(y_axis)[:,1]
                #plt.sca(img1[0])
                y_axis_plot=plt.scatter(x,y,marker='+')
                canvas.draw()

    def y_axis_selection():
        """Connects the pick_y_axis event to the canvas.
        It also empties the list of the points on the y-axis
        and removes the plot of the two points if present."""
        global y_axis,y_axis_plot, y_axis_connect
        y_axis=[]
        try:
            y_axis_plot.remove()
        except:
            pass
        canvas.draw()
        y_axis_connect=canvas.mpl_connect("button_press_event", pick_y_axis)

    button_y_axis=tk.Button(root,text="Right click on two\npoints on the y-axis",width=30,font=('Helvetica', '14'), command=y_axis_selection)
    button_y_axis.grid(row=6, column=0,padx=10,pady=10)

    #Radiobuttons for 'line' or 'scatter' graph type
    graph_type=tk.StringVar()
    type_label=tk.Label(root, text='Select the type of graph.',font=('Helvetica', '14'))
    type_label.grid(row=1,column=0,padx=10,pady=10)
    line_radio=tk.Radiobutton(root,text='Line',variable=graph_type, value='line',font=('Helvetica', '12'))
    scatter_radio=tk.Radiobutton(root,text='Scatter',variable=graph_type, value='scatter',font=('Helvetica', '12'))
    line_radio.grid(row=2,column=0,padx=10,pady=10)
    scatter_radio.grid(row=3,column=0,padx=10,pady=10)
    line_radio.select()

    #Entries for points on x and y axes, with labels
    coordinates_label=tk.Label(root, text='Enter the coordinates of the\npoints on the axes in the order\nyou selected them',width=30,anchor='w',justify='left',font=('Helvetica', '14'))
    coordinates_label.grid(row=1,column=5,columnspan=2,padx=10,pady=10)

    x1=tk.StringVar()
    x2=tk.StringVar()
    x_label=tk.Label(root,text='X values of x-axis',font=('Helvetica', '14'),anchor='w')
    x1_entry=tk.Entry(root, textvariable=x1)
    x2_entry=tk.Entry(root, textvariable=x2)
    x_label.grid(row=2,column=5,padx=10,pady=10)
    x1_entry.grid(row=3,column=5)
    x2_entry.grid(row=3, column=6)

    y1=tk.StringVar()
    y2=tk.StringVar()
    y_label=tk.Label(root,text='Y values of y-axis',font=('Helvetica', '14'),anchor='w')
    y1_entry=tk.Entry(root, textvariable=y1)
    y2_entry=tk.Entry(root, textvariable=y2)
    y_label.grid(row=4,column=5,padx=10,pady=10)
    y1_entry.grid(row=5,column=5)
    y2_entry.grid(row=5, column=6)

    info="Extract data from a PNG file. It can be a line or a scatter plot.\nIn the case of a line plot, make sure the plot is not multivalued with respect to the x-variable."
    info_label=tk.Label(root,text=info,font=('Helvetica', '14'),height=3,justify='left')
    info_label.grid(row=0, column=1, columnspan=4,padx=10,pady=10)

    def _quit():

        root.quit()     
        root.destroy()


    quit_button=tk.Button(master=root, text="Extract",font=('Helvetica', '14'),height=2, command=_quit)
    quit_button.grid(row=9,column=5,rowspan=2,columnspan=2,sticky='nesw',padx=10,pady=10)

    tk.mainloop()
    plt.close()
    

    try:
        im_path+''
        x_axis_values=np.array([x1.get(),x2.get()]).astype(np.float)
        y_axis_values=np.array([y1.get(),y2.get()]).astype(np.float)
        graph=Graph(im_path, x_axis, y_axis, x_axis_values,y_axis_values, graph_type)
        return graph
    except:
        print("Make sure you enter all information")
        return None

def display_input(graph):
    """Prints input"""
    if graph:
        print('File path',graph.path)
        print('Pixel coordinates of x-axis\n',graph.x_axis)
        print('Pixel coordinates of y-axis\n',graph.y_axis)
        print('Real coordinates of x-axis',graph.x_axis_values)
        print('Real oordinates of x-axis',graph.y_axis_values)
        print('Graph type',graph.type)
    else:
        print('Something went wrong')


if __name__=="__main__":
    graph=initialise()
    display_input(graph)


