from PIL import Image
import numpy as np
import itertools

"""Contains functions to convert images to pixels and remove the axes,
functions for line plots and
functions to assign values to pixels"""

#image
def pixelate(graph):
    """opens image and assigns pixels to pix
    adds pix, maximum x value, maximum y value and the total number of pixels
    to the graph class."""
    im=Image.open(graph.path)
    graph.pix=im.load()
    graph.x_max=im.size[0]
    graph.y_max=im.size[1]
    graph.num_pxls=graph.x_max*graph.y_max

    graph=remove_axes(graph)
    
    return graph

def remove_axes(graph):
    """Finds the upper and rightmost limits of the x and y axes respectively
    and removes all pixels below or left of the axis.
    
    If ticks point inwards it won't eliminate them unless the input points
    on the axes lie on them."""
 
    x1, x2 = graph.x_axis #[0],graph.x_axis[1]

    if x1[0]>x2[0]: #chooses the point with highest x to reduce chance of origin being selected
        x_point=x1
    else:
        x_point=x2
    x,y=x_point
    x,y=int(x),int(y)
    colour=graph.pix[x,y]
 
    for dy in range(50):
        if graph.pix[x,y-dy]==colour: #-dy because y is inverted in PIL image
            upper_limit=y-dy
        else:
            break
    #sets pixels outside of axis to white
    if upper_limit:
        for y in range(upper_limit, graph.y_max):
            for x in range(graph.x_max):
                graph.pix[x,y]=(255,255,255)

    y1, y2 = graph.y_axis

    if y1[1]<y2[1]:
        y_point=y1 
    else:
        y_point=y2
    x,y=y_point
    x,y=int(x),int(y)
    colour=graph.pix[x,y]
    for dx in range(50): 
        if graph.pix[x+dx,y]==colour:
            right_limit=x+dx
        else:
            break
    #sets pixels outside of axiss to white
    if right_limit:
        for x in range(right_limit+1):
            for y in range(graph.y_max):
                graph.pix[x,y]=(255,255,255)
        return graph

#lineplot
def line_thinner(graph):
    """Calculates the middle of a line by inferring the sign of the slope
    and then by projecting a pixel on one side onto a segment formed by two
    pixels on the other side of the line. It then finds the midpoint between the
    projection and the point that was projected.
    If the line is horizontal it finds the point on the other side in a vertical line
    and calculates the midpoint."""
    line=[]

    for x in range(graph.x_max):
        for y in range(graph.y_max):
            if graph.pix[x,y][0]<graph.RGB_limit or graph.pix[x,y][1]<graph.RGB_limit or graph.pix[x,y][2]<graph.RGB_limit:
                x0=x
                y0=y
                P=np.array([x0,y0]) #point to project
                
                slope=line_slope(x0,y0,graph)

                if slope=='positive':
                    A,B=positive_triangle(x0,y0,graph) #points on opposite segment
                    distance2=np.dot((A-B),(A-B))   #distance **2
                    if distance2!=0:                #if 0 A==B
                        projection=np.dot((P-B),(A-B))/distance2*(A-B)+B
                        midpoint=(projection+P)/2
                elif slope=='negative':
                    A,B=negative_triangle(x0,y0,graph)
                    distance2=np.dot((A-B),(A-B))
                    if distance2!=0:
                        projection=np.dot((P-B),(A-B))/distance2*(A-B)+B
                        midpoint=(projection+P)/2
                elif slope=='horizontal':
                    midpoint=horizontal_thinner(x0,y0,graph)
                else:
                    break
                
                line.append(tuple(midpoint))            
                break
    return line

def line_slope(x,y,graph):
    """Determines the local slope of the line by checking first pixel on the right,
    left, below. If all are nonwhite it checks top_left and top_right.
    It doesn't check above because pixels are iterated from y=0 to y_max"""

    right=graph.pix[x+1,y][0]<graph.RGB_limit or graph.pix[x+1,y][1]<graph.RGB_limit or graph.pix[x+1,y][2]<graph.RGB_limit
    bottom=graph.pix[x,y+1][0]<graph.RGB_limit or graph.pix[x,y+1][1]<graph.RGB_limit or graph.pix[x,y+1][2]<graph.RGB_limit
    left=graph.pix[x-1,y][0]<graph.RGB_limit or graph.pix[x-1,y][1]<graph.RGB_limit or graph.pix[x-1,y][2]<graph.RGB_limit
        
    if right and bottom and left:
        top_left=graph.pix[x-1,y-1][0]<graph.RGB_limit or graph.pix[x-1,y-1][1]<graph.RGB_limit or graph.pix[x-1,-1][2]<graph.RGB_limit
        top_right=graph.pix[x+1,y-1][0]<graph.RGB_limit or graph.pix[x+1,y-1][1]<graph.RGB_limit or graph.pix[x+1,y-1][2]<graph.RGB_limit
        if top_left:
            return 'negative'
        elif top_right:
            return 'positive'
        else:
            return 'horizontal'
    elif right and bottom:
        return 'positive'
    elif bottom and left:
        return 'negative'
    else:
        return None
    
