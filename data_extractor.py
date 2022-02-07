import matplotlib.pyplot as plt
import numpy as np
import input_UI
import lineplot 
import scatterplot

graph=input_UI.initialise()
input_UI.display_input(graph)

if graph:
    graph=lineplot.pixelate(graph)
    graph=lineplot.pixel2value(graph)

    if graph.type=='line':
        thinned_line=lineplot.line_thinner(graph)
        thinned_line=np.array(thinned_line)
        thinned_line=lineplot.line2line(thinned_line,graph)

        absolute_line=lineplot.absolute_data(graph)
        absolute_line=np.array(absolute_line)
        absolute_line=lineplot.line2line(absolute_line,graph)

        with open('Absolute line plot.csv','w') as f:
            f.write('x, y\n')
            np.savetxt(f,absolute_line,delimiter=', ')

        with open('Thinned line plot.csv','w') as f:
            f.write('x, y\n')
            np.savetxt(f,thinned_line,delimiter=', ')

        
        plt.plot(thinned_line[:,0], thinned_line[:,1],'o', markersize=3)
        plt.plot(absolute_line[:,0], absolute_line[:,1,],'s',markersize=1)
        plt.show()
        plt.close()

    elif graph.type=='scatter':
        data=lineplot.absolute_data(graph)
        scatter, points =scatterplot.scatterplot(data,graph)

        with open('Absolute scatter plot.csv','w') as f:
            f.write('x, y\n')
            data=np.array(data)
            data=lineplot.line2line(data,graph)
            np.savetxt(f,data,delimiter=', ')

        with open('Centred scatter plot.csv','w') as f:
            f.write('x, y\n')
            scatter=lineplot.line2line(scatter,graph)
            np.savetxt(f,scatter,delimiter=', ')

        for p in points:
            p=np.array(p)
            p=lineplot.line2line(p,graph)
            plt.scatter(p[:,0],p[:,1])
        
        plt.scatter(scatter[:,0],scatter[:,1], s=3)
        plt.show()


