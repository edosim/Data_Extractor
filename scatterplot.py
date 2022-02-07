from PIL import Image
import lineplot
import itertools
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":
    
    #im_path=r"graph_images\Scatter markers.png"
    im_path=r"C:\Users\edoar\OneDrive\Documents\Backup 19-04-20\University\CHEM0062\projects\MAIN project\extract graphs\vsc stuff\graph_images\Scatter markers closer.png"
    #im_path=r"graph_images\desmos scatter close.png"
    #im_path=r'graph_images\Origin scatter.png'

    x_axis=np.array([[1202., 2050.],[1828., 2050.]]) #origin
    y_axis=np.array([[ 577., 637.],[ 577.,  1345.]]) #origin

    #x_axis=np.array([[500., 997.],[700., 997.]]) #desmos
    #y_axis=np.array([[ 140., 300.],[ 140.,  800.]]) #desmos
    graph_type='scatter'
    x_axis_values=np.array([1,2])
    y_axis_values=np.array([10,5])
    import input_UI
    graph=input_UI.Graph(im_path, x_axis, y_axis, x_axis_values,y_axis_values, graph_type)

    graph=lineplot.pixelate(graph)


"""Functions for scatter plots"""
neighbours=np.array([[-1,-1],
                    [0,-1],
                    [1,-1],
                    [1,0],
                    [1,1],
                    [0,1],
                    [-1,1],
                    [-1,0]])


def centre(points):
    """Finds centre of a point by calculating the average position of its pixels"""
    scatter=[]
    for p in points:
        p=np.array(p)
        x=np.mean(p[:,0])
        y=np.mean(p[:,1])
        scatter.append((x,y))
    scatter=np.array(scatter)
    return scatter

def short_neighbourhood(pixel, point, data, start):
    """Performs Moore neighbourhood on a point. It checks the adjacent points
    clockwise and stops when it finds a non-white point"""

    x,y=pixel
    for i,coordinates in enumerate(np.concatenate((neighbours[start:],neighbours[:start]))):
        dx=coordinates[0].item()
        dy=coordinates[1].item()
        if (x+dx,y+dy) in point:
            new_pixel=None
            break
        elif (x+dx,y+dy) in data:
            new_pixel=(x+dx,y+dy)
            break
        else:
            new_pixel=None
    
    #finds the starting point for the newfound pixel
    #i.e. the pixel it was approached from
    if new_pixel:
        i+=start
        if i>7:i-=8

        if i==1 or i==2: new_i=7
        if i==3 or i==4: new_i=1
        if i==5 or i==6: new_i=3
        if i==7 or i==0: new_i=5
    else:
        new_i=None
    return new_pixel, new_i

def fill_point_and_remove(point,data,graph):
    """Draws a rectangle around the scatter point(finds the maximum and minimum x and y)
    identifies non white pixels in it and removes the from data"""
    temp_point=np.array(point)
    min_x,max_x=np.amin(temp_point[:,0]),np.amax(temp_point[:,0])
    min_y,max_y=np.amin(temp_point[:,1]),np.amax(temp_point[:,1])

    rectangle=[(x,y) for (x,y) in itertools.product(range(min_x,max_x+1),range(min_y,max_y+1))]
    point=[(x,y) for (x,y) in rectangle if graph.pix[x,y][0]<graph.RGB_limit or graph.pix[x,y][1]<graph.RGB_limit or graph.pix[x,y][2]<graph.RGB_limit]
    data=[(x,y) for (x,y) in data if (x,y) not in rectangle]

    return point,data

def scatterplot(data,graph):
    """Finds contour of scatter points, fills them and calculates the centre of each scatter point"""

    points=[]
    point=[]
            
    while data:
        start=0
        pixel=data[0]
        point.append(pixel)

        while pixel:
            new_pixel, start=short_neighbourhood(pixel, point, data, start)
            if new_pixel:
                point.append(new_pixel)
            else:
                point,data=fill_point_and_remove(point,data,graph)
                points.append(point)
                point=[]
            pixel=new_pixel

    scatter=centre(points)
    return scatter, points

if __name__=="__main__":
    data=lineplot.absolute_data(graph)
    scatter, points =scatterplot(data,graph)
    graph=lineplot.pixel2value(graph)
    print(graph.xslope,graph.yslope)
    print(graph.xintercept,graph.yintercept)
      
    with open('Absolute scatter plot.csv','w') as f:
        f.write('x, y\n')
        data=np.array(data)
        np.savetxt(f,data,delimiter=', ')

    with open('Centred scatter plot.csv','w') as f:
        f.write('x, y\n')
        np.savetxt(f,scatter,delimiter=', ')

    for p in points:
        p=np.array(p)
        p=lineplot.line2line(p,graph)
        plt.scatter(p[:,0],graph.y_max-p[:,1])
    scatter=lineplot.line2line(scatter,graph)
    plt.scatter(scatter[:,0],graph.y_max-scatter[:,1], s=3)
    plt.show()