def positive_triangle(x0,y0,graph):
    """Finds A and B (two points on the other side of the line)
    by iterating vertical and horizontal lines.
    x is iterated in the positive direction, since the slope is positive"""
    
    for temp_y in range(y0,graph.y_max):
        if graph.pix[x0,temp_y][0]>graph.RGB_limit and graph.pix[x0,temp_y][1]>graph.RGB_limit and graph.pix[x0,temp_y][2]>graph.RGB_limit:
            y1=temp_y-1
            break
    A=np.array([x0,y1])
    for temp_x in range(x0,graph.x_max):
        if graph.pix[temp_x,y0][0]>graph.RGB_limit and graph.pix[temp_x,y0][1]>graph.RGB_limit and graph.pix[temp_x,y0][2]>graph.RGB_limit:
            x1=temp_x-1
            break
    B=np.array([x1,y0])

    return A, B

def negative_triangle(x0,y0,graph):
    """Finds A and B (two points on the other side of the line)
    by iterating vertical and horizontal lines.
    x is iterated in the negative direction, since the slope is negatice""" 
    for temp_y in range(y0,graph.y_max):
        if graph.pix[x0,temp_y][0]>graph.RGB_limit and graph.pix[x0,temp_y][1]>graph.RGB_limit and graph.pix[x0,temp_y][2]>graph.RGB_limit:
            y1=temp_y-1
            break
    A=np.array([x0,y1])
    for temp_x in range(x0,-1,-1):
        if graph.pix[temp_x,y0][0]>graph.RGB_limit and graph.pix[temp_x,y0][1]>graph.RGB_limit and graph.pix[temp_x,y0][2]>graph.RGB_limit:
            x1=temp_x-1
            break
    B=np.array([x1,y0])
    return A,B    

def horizontal_thinner(x0,y0,graph):
    """Finds midpoint in a vertical straight line"""
    for temp_y in range(y0,graph.y_max):
        if graph.pix[x0,temp_y][0]>graph.RGB_limit and graph.pix[x0,temp_y][1]>graph.RGB_limit and graph.pix[x0,temp_y][2]>graph.RGB_limit:
            y1=temp_y-1
            break
    y=(y1+y0)/2
    midpoint=np.array([x0,y])
    return midpoint

def absolute_data(graph):
    """appends all pixels less than RGB limit to data set"""
    line=[]
    for x in range(graph.x_max):
        for y in range(graph.y_max):
            if graph.pix[x,y][0]<graph.RGB_limit or graph.pix[x,y][1]<graph.RGB_limit or graph.pix[x,y][2]<graph.RGB_limit:
                line.append((x,y))
    return line

#assign values

def pixel2value(graph):
    """Determines linear relationship between the coordinates
    of the pixels selected at the start and the
    values assigned to them.
    real=slope*pixel+intercept """

    graph.xslope=np.diff(graph.x_axis_values)/np.diff(graph.x_axis[:,0])
    graph.xintercept=graph.x_axis_values[0]-graph.xslope*graph.x_axis[0,0]

    graph.yslope=np.diff(graph.y_axis_values)/np.diff(graph.y_axis[:,1])
    graph.yintercept=graph.y_axis_values[0]-graph.yslope*graph.y_axis[0,1]
    
    return graph 


def line2line(line,graph):
    """Changes the values of points from pixel coordinate to real coordinates"""
    line=line.astype(np.float)
    for i, x in enumerate(line[:,0]):
        line[i,0]=graph.xslope*x+graph.xintercept
    for i, y in enumerate(line[:,1]):
        line[i,1]=graph.yslope*y+graph.yintercept
    return line